"""
Extensions module to hold Flask extensions to avoid circular imports.
"""
import redis
from flask import jsonify, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_caching import Cache
from flask_cors import CORS
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()
cache = Cache()
cors = CORS()

def init_redis(app):
    """Initialize Redis connection with proper error handling"""
    global redis_client, jwt_redis_blocklist
    
    redis_url = app.config.get('REDIS_URL')
    if not redis_url:
        logger.warning("No REDIS_URL configured, Redis features will be disabled")
        redis_client = None
        jwt_redis_blocklist = None
        return

    try:
        redis_client = redis.Redis.from_url(redis_url, decode_responses=True)
        # Test the connection
        redis_client.ping()
        logger.info("Successfully connected to Redis")
        jwt_redis_blocklist = redis_client
    except (redis.RedisError, ConnectionError) as e:
        logger.warning(f"Failed to connect to Redis: {str(e)}. Redis features will be disabled")
        redis_client = None
        jwt_redis_blocklist = None

# Initialize Redis as None initially
redis_client = None
jwt_redis_blocklist = None

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    """Check if a JWT exists in the redis blocklist"""
    if not current_app.config.get('JWT_BLOCKLIST_ENABLED', True):
        return False
    if not jwt_redis_blocklist:
        return False
    jti = jwt_payload["jti"]
    # Use the same key structure as in the logout route
    token_in_redis = jwt_redis_blocklist.get(f'jwt_blocklist:{jti}')
    return token_in_redis is not None

@jwt.revoked_token_loader
def handle_revoked_token(jwt_header, jwt_payload):
    """Custom response for revoked tokens"""
    return jsonify({
        'status': 'error',
        'message': 'Token has been revoked',
        'error': 'token_revoked'
    }), 401
