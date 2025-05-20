from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_cors import CORS
from datetime import datetime
from models import db, User, UserRole, BidStatus, JobStatus, Message
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import HTTPException
import os
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    JWTManager, create_access_token,
    jwt_required, get_jwt_identity
)
from datetime import timedelta
from functools import wraps

load_dotenv()

app = Flask(__name__)

DATABASE_URL =os.getenv("DATABASE_URL") or \
               'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app.db')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback-secret-key')
app.config['JSON_SORT_KEYS'] = False
app.config['JWT_SECRET_KEY'] = app.config['SECRET_KEY']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=7)

# Mpesa configs
MPESA_CONSUMER_KEY = os.getenv('MPESA_CONSUMER_KEY')
MPESA_CONSUMER_SECRET = os.getenv('MPESA_CONSUMER_SECRET')
MPESA_PASSKEY = os.getenv('MPESA_PASSKEY')
MPESA_SHORTCODE = os.getenv('MPESA_SHORTCODE')
MPESA_CALLBACK_URL = os.getenv('MPESA_CALLBACK_URL')
MPESA_AUTH_TOKEN = None
MPESA_AUTH_TOKEN_EXPIRY = None

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
CORS(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

def get_current_user():
    current_user_id = get_jwt_identity()
    return User.query.get(int(current_user_id))

# Helper functions. validation functions unused as of now.. not handling registration on api
def validate_email(email):
    import re
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(pattern, email):
        raise ValueError('Invalid email format')

def validate_phone(phone):
    import re
    # +2xx, 07xx, 01xx
    pattern = r'^(?:\+2\d{7,14}|0(7\d{8}|1\d{8}))$'
    if not re.match(pattern, phone):
        raise ValueError('Invalid phone number format')

def validate_json():
    if not request.is_json:
        raise ValueError('Content-Type must be application/json')
    return request.get_json()

def validate_required_fields(data, required_fields):
    missing = [field for field in required_fields if field not in data]
    if missing:
        raise ValueError(f'Missing required fields: {", ".join(missing)}')
    
    # location filtering
    def get_location_hierarchy(location):
        """
        Convert a location string into hierarchical components (county, subcounty, ward, etc.)
        This is a simplified version - you'll need to adapt this based on your actual location structure
        """
        # This is a placeholder - implement actual location parsing logic
        parts = location.lower().split(',')
        parts = [p.strip() for p in parts]
        return {
            'full': location,
            'county': parts[-1] if len(parts) > 0 else None,
            'subcounty': parts[-2] if len(parts) > 1 else None,
            'ward': parts[-3] if len(parts) > 2 else None
        }
    
    def location_match_score(client_location, contractor_location):
        """
        Calculate a match score between client and contractor locations
        Higher score means better match
        """
        client = get_location_hierarchy(client_location)
        contractor = get_location_hierarchy(contractor_location)
        
        if client['full'] == contractor['full']:
            return 3  
        elif client['ward'] and client['ward'] == contractor.get('ward'):
            return 2  
        elif client['subcounty'] and client['subcounty'] == contractor.get('subcounty'):
            return 1  
        elif client['county'] and client['county'] == contractor.get('county'):
            return 0.5  
        return 0  

# auth helper

def role_required(roles):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            current_user = get_current_user()
            if not current_user:
                return jsonify({
                    'success': False,
                    'message': 'User not found',
                    'data': None
                }), 404
            
            if current_user.role not in roles:
                return jsonify({
                    'success': False,
                    'message': 'Insufficient permissions',
                    'data': None
                }), 403
            
            return fn(*args, **kwargs)
        return wrapper
    return decorator


# routes
@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = validate_json()
        validate_required_fields(data, ['email', 'password'])
    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e),
            'data': None
        }), 400

    user = User.query.filter_by(email=data['email']).first()
    if not user or not bcrypt.check_password_hash(user.password_hash, data['password']):
        return jsonify({
            'success': False,
            'message': 'Invalid credentials',
            'data': None
        }), 401

    access_token = create_access_token(identity=str(user.id))
    return jsonify({
        'success': True,
        'message': 'Login successful',
        'data': {
            'access_token': access_token
        }
    }), 200


@app.route('/api/profile', methods=['GET'])
@jwt_required()
def get_profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({
            'success': False,
            'message': 'User not found',
            'data': None
        }), 404

    return jsonify({
        'success': True,
        'message': 'Profile retrieved successfully',
        'data': user.to_dict()
    })

# Admin only routes
@app.route('/api/admin/dashboard', methods=['GET'])
@role_required([UserRole.ADMIN])
def admin_dashboard():
    return jsonify({
        'success': True,
        'message': 'Admin dashboard accessed successfully',
        'data': {
            'total_users': User.query.count(),
            'total_professionals': User.query.filter_by(role=UserRole.PROFESSIONAL).count(),
            'total_customers': User.query.filter_by(role=UserRole.CUSTOMER).count()
        }
    })

# Professional only routes
@app.route('/api/professional/dashboard', methods=['GET'])
@role_required([UserRole.PROFESSIONAL])
def professional_dashboard():
    current_user = get_current_user()
    return jsonify({
        'success': True,
        'message': 'Professional dashboard accessed successfully',
        'data': {
            'total_bids': len(current_user.bids),
            'active_jobs': len([bid for bid in current_user.bids if bid.status == BidStatus.ACCEPTED])
        }
    })

# Customer only routes
@app.route('/api/customer/dashboard', methods=['GET'])
@role_required([UserRole.CUSTOMER])
def customer_dashboard():
    current_user = get_current_user()
    return jsonify({
        'success': True,
        'message': 'Customer dashboard accessed successfully',
        'data': {
            'total_jobs': len(current_user.jobs),
            'active_jobs': len([job for job in current_user.jobs if job.status == JobStatus.IN_PROGRESS])
        }
    })

def role_required(roles):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            current_user = get_current_user()
            if not current_user:
                return jsonify({
                    'success': False,
                    'message': 'User not found',
                    'data': None
                }), 404
            
            if current_user.role not in roles:
                return jsonify({
                    'success': False,
                    'message': 'Insufficient permissions',
                    'data': None
                }), 403
            
            return fn(*args, **kwargs)
        return wrapper
    return decorator

# Test Routes
@app.route('/api/test', methods=['POST', 'GET'])
def test():
    if request.method == 'POST':
        data = request.get_json() or {}
        return jsonify({
            'success': True,
            'message': 'POST request successful',
            'received_data': data,
            'timestamp': datetime.now().isoformat()
        })
    elif request.method == 'GET':
        return jsonify({
            'success': True,
            'message': 'GET request successful',
            'timestamp': datetime.now().isoformat()
        })


@app.errorhandler(HTTPException)
def handle_http_error(e):
    return jsonify({
        'success': False,
        'error': e.name,
        'message': e.description
    }), e.code

@app.errorhandler(SQLAlchemyError)
def handle_db_error(e):
    db.session.rollback()
    return jsonify({
        'success': False,
        'error': 'Db error',
        'message': str(e)
    }), 500

@app.errorhandler(Exception)
def handle_unexpected_error(e):
    return jsonify({
        'success': False,
        'error': 'Unexpected error',
        'message': str(e)
    }), 500

@app.route('/api/health')
def health_check():
    return jsonify({
        'success': True,
        'message': 'healthy api',
    })

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG', False))