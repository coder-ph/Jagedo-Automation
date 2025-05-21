from flask import request, make_response
from functools import wraps

def init_cors(app):
    """Initialize CORS with default settings."""
    @app.after_request
    def after_request(response):
        """Add CORS headers to all responses."""
        allowed_origins = app.config.get('ALLOWED_ORIGINS', ['*'])
        origin = request.headers.get('Origin', '')
        
        # Check if the origin is in the allowed origins or allow all
        if '*' in allowed_origins or origin in allowed_origins:
            response.headers.add('Access-Control-Allow-Origin', origin or '*')
        
        # Set allowed methods and headers
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 
                           'Content-Type, Authorization, X-Requested-With')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        
        # Handle preflight requests
        if request.method == 'OPTIONS':
            response = make_response()
            response.headers.add('Access-Control-Max-Age', '1728000')  # 20 days
        
        return response

def cors_required(f):
    """Decorator to explicitly mark a route as requiring CORS."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method == 'OPTIONS':
            response = make_response()
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
            response.headers.add('Access-Control-Allow-Headers', 
                              'Content-Type, Authorization, X-Requested-With')
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            response.headers.add('Access-Control-Max-Age', '1728000')
            return response
        return f(*args, **kwargs)
    return decorated_function
