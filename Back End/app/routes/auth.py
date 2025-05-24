from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, get_jwt, get_jwt_header,
    verify_jwt_in_request, decode_token
)
from werkzeug.security import generate_password_hash, check_password_hash
import re
from datetime import datetime, timedelta
from functools import wraps

from ..models import db, User, UserRole
from ..extensions import jwt
from ..utils.decorators import role_required
from ..utils.validators import validate_email, validate_password

# Create auth blueprint
auth_bp = Blueprint('auth', __name__)

def format_response(data=None, message='', status='success', status_code=200):
    """Format API response."""
    response = {
        'status': status,
        'message': message,
        'data': data
    }
    return jsonify(response), status_code

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No input data provided',
                'data': {'errors': {'general': 'No input data provided'}}
            }), 400
        
        # Validate required fields
        required_fields = ['name', 'email', 'password', 'role', 'location']
        errors = {}
        for field in required_fields:
            if field not in data or not data[field]:
                errors[field] = f'{field.replace("_", " ").title()} is required.'
        
        if errors:
            return jsonify({
                'status': 'error',
                'message': 'Validation failed',
                'data': {'errors': errors}
            }), 400
        
        # Validate role
        try:
            role = UserRole(data['role'].lower())
        except ValueError:
            return jsonify({
                'status': 'error',
                'message': 'Validation failed',
                'data': {'errors': {'role': 'Invalid role. Must be one of: customer, professional, admin'}}
            }), 400
        
        # Validate email
        if not validate_email(data['email']):
            return jsonify({
                'status': 'error',
                'message': 'Validation failed',
                'data': {'errors': {'email': 'Invalid email format.'}}
            }), 400
        
        # Validate password strength
        if not validate_password(data['password']):
            return jsonify({
                'status': 'error',
                'message': 'Validation failed',
                'data': {
                    'errors': {'password': 'Password must be at least 8 characters long and include uppercase, lowercase, digit, and special character.'}
                }
            }), 400
        
        # Check if email already exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({
                'status': 'error',
                'message': 'Registration failed',
                'data': {'errors': {'email': 'Email already registered.'}}
            }), 409
        
        # Create new user
        try:
            user = User(
                name=data['name'],
                email=data['email'],
                role=role,
                location=data['location'],
                company_name=data.get('company_name', ''),
                phone=data.get('phone', ''),
                is_verified=True  # Auto-verify for testing
            )
            user.password = data['password']  # This will hash the password using the property setter
            
            db.session.add(user)
            db.session.commit()
            
            # Generate tokens
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)
            
            return jsonify({
                'status': 'success',
                'message': 'User registered successfully',
                'data': {
                    'user': user.to_dict(),
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }
            }), 201
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'User creation error: {str(e)}', exc_info=True)
            return jsonify({
                'status': 'error',
                'message': 'Failed to create user',
                'data': {'error': str(e)}
            }), 500
            
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Registration error: {str(e)}', exc_info=True)
        return jsonify({
            'status': 'error',
            'message': 'Registration failed',
            'data': {'error': str(e)}
        }), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Authenticate user and return tokens."""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'email' not in data or 'password' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Login failed',
                'data': {'errors': {'auth': 'Email and password are required'}}
            }), 400
            
        email = data['email'].strip().lower()
        password = data['password']
        
        # Basic email validation
        if not email or '@' not in email:
            return jsonify({
                'status': 'error',
                'message': 'Login failed',
                'data': {'errors': {'email': 'Invalid email format'}}
            }), 400
            
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.verify_password(password):
            return jsonify({
                'status': 'error',
                'message': 'Login failed',
                'data': {'errors': {'auth': 'Invalid email or password'}}
            }), 401
            
        # Check if user is active
        if not user.is_active:
            return jsonify({
                'status': 'error',
                'message': 'Account deactivated',
                'data': {'errors': {'account': 'This account has been deactivated'}}
            }), 403
        
        # Generate tokens
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        
        return jsonify({
            'status': 'success',
            'message': 'Login successful',
            'data': {
                'user': user.to_dict(),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f'Login error: {str(e)}', exc_info=True)
        return jsonify({
            'status': 'error',
            'message': 'An error occurred during login',
            'data': {'errors': {'auth': 'Failed to process login'}}
        }), 500

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current user's profile."""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({
                'status': 'error',
                'message': 'User not found',
                'data': None
            }), 404
            
        return jsonify({
            'status': 'success',
            'message': 'User profile retrieved successfully',
            'data': user.to_dict()
        }), 200
        
    except Exception as e:
        current_app.logger.error(f'Error getting current user: {str(e)}', exc_info=True)
        return jsonify({
            'status': 'error',
            'message': 'An error occurred while retrieving user profile',
            'data': {'error': str(e)}
        }), 500

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token using refresh token."""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({
                'status': 'error',
                'message': 'User not found',
                'data': None
            }), 404
            
        # Create new tokens
        access_token = create_access_token(identity=current_user_id)
        refresh_token = create_refresh_token(identity=current_user_id)
        
        return jsonify({
            'status': 'success',
            'message': 'Token refreshed successfully',
            'data': {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': user.to_dict()
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f'Refresh token error: {str(e)}', exc_info=True)
        return jsonify({
            'status': 'error',
            'message': 'Failed to refresh token. Please try again.',
            'data': {'error': str(e)}
        }), 500

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Log out the current user."""
    try:
        jti = get_jwt()['jti']
        
        # Add the token to the blocklist with an expiration time (24 hours from now)
        expires_delta = timedelta(hours=24)
        
        from app.extensions import redis_client
        redis_client.set(f'jwt_blocklist:{jti}', 'true', ex=expires_delta)
        
        return jsonify({
            'status': 'success',
            'message': 'Successfully logged out',
            'data': None
        }), 200
        
    except Exception as e:
        current_app.logger.error(f'Logout error: {str(e)}', exc_info=True)
        return jsonify({
            'status': 'error',
            'message': 'An error occurred during logout',
            'data': {'error': str(e)}
        }), 500

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user's profile."""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({
                'status': 'error',
                'message': 'User not found',
                'data': None
            }), 404
            
        return jsonify({
            'status': 'success',
            'message': 'Profile retrieved successfully',
            'data': user.to_dict()
        }), 200
        
    except Exception as e:
        current_app.logger.error(f'Error getting profile: {str(e)}', exc_info=True)
        return jsonify({
            'status': 'error',
            'message': 'Failed to retrieve profile',
            'data': {'error': str(e)}
        }), 500

