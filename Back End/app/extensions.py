"""
Extensions module to hold Flask extensions to avoid circular imports.
"""
import redis
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_caching import Cache
from flask_cors import CORS
from datetime import timedelta

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()
cache = Cache()
cors = CORS()

# Initialize Redis for token blacklist
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Token blocklist for JWT
jwt_redis_blocklist = redis_client

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    """Check if a JWT exists in the redis blocklist"""
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
