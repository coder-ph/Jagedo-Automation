from functools import wraps
from flask import g, request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
from ..models import User, UserRole
import logging

def init_auth_middleware(app):
    """Initialize authentication middleware."""
    logger = logging.getLogger(__name__)
    
    @app.before_request
    def load_logged_in_user():
        """Load user from JWT token if available."""
        g.user = None
        g.user_id = None
        g.roles = []
        
        # Skip authentication for public endpoints
        if request.endpoint in ['auth.login', 'auth.register', 'auth.refresh', 'static']:
            return
            
        try:
            # Check for JWT token in Authorization header
            auth_header = request.headers.get('Authorization', '')
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
                # Verify the token is valid and not expired
                verify_jwt_in_request()
                
                # Get user identity from token
                user_id = get_jwt_identity()
                if user_id:
                    # Get user from database
                    user = User.query.get(user_id)
                    if user:
                        g.user = user
                        g.user_id = user.id
                        g.roles = [user.role.value]
                        
                        # Store additional claims if needed
                        g.jwt_claims = get_jwt()
                        
                        # Update last active timestamp
                        user.update_last_active()
                        
        except Exception as e:
            logger.warning(f"Authentication error: {str(e)}")
            # Don't fail the request here, let the route handle authentication
            pass

def jwt_required_with_roles(roles=None):
    """Decorator to require JWT authentication with specific roles.
    
    Args:
        roles: List of required roles (UserRole enum values)
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Check if user is authenticated
            if not hasattr(g, 'user') or not g.user:
                return jsonify({
                    'success': False,
                    'error': 'Authentication required.'
                }), 401
                
            # Check if user has required role
            if roles:
                user_roles = getattr(g, 'roles', [])
                has_role = any(role in user_roles for role in roles)
                
                if not has_role:
                    return jsonify({
                        'success': False,
                        'error': 'Insufficient permissions.'
                    }), 403
                    
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    """Shortcut decorator for admin-only endpoints."""
    return jwt_required_with_roles([UserRole.ADMIN.value])(f)

def professional_required(f):
    """Shortcut decorator for professional-only endpoints."""
    return jwt_required_with_roles([UserRole.PROFESSIONAL.value, UserRole.ADMIN.value])(f)

def customer_required(f):
    """Shortcut decorator for customer-only endpoints."""
    return jwt_required_with_roles([UserRole.CUSTOMER.value, UserRole.ADMIN.value])(f)

def get_current_user():
    """Get the current authenticated user."""
    return g.get('user')

def get_current_user_id():
    """Get the current authenticated user ID."""
    return g.get('user_id')

def get_jwt_claims():
    """Get the JWT claims for the current request."""
    return g.get('jwt_claims', {})
