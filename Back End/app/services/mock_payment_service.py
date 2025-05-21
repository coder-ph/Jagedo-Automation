import uuid
from datetime import datetime, timedelta
from flask import current_app
from sqlalchemy.exc import SQLAlchemyError
from ..models import db, PaymentTransaction, PaymentStatus, Job, JobStatus
from ..utils.helpers import generate_reference

class MockPaymentService:
    """Mock payment service for simulating M-Pesa payments during development and testing."""
    
    def __init__(self, app=None):
        """Initialize the mock payment service."""
        self.app = app
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize with Flask app context."""
        self.app = app
    
    def create_payment_record(self, user_id, amount, job_id=None, method='mpesa', description=''):
        """
        Create a payment record in the database.
        
        Args:
            user_id: ID of the user making the payment
            amount: Payment amount
            job_id: Optional associated job ID
            method: Payment method (default: 'mpesa')
            description: Payment description
            
        Returns:
            PaymentTransaction: The created payment record
        """
        try:
            # Generate a unique reference
            reference = f"MOCK-{generate_reference()}"
            
            # Create the payment record
            payment = PaymentTransaction(
                user_id=user_id,
                project_id=job_id,
                amount=amount,
                status=PaymentStatus.PENDING,
                method=method,
                reference=reference,
                payment_metadata={
                    'description': description,
                    'created_at': datetime.utcnow().isoformat(),
                    'simulated': True
                }
            )
            
            db.session.add(payment)
            db.session.commit()
            
            current_app.logger.info(f"Created mock payment record: {reference}")
            return payment
            
        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error(f"Failed to create mock payment record: {str(e)}")
            raise Exception("Failed to create payment record")
    
    def simulate_payment(self, payment_reference, success=True):
        """
        Simulate a payment response.
        
        Args:
            payment_reference: The payment reference to simulate
            success: Whether the payment should succeed (default: True)
            
        Returns:
            tuple: (success: bool, message: str, payment: PaymentTransaction)
        """
        try:
            # Find the payment record
            payment = PaymentTransaction.query.filter_by(reference=payment_reference).first()
            if not payment:
                return False, "Payment not found", None
                
            if payment.status != PaymentStatus.PENDING:
                return False, f"Payment is already {payment.status}", payment
            
            # Update payment status based on simulation result
            if success:
                payment.status = PaymentStatus.COMPLETED
                payment.payment_metadata['paid_at'] = datetime.utcnow().isoformat()
                payment.payment_metadata['mpesa_receipt'] = f"MPE{generate_reference()}"
                
                # Update associated job if exists
                if payment.project_id:
                    job = Job.query.get(payment.project_id)
                    if job:
                        job.mark_as_paid()
                        current_app.logger.info(f"Marked job {job.id} as paid")
                
                message = "Payment simulated successfully"
            else:
                payment.status = PaymentStatus.FAILED
                payment.payment_metadata['failed_at'] = datetime.utcnow().isoformat()
                message = "Payment simulation failed"
            
            payment.updated_at = datetime.utcnow()
            db.session.commit()
            
            return success, message, payment
            
        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error(f"Error simulating payment: {str(e)}")
            return False, "Error processing payment simulation", None
    
    def check_payment_status(self, payment_reference):
        """
        Check the status of a payment.
        
        Args:
            payment_reference: The payment reference to check
            
        Returns:
            dict: Payment status information
        """
        payment = PaymentTransaction.query.filter_by(reference=payment_reference).first()
        if not payment:
            return {
                'success': False,
                'message': 'Payment not found',
                'status': 'not_found'
            }
        
        return {
            'success': True,
            'status': payment.status,
            'reference': payment.reference,
            'amount': float(payment.amount),
            'currency': payment.currency,
            'metadata': payment.payment_metadata or {}
        }

# Create a singleton instance
mock_payment_service = MockPaymentService()
