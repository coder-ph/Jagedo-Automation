from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError
from ..models import db, PaymentTransaction, Job as Project, User, PaymentStatus, PaymentMethod, UserRole
from ..services.payment_service import payment_service, mpesa_service
from ..utils.decorators import role_required, handle_errors
from datetime import datetime

bp = Blueprint('payment', __name__, url_prefix='/api/payments')

@bp.route('/initiate/mpesa', methods=['POST'])
@jwt_required()
@role_required([UserRole.CUSTOMER, UserRole.ADMIN])
@handle_errors
def initiate_mpesa_payment():
    """
    Initiate M-Pesa payment
    ---
    tags:
      - Payments
    security:
      - JWT: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - phone
            - amount
            - project_id
          properties:
            phone:
              type: string
              description: Customer's phone number (format: 2547XXXXXXXX)
            amount:
              type: number
              description: Amount to be paid
            project_id:
              type: integer
              description: ID of the project being paid for (optional)
            description:
              type: string
              description: Payment description (optional)
    responses:
      200:
        description: Payment initiated successfully
      400:
        description: Invalid input data
      500:
        description: Internal server error
    """
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['phone', 'amount']
    for field in required_fields:
        if field not in data:
            return jsonify({'success': False, 'message': f'Missing required field: {field}'}), 400
    
    try:
        user_id = get_jwt_identity()
        phone = data['phone']
        amount = float(data['amount'])
        project_id = data.get('project_id')
        description = data.get('description', 'Payment')
        
        # Validate project exists if project_id is provided
        if project_id:
            project = Project.query.get(project_id)
            if not project:
                return jsonify({'success': False, 'message': 'Project not found'}), 404
        
        # Initiate payment
        result = payment_service.initiate_mpesa_payment(
            user_id=user_id,
            phone=phone,
            amount=amount,
            project_id=project_id,
            description=description
        )
        
        return jsonify(result), 200
        
    except ValueError as e:
        return jsonify({'success': False, 'message': 'Invalid amount'}), 400
    except Exception as e:
        current_app.logger.error(f"Error initiating M-Pesa payment: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

@bp.route('/mpesa/callback', methods=['POST'])
def mpesa_callback():
    """
    M-Pesa payment callback
    ---
    tags:
      - Payments (Webhooks)
    parameters:
      - in: body
        name: body
        required: true
        description: M-Pesa callback data
    responses:
      200:
        description: Callback processed successfully
      400:
        description: Invalid callback data
      500:
        description: Internal server error
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'status': 'error', 'message': 'No data provided'}), 400
            
        # Process the callback
        return payment_service.handle_mpesa_callback(data)
        
    except Exception as e:
        current_app.logger.error(f"Error processing M-Pesa callback: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Internal server error'}), 500

@bp.route('/transactions', methods=['GET'])
@jwt_required()
@handle_errors
def get_transactions():
    """
    Get user's payment transactions
    ---
    tags:
      - Payments
    security:
      - JWT: []
    parameters:
      - in: query
        name: status
        type: string
        enum: [pending, completed, failed, cancelled]
        description: Filter by status
      - in: query
        name: method
        type: string
        enum: [mpesa, card, bank_transfer]
        description: Filter by payment method
      - in: query
        name: project_id
        type: integer
        description: Filter by project ID
      - in: query
        name: limit
        type: integer
        default: 10
        description: Number of transactions to return
      - in: query
        name: page
        type: integer
        default: 1
        description: Page number
    responses:
      200:
        description: List of payment transactions
      500:
        description: Internal server error
    """
    try:
        user_id = get_jwt_identity()
        status = request.args.get('status')
        method = request.args.get('method')
        project_id = request.args.get('project_id', type=int)
        limit = min(int(request.args.get('limit', 10)), 100)
        page = max(int(request.args.get('page', 1)), 1)
        
        # Build query
        query = PaymentTransaction.query.filter_by(user_id=user_id)
        
        # Apply filters
        if status:
            query = query.filter_by(status=PaymentStatus(status))
        if method:
            query = query.filter_by(method=PaymentMethod(method))
        if project_id:
            query = query.filter_by(project_id=project_id)
        
        # Paginate results
        pagination = query.order_by(PaymentTransaction.created_at.desc()).paginate(
            page=page, per_page=limit, error_out=False
        )
        
        # Prepare response
        transactions = [txn.to_dict() for txn in pagination.items]
        
        return jsonify({
            'success': True,
            'transactions': transactions,
            'pagination': {
                'total': pagination.total,
                'pages': pagination.pages,
                'current_page': page,
                'per_page': limit,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }), 200
        
    except ValueError as e:
        return jsonify({'success': False, 'message': 'Invalid filter value'}), 400
    except Exception as e:
        current_app.logger.error(f"Error fetching transactions: {str(e)}")
        return jsonify({'success': False, 'message': 'Failed to fetch transactions'}), 500

@bp.route('/transactions/<int:transaction_id>', methods=['GET'])
@jwt_required()
@handle_errors
def get_transaction(transaction_id):
    """
    Get payment transaction details
    ---
    tags:
      - Payments
    security:
      - JWT: []
    parameters:
      - in: path
        name: transaction_id
        type: integer
        required: true
        description: Transaction ID
    responses:
      200:
        description: Transaction details
      404:
        description: Transaction not found
      500:
        description: Internal server error
    """
    try:
        user_id = get_jwt_identity()
        
        transaction = PaymentTransaction.query.filter_by(
            id=transaction_id,
            user_id=user_id
        ).first()
        
        if not transaction:
            return jsonify({'success': False, 'message': 'Transaction not found'}), 404
        
        return jsonify({
            'success': True,
            'transaction': transaction.to_dict()
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error fetching transaction {transaction_id}: {str(e)}")
        return jsonify({'success': False, 'message': 'Failed to fetch transaction'}), 500

@bp.route('/verify', methods=['POST'])
@jwt_required()
@role_required([UserRole.ADMIN])
@handle_errors
def verify_payment():
    """
    Verify a payment (Admin only)
    ---
    tags:
      - Payments (Admin)
    security:
      - JWT: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - transaction_id
            - status
          properties:
            transaction_id:
              type: integer
              description: Transaction ID
            status:
              type: string
              enum: [completed, failed, cancelled]
              description: New status
            notes:
              type: string
              description: Optional notes
    responses:
      200:
        description: Payment verified successfully
      400:
        description: Invalid input data
      404:
        description: Transaction not found
      500:
        description: Internal server error
    """
    data = request.get_json()
    
    try:
        transaction_id = data.get('transaction_id')
        status = data.get('status')
        notes = data.get('notes')
        
        if not transaction_id or not status:
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        
        # Get transaction
        transaction = PaymentTransaction.query.get(transaction_id)
        if not transaction:
            return jsonify({'success': False, 'message': 'Transaction not found'}), 404
        
        # Update status
        transaction.status = PaymentStatus(status)
        if notes:
            if 'admin_notes' not in transaction.metadata:
                transaction.metadata['admin_notes'] = []
            transaction.metadata['admin_notes'].append({
                'timestamp': datetime.utcnow().isoformat(),
                'status': status,
                'notes': notes
            })
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Payment verified successfully',
            'transaction': transaction.to_dict()
        }), 200
        
    except ValueError as e:
        return jsonify({'success': False, 'message': 'Invalid status value'}), 400
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error verifying payment: {str(e)}")
        return jsonify({'success': False, 'message': 'Failed to verify payment'}), 500
