from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import db, PaymentTransaction, Job, PaymentStatus, JobStatus
from ..services.mock_payment_service import mock_payment_service
from ..utils.helpers import admin_required

bp = Blueprint('payments', __name__, url_prefix='/api/payments')

@bp.route('/initiate', methods=['POST'])
@jwt_required()
def initiate_payment():
    """
    Initiate a mock payment for a job.
    
    Expected JSON payload:
    {
        "job_id": 123,
        "amount": 1000.00,
        "phone": "254712345678"
    }
    """
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validate required fields
    if not data or 'job_id' not in data or 'amount' not in data:
        return jsonify({
            'success': False,
            'message': 'Missing required fields: job_id and amount are required'
        }), 400
    
    try:
        job_id = data['job_id']
        amount = float(data['amount'])
        phone = data.get('phone', '')
        
        # Verify job exists and belongs to the user
        job = Job.query.get(job_id)
        if not job:
            return jsonify({
                'success': False,
                'message': 'Job not found'
            }), 404
            
        if job.customer_id != current_user_id:
            return jsonify({
                'success': False,
                'message': 'Unauthorized: You can only make payments for your own jobs'
            }), 403
        
        # Create payment record
        payment = mock_payment_service.create_payment_record(
            user_id=current_user_id,
            amount=amount,
            job_id=job_id,
            method='mpesa',
            description=f'Payment for job #{job_id}'
        )
        
        # Update job status to pending payment
        if job.status != JobStatus.PENDING_PAYMENT:
            job.status = JobStatus.PENDING_PAYMENT
            db.session.commit()
        
        # In a real implementation, we would initiate STK push here
        # For the mock service, we'll simulate the payment immediately
        success, message, _ = mock_payment_service.simulate_payment(
            payment.reference,
            success=True  # Always succeed for now, can be made configurable
        )
        
        # Refresh payment data
        payment = PaymentTransaction.query.get(payment.id)
        
        return jsonify({
            'success': True,
            'message': 'Payment initiated successfully',
            'payment': {
                'id': payment.id,
                'reference': payment.reference,
                'amount': float(payment.amount),
                'status': payment.status,
                'created_at': payment.created_at.isoformat(),
                'metadata': payment.payment_metadata or {}
            }
        })
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'message': f'Invalid amount: {str(e)}'
        }), 400
    except Exception as e:
        current_app.logger.error(f"Error initiating payment: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Failed to initiate payment'
        }), 500

@bp.route('/status/<payment_reference>', methods=['GET'])
@jwt_required()
def check_payment_status(payment_reference):
    """Check the status of a payment."""
    current_user_id = get_jwt_identity()
    
    try:
        payment = PaymentTransaction.query.filter_by(reference=payment_reference).first()
        if not payment:
            return jsonify({
                'success': False,
                'message': 'Payment not found'
            }), 404
        
        # Verify the payment belongs to the user
        if payment.user_id != current_user_id:
            return jsonify({
                'success': False,
                'message': 'Unauthorized: You can only check your own payments'
            }), 403
        
        # Get updated status from the mock service
        status_info = mock_payment_service.check_payment_status(payment_reference)
        
        return jsonify({
            'success': True,
            'payment': {
                'id': payment.id,
                'reference': payment.reference,
                'amount': float(payment.amount),
                'status': payment.status,
                'created_at': payment.created_at.isoformat(),
                'updated_at': payment.updated_at.isoformat() if payment.updated_at else None,
                'metadata': payment.payment_metadata or {}
            }
        })
        
    except Exception as e:
        current_app.logger.error(f"Error checking payment status: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Failed to check payment status'
        }), 500

# Admin endpoint to simulate payment webhook (for testing)
@bp.route('/webhook/simulate', methods=['POST'])
@admin_required
def simulate_webhook():
    """
    Simulate a payment webhook (admin only).
    
    Expected JSON payload:
    {
        "reference": "PAY-123456",
        "success": true
    }
    """
    data = request.get_json()
    
    if not data or 'reference' not in data:
        return jsonify({
            'success': False,
            'message': 'Missing required field: reference'
        }), 400
    
    success = data.get('success', True)
    reference = data['reference']
    
    try:
        success, message, payment = mock_payment_service.simulate_payment(reference, success)
        
        if not payment:
            return jsonify({
                'success': False,
                'message': message
            }), 404
            
        return jsonify({
            'success': success,
            'message': message,
            'payment': {
                'id': payment.id,
                'reference': payment.reference,
                'status': payment.status,
                'amount': float(payment.amount),
                'job_id': payment.project_id,
                'metadata': payment.payment_metadata or {}
            }
        })
        
    except Exception as e:
        current_app.logger.error(f"Error in webhook simulation: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error processing webhook: {str(e)}'
        }), 500