@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update current user's profile."""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({
                'status': 'error',
                'message': 'User not found',
                'data': None
            }), 404
            
        data = request.get_json()
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No data provided',
                'data': None
            }), 400
        
        # Update allowed fields
        allowed_fields = ['name', 'company_name', 'profile_description', 'location', 'phone']
        updates = {}
        for field in allowed_fields:
            if field in data:
                setattr(user, field, data[field])
                updates[field] = data[field]
        
        if not updates:
            return jsonify({
                'status': 'error',
                'message': 'No valid fields to update',
                'data': None
            }), 400
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Profile updated successfully',
            'data': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Profile update error: {str(e)}', exc_info=True)
        return jsonify({
            'status': 'error',
            'message': 'Failed to update profile',
            'data': {'error': str(e)}
        }), 500

@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """Change user's password."""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({
                'status': 'error',
                'message': 'User not found',
                'data': None
            }), 404
            
        data = request.get_json()
        
        # Validate required fields
        if not data or 'current_password' not in data or 'new_password' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Validation failed',
                'data': {'errors': {'password': 'Current and new password are required'}}
            }), 400
            
        # Verify current password
        if not user.verify_password(data['current_password']):
            return jsonify({
                'status': 'error',
                'message': 'Password change failed',
                'data': {'errors': {'current_password': 'Current password is incorrect'}}
            }), 400
            
        # Update password
        user.password = data['new_password']
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Password updated successfully',
            'data': None
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error changing password: {str(e)}', exc_info=True)
        return jsonify({
            'status': 'error',
            'message': 'An error occurred while changing password',
            'data': {'error': str(e)}
        }), 500
