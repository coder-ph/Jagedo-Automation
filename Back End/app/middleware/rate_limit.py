import time
from functools import wraps
from flask import request, jsonify, g
import redis
from .. import redis_client
import logging

class RateLimitExceeded(Exception):
    """Exception raised when rate limit is exceeded."""
    def __init__(self, message, limit, remaining, reset_time):
        self.message = message
        self.limit = limit
        self.remaining = remaining
        self.reset_time = reset_time
        super().__init__(self.message)

def get_remote_address():
    """Get the IP address of the client."""
    # Check for forwarded IP (if behind a proxy)
    if request.headers.getlist("X-Forwarded-For"):
        return request.headers.getlist("X-Forwarded-For")[0]
    return request.remote_addr

def get_rate_limit_key():
    """Generate a rate limit key based on the endpoint and IP address."""
    endpoint = request.endpoint or 'unknown'
    ip = get_remote_address()
    return f"rate_limit:{endpoint}:{ip}"

def get_rate_limit(limit, per):
    """
    Decorator to limit the rate of requests to a specific endpoint.
    
    Args:
        limit: Maximum number of requests allowed in the time window
        per: Time window in seconds
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Skip rate limiting if Redis is not available
            if not redis_client:
                return f(*args, **kwargs)
                
            key = get_rate_limit_key()
            current = redis_client.get(key)
            
            # If the key doesn't exist, set it with an expiration time
            if current is None:
                redis_client.setex(key, per, 1)
                current = 1
            else:
                current = int(current)
                
            # Check if the rate limit has been exceeded
            if current >= limit:
                # Get the time until the rate limit resets
                ttl = redis_client.ttl(key)
                raise RateLimitExceeded(
                    message="Rate limit exceeded. Please try again later.",
                    limit=limit,
                    remaining=0,
                    reset_time=int(time.time()) + ttl
                )
            
            # Increment the counter
            redis_client.incr(key)
            
            # Set the expiration time if this is the first increment in the window
            if current == 0:
                redis_client.expire(key, per)
            
            # Add rate limit headers to the response
            remaining = limit - current - 1
            g.rate_limit = {
                'limit': limit,
                'remaining': max(0, remaining),
                'reset': int(time.time()) + (redis_client.ttl(key) or per)
            }
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def init_rate_limit(app):
    """Initialize rate limiting for the application."""
    logger = logging.getLogger(__name__)
    
    @app.before_request
    def check_rate_limit():
        """Check rate limits for all requests."""
        # Skip rate limiting for certain endpoints
        if request.endpoint in ['static', 'auth.login', 'auth.register', 'health']:
            return
            
        # Get rate limit configuration for the current endpoint
        rate_limits = app.config.get('RATE_LIMITS', {})
        endpoint = request.endpoint or 'default'
        
        # Apply the most specific rate limit that matches the endpoint
        limit_config = None
        for pattern, config in rate_limits.items():
            if endpoint.startswith(pattern):
                limit_config = config
                break
        
        if not limit_config:
            return
            
        limit = limit_config.get('limit', 100)
        per = limit_config.get('per', 60)  # Default: 100 requests per minute
        
        # Apply rate limiting
        key = f"rate_limit:{endpoint}:{get_remote_address()}"
        current = redis_client.get(key)
        
        if current is None:
            redis_client.setex(key, per, 1)
            current = 1
        else:
            current = int(current)
            
        if current >= limit:
            ttl = redis_client.ttl(key)
            response = jsonify({
                'success': False,
                'error': 'Rate limit exceeded. Please try again later.',
                'limit': limit,
                'remaining': 0,
                'reset_in': ttl
            })
            response.headers['X-RateLimit-Limit'] = limit
            response.headers['X-RateLimit-Remaining'] = 0
            response.headers['X-RateLimit-Reset'] = int(time.time()) + ttl
            response.status_code = 429
            return response
            
        redis_client.incr(key)
        
        # Add rate limit headers to the response
        g.rate_limit = {
            'limit': limit,
            'remaining': max(0, limit - current - 1),
            'reset': int(time.time()) + (redis_client.ttl(key) or per)
        }
    
    @app.after_request
    def add_rate_limit_headers(response):
        """Add rate limit headers to all responses."""
        if hasattr(g, 'rate_limit'):
            response.headers['X-RateLimit-Limit'] = g.rate_limit['limit']
            response.headers['X-RateLimit-Remaining'] = g.rate_limit['remaining']
            response.headers['X-RateLimit-Reset'] = g.rate_limit['reset']
        return response
    
    @app.errorhandler(RateLimitExceeded)
    def handle_rate_limit_exceeded(e):
        """Handle rate limit exceeded errors."""
        response = jsonify({
            'success': False,
            'error': str(e),
            'limit': e.limit,
            'remaining': e.remaining,
            'reset_in': e.reset_time - int(time.time())
        })
        response.headers['X-RateLimit-Limit'] = e.limit
        response.headers['X-RateLimit-Remaining'] = e.remaining
        response.headers['X-RateLimit-Reset'] = e.reset_time
        response.status_code = 429
        return response
