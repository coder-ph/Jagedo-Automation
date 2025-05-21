import os
import sys
import requests
from flask import Flask, json, Blueprint
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models import db, User, UserRole
from app import app, bcrypt

# Create a test auth blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/login', methods=['POST'])
def login():
    from flask import request, jsonify
    from models import User
    from app import bcrypt
    
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'success': False, 'message': 'Email and password are required'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    if not user or not bcrypt.check_password_hash(user.password_hash, data['password']):
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
    
    # Create access token
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'success': True,
        'data': {
            'access_token': access_token,
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'role': user.role.value,
                'company_name': user.company_name
            }
        }
    }), 200

# Test configuration
TEST_EMAIL = 'test_pro@example.com'
TEST_PASSWORD = 'password123'
TEST_NAME = 'Test Professional'

class TestConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
    SECRET_KEY = 'test-secret-key'

class TestClient:
    def __init__(self, app):
        self.app = app
        self.client = app.test_client()
        
    def login(self, email, password):
        return self.client.post('/api/login', 
                              data=json.dumps({'email': email, 'password': password}),
                              content_type='application/json')

def create_test_app():
    # Create a test Flask app with the same configuration as the main app
    test_app = Flask(__name__)
    test_app.config.from_object(TestConfig)
    
    # Initialize extensions with test app
    db.init_app(test_app)
    
    # Initialize bcrypt with test app
    test_bcrypt = Bcrypt(test_app)
    
    # Initialize JWT
    JWTManager(test_app)
    
    # Register blueprints
    test_app.register_blueprint(auth_bp)
    
    return test_app, test_bcrypt

def setup_database(app, bcrypt):
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Create a test professional user
        hashed_password = bcrypt.generate_password_hash(TEST_PASSWORD).decode('utf-8')
        
        user = User(
            email=TEST_EMAIL,
            name=TEST_NAME,
            role=UserRole.PROFESSIONAL,
            password_hash=hashed_password,
            location='Nairobi',
            company_name='Test Contractors Ltd',
            nca_level=5,
            average_rating=4.5,
            total_ratings=10,
            successful_bids=7,
            total_bids=10
        )
        
        db.session.add(user)
        db.session.commit()
        
        return user

def test_login():
    # Create test app and get bcrypt instance
    test_app, test_bcrypt = create_test_app()
    
    # Set up test client
    with test_app.test_request_context():
        # Set up database
        user = setup_database(test_app, test_bcrypt)
        
        # Create test client
        client = TestClient(test_app)
        
        # Test successful login
        print("\nTesting successful login...")
        try:
            response = client.login(TEST_EMAIL, TEST_PASSWORD)
            print(f"Response status code: {response.status_code}")
            print(f"Response data: {response.data}")
            
            # Try to parse JSON only if there's content
            response_data = {}
            if response.data:
                try:
                    response_data = response.get_json()
                    if response_data is None:
                        response_data = {}
                    print("Parsed JSON response:", response_data)
                except Exception as e:
                    print(f"Failed to parse JSON response: {e}")
                    print(f"Raw response data: {response.data}")
            
            if response.status_code == 200 and response_data.get('success') and response_data.get('data', {}).get('access_token'):
                print("✅ Login successful!")
                print(f"Access token: {response_data['data']['access_token'][:30]}...")
            else:
                print("❌ Login failed!")
                print(f"Status code: {response.status_code}")
                print(f"Response: {response_data}")
        except Exception as e:
            print(f"❌ Exception during login test: {e}")
            import traceback
            traceback.print_exc()
        
        # Test invalid password
        print("\nTesting invalid password...")
        response = client.login(TEST_EMAIL, 'wrongpassword')
        data = json.loads(response.data)
        
        if response.status_code == 401 and not data.get('success') and 'Invalid credentials' in data.get('message', ''):
            print("✅ Invalid password handled correctly")
        else:
            print("❌ Invalid password not handled correctly")
            print(f"Status code: {response.status_code}")
            print(f"Response: {data}")
        
        # Clean up
        db.drop_all()

if __name__ == '__main__':
    test_login()
