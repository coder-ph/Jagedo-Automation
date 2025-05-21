from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from ..extensions import db
from ..models import User, UserRole

def role_required(roles):
    """
    Decorator to check if the user has the required role(s).
    
    Args:
        roles: A single role (string) or list of roles that are allowed to access the endpoint
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            verify_jwt_in_request()
            current_user_id = get_jwt_identity()
            user = db.session.get(User, current_user_id)
            
            if not user:
                return jsonify({
                    'success': False,
                    'error': 'User not found.'
                }), 404
                
            # Convert single role to list for uniform handling
            if isinstance(roles, str):
                required_roles = [roles]
            else:
                required_roles = roles
                
            # Check if user has any of the required roles
            if user.role not in required_roles:
                return jsonify({
                    'success': False,
                    'error': 'Insufficient permissions.'
                }), 403
                
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def validate_json_content_type(f):
    """
    Decorator to check if the request has JSON content type.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': 'Content-Type must be application/json.'
            }), 400
        return f(*args, **kwargs)
    return decorated_function

def validate_required_fields(required_fields):
    """
    Decorator to validate that required fields are present in the request.
    
    Args:
        required_fields: List of required field names
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = request.get_json()
            missing_fields = [field for field in required_fields if field not in data or data[field] is None]
            
            if missing_fields:
                return jsonify({
                    'success': False,
                    'error': 'Missing required fields.',
                    'missing_fields': missing_fields
                }), 400
                
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    """Shortcut decorator for admin-only endpoints."""
    return role_required(UserRole.ADMIN)(f)

def professional_required(f):
    """Shortcut decorator for professional-only endpoints."""
    return role_required([UserRole.PROFESSIONAL, UserRole.ADMIN])(f)

def customer_required(f):
    """Shortcut decorator for customer-only endpoints."""
    return role_required([UserRole.CUSTOMER, UserRole.ADMIN])(f)

def handle_errors(f):
    """
    Decorator to handle common exceptions and return appropriate JSON responses.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as e:
            return jsonify({
                'success': False,
                'error': str(e) or 'Invalid value provided.'
            }), 400
        except Exception as e:
            current_app.logger.error(f'Unexpected error in {f.__name__}: {str(e)}')
            return jsonify({
                'success': False,
                'error': 'An unexpected error occurred. Please try again.'
            }), 500
    return decorated_function
