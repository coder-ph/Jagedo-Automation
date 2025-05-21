import os
import base64
import hashlib
import hmac
import json
import requests
from datetime import datetime, timedelta
from flask import current_app, jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from ..models import db, PaymentTransaction, PaymentStatus, PaymentMethod, Job, User
from ..utils.helpers import generate_reference

class MpesaService:
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        self.app = app
        self.consumer_key = app.config.get('MPESA_CONSUMER_KEY')
        self.consumer_secret = app.config.get('MPESA_CONSUMER_SECRET')
        self.passkey = app.config.get('MPESA_PASSKEY')
        self.shortcode = app.config.get('MPESA_SHORTCODE')
        self.callback_url = app.config.get('MPESA_CALLBACK_URL')
        self.env = app.config.get('MPESA_ENV', 'sandbox')
        self.auth_token = None
        self.auth_token_expiry = None
        
        # Set base URLs based on environment
        if self.env == 'production':
            self.base_url = 'https://api.safaricom.co.ke'
        else:
            self.base_url = 'https://sandbox.safaricom.co.ke'
    
    def get_auth_token(self):
        """Get or refresh M-Pesa OAuth token"""
        if self.auth_token and datetime.utcnow() < self.auth_token_expiry:
            return self.auth_token
        
        auth = base64.b64encode(f"{self.consumer_key}:{self.consumer_secret}".encode()).decode()
        headers = {'Authorization': f'Basic {auth}'}
        
        try:
            response = requests.get(
                f"{self.base_url}/oauth/v1/generate?grant_type=client_credentials",
                headers=headers
            )
            response.raise_for_status()
            
            data = response.json()
            self.auth_token = data['access_token']
            # Set expiry 5 minutes before actual expiry to be safe
            self.auth_token_expiry = datetime.utcnow() + timedelta(seconds=data['expires_in'] - 300)
            return self.auth_token
            
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"Failed to get M-Pesa auth token: {str(e)}")
            raise Exception("Failed to authenticate with M-Pesa service")
    
    def initiate_stk_push(self, phone, amount, account_reference, description):
        """Initiate STK push to customer's phone"""
        try:
            token = self.get_auth_token()
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            password = base64.b64encode(
                f"{self.shortcode}{self.passkey}{timestamp}".encode()
            ).decode()
            
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            
            # Format phone number (strip + and leading 0 if present)
            phone = phone.lstrip('+').lstrip('0')
            if not phone.startswith('254'):
                phone = f'254{phone}'
            
            payload = {
                'BusinessShortCode': self.shortcode,
                'Password': password,
                'Timestamp': timestamp,
                'TransactionType': 'CustomerPayBillOnline',
                'Amount': amount,
                'PartyA': phone,
                'PartyB': self.shortcode,
                'PhoneNumber': phone,
                'CallBackURL': self.callback_url,
                'AccountReference': account_reference[:12],  # Max 12 chars
                'TransactionDesc': description[:13]  # Max 13 chars
            }
            
            response = requests.post(
                f"{self.base_url}/mpesa/stkpush/v1/processrequest",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"STK push failed: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                current_app.logger.error(f"Response: {e.response.text}")
            raise Exception("Failed to initiate M-Pesa payment")
    
    def validate_webhook_signature(self, request_data, signature):
        """Validate M-Pesa webhook signature"""
        # Get the passkey from config
        passkey = self.passkey
        
        # Sort the request data and create a signature string
        sorted_data = dict(sorted(request_data.items()))
        signature_string = ''.join(f"{key}{value}" for key, value in sorted_data.items())
        
        # Generate HMAC-SHA256 hash
        hmac_obj = hmac.new(
            passkey.encode('utf-8'),
            signature_string.encode('utf-8'),
            hashlib.sha256
        )
        
        generated_signature = hmac_obj.hexdigest()
        
        # Compare signatures
        return hmac.compare_digest(generated_signature, signature)


class PaymentService:
    def __init__(self, mpesa_service=None):
        self.mpesa = mpesa_service or MpesaService(current_app)
    
    def create_payment_transaction(self, user_id, amount, method, project_id=None, **kwargs):
        """Create a new payment transaction"""
        try:
            # Generate a unique reference
            reference = generate_reference('PAY')
            
            transaction = PaymentTransaction(
                user_id=user_id,
                project_id=project_id,
                amount=amount,
                method=method,
                reference=reference,
                status=PaymentStatus.PENDING,
                metadata=kwargs.get('metadata', {})
            )
            
            db.session.add(transaction)
            db.session.commit()
            
            return transaction
            
        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error(f"Failed to create payment transaction: {str(e)}")
            raise Exception("Failed to create payment transaction")
    
    def initiate_mpesa_payment(self, user_id, phone, amount, project_id=None, description="Payment"):
        """Initiate M-Pesa payment"""
        try:
            # Create payment transaction
            transaction = self.create_payment_transaction(
                user_id=user_id,
                amount=amount,
                method=PaymentMethod.MPESA,
                project_id=project_id,
                payment_metadata={
                    'phone': phone,
                    'description': description
                }
            )
            
            # Initiate STK push
            response = self.mpesa.initiate_stk_push(
                phone=phone,
                amount=amount,
                account_reference=transaction.reference,
                description=description
            )
            
            # Update transaction with M-Pesa response
            if response.get('ResponseCode') == '0':
                transaction.payment_metadata.update({
                    'mpesa_request': response,
                    'checkout_request_id': response.get('CheckoutRequestID')
                })
                db.session.commit()
                
                return {
                    'success': True,
                    'message': 'Payment initiated successfully',
                    'transaction': transaction.to_dict(),
                    'mpesa_response': response
                }
            else:
                raise Exception(response.get('errorMessage', 'Failed to initiate payment'))
                
        except Exception as e:
            # Update transaction status on error
            if 'transaction' in locals():
                try:
                    transaction.status = PaymentStatus.FAILED
                    transaction.payment_metadata['error'] = str(e)
                    db.session.commit()
                except:
                    db.session.rollback()
            
            current_app.logger.error(f"Payment initiation failed: {str(e)}")
            raise Exception(f"Payment initiation failed: {str(e)}")
    
    def handle_mpesa_callback(self, data):
        """Handle M-Pesa payment callback"""
        try:
            # Verify the callback signature
            signature = request.headers.get('X-Mpesa-Signature')
            if not signature or not self.mpesa.validate_webhook_signature(data, signature):
                current_app.logger.warning("Invalid M-Pesa callback signature")
                return jsonify({'status': 'error', 'message': 'Invalid signature'}), 400
            
            # Extract transaction details
            result_code = data.get('Body', {}).get('stkCallback', {}).get('ResultCode')
            result_desc = data.get('Body', {}).get('stkCallback', {}).get('ResultDesc')
            checkout_request_id = data.get('Body', {}).get('stkCallback', {}).get('CheckoutRequestID')
            
            # Find the transaction by checkout request ID
            transaction = PaymentTransaction.query.filter_by(
                payment_metadata['checkout_request_id'].astext == checkout_request_id
            ).first()
            
            if not transaction:
                current_app.logger.warning(f"Transaction not found for checkout ID: {checkout_request_id}")
                return jsonify({'status': 'error', 'message': 'Transaction not found'}), 404
            
            # Process the callback
            if result_code == '0':
                # Payment was successful
                metadata = data.get('Body', {}).get('stkCallback', {}).get('CallbackMetadata', {}).get('Item', [])
                
                # Extract payment details
                payment_data = {}
                for item in metadata:
                    if 'Name' in item and 'Value' in item:
                        payment_data[item['Name']] = item['Value']
                
                # Update transaction
                transaction.status = PaymentStatus.COMPLETED
                transaction.mpesa_receipt = payment_data.get('MpesaReceiptNumber')
                transaction.phone_number = payment_data.get('PhoneNumber')
                transaction.payment_metadata.update({
                    'mpesa_callback': data,
                    'payment_data': payment_data
                })
                
                # Update related project if exists
                if transaction.project_id:
                    project = Project.query.get(transaction.project_id)
                    if project:
                        project.payment_status = 'paid'
                        db.session.add(project)
                
                db.session.commit()
                
                # TODO: Send payment confirmation email/notification
                
                return jsonify({'status': 'success'}), 200
                
            else:
                # Payment failed
                transaction.status = PaymentStatus.FAILED
                transaction.payment_metadata.update({
                    'mpesa_callback': data,
                    'error': result_desc
                })
                db.session.commit()
                
                return jsonify({'status': 'error', 'message': result_desc}), 400
                
        except Exception as e:
            current_app.logger.error(f"Error processing M-Pesa callback: {str(e)}")
            return jsonify({'status': 'error', 'message': 'Internal server error'}), 500


# Initialize payment service
mpesa_service = MpesaService()
payment_service = PaymentService(mpesa_service)
