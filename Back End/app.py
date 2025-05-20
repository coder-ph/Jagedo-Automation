from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_cors import CORS
from datetime import datetime
from models import db, User, UserRole, BidStatus, JobStatus, Message
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import HTTPException
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    JWTManager, create_access_token,
    jwt_required, get_jwt_identity
)
from datetime import timedelta, datetime
from functools import wraps
import base64
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from twilio.rest import Client
import requests

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

# Email configs
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
SMTP_USERNAME = os.getenv('SMTP_USERNAME')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
EMAIL_FROM = os.getenv('EMAIL_FROM')

# Twilio configs
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')

def send_email(to_email, subject, message):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_FROM
        msg['To'] = to_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(message, 'plain'))
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def send_sms(to_phone, message):
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=to_phone
        )
        return True
    except Exception as e:
        print(f"Error sending SMS: {e}")
        return False

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
   
    if not location:
        return {}
        
    parts = [p.strip() for p in location.split(',')]
    parts = [p for p in parts if p]  
    
    hierarchy = {
        'full': location,
        'building': parts[0] if len(parts) > 0 else None,
        'street': parts[1] if len(parts) > 1 else None,
        'ward': parts[2] if len(parts) > 2 else None,
        'subcounty': parts[3] if len(parts) > 3 else None,
        'county': parts[4] if len(parts) > 4 else None
    }
    
    return hierarchy
    
def location_match_score(client_location, contractor_location):
    """
    Calculate a match score between client and contractor locations
    Returns: score (float), match_type (str)
    """
    if not client_location or not contractor_location:
        return 0.0, 'no_location'
    
    client = get_location_hierarchy(client_location)
    contractor = get_location_hierarchy(contractor_location)
    
    # Exact match (same building/street)
    if client.get('building') and client.get('building') == contractor.get('building'):
        return 1.0, 'exact'
    
    # Same street
    if client.get('street') and client.get('street') == contractor.get('street'):
        return 0.9, 'same_street'
    
    # Same ward
    if client.get('ward') and client.get('ward') == contractor.get('ward'):
        return 0.7, 'same_ward'
    
    # Same sub-county
    if client.get('subcounty') and client.get('subcounty') == contractor.get('subcounty'):
        return 0.5, 'same_subcounty'
    
    # Same county
    if client.get('county') and client.get('county') == contractor.get('county'):
        return 0.3, 'same_county'
    
    return 0.0, 'no_match'

def calculate_bid_score(bid):
    """
    Calculate a weighted score for a bid based on multiple factors
    Returns: float score (0-100)
    """
    contractor = bid.contractor
    
    # 1. NCA Level (40% weight)
    # Higher NCA levels (1-8) are better
    nca_score = (contractor.nca_level / 8) * 40
    
    # 2. Contractor Rating (25% weight)
    # Assuming rating is between 0-5
    rating_score = (contractor.average_rating / 5) * 25 if contractor.average_rating else 0
    
    # 3. Success Rate (15% weight)
    success_rate = 0
    if contractor.total_bids > 0:
        success_rate = (contractor.successful_bids / contractor.total_bids) * 100
    success_score = (success_rate / 100) * 15
    
    # 4. Location Score (20% weight)
    # Use the pre-calculated location score (0-1.0) and scale to 20%
    location_score = (bid.location_score or 0) * 20
    
    # Calculate total score
    total_score = nca_score + rating_score + success_score + location_score
    
    # Ensure score is within bounds
    return max(0, min(100, total_score))

def select_winning_bid(project_id):

    project = Job.query.get(project_id)
    if not project or project.status != JobStatus.OPEN:
        return None, None
    
    bids = Bid.query.filter_by(
        project_id=project_id,
        status=BidStatus.PENDING
    ).all()
    
    if not bids:
        return None, None
    
    # Calculate score for each bid
    scored_bids = []
    for bid in bids:
        score = calculate_bid_score(bid)
        scored_bids.append((bid, score))
    
    # Sort by score (descending)
    scored_bids.sort(key=lambda x: x[1], reverse=True)
    
    return scored_bids[0] if scored_bids else (None, None)
    
def find_contractors_for_project(project_id, min_score=0.3, max_results=20):
    """
    Find contractors for a project with location-based fallback
    Returns: list of (contractor, score, match_type) tuples
    """
    project = Job.query.get(project_id)
    if not project:
        return []
    
    # Get all active professionals
    professionals = User.query.filter_by(
        role=UserRole.PROFESSIONAL,
        is_active=True  # Assuming we have this field
    ).all()
    
    # Score each professional
    scored_contractors = []
    for pro in professionals:
        score, match_type = location_match_score(project.location, pro.location)
        if score >= min_score:
            scored_contractors.append({
                'contractor': pro,
                'score': score,
                'match_type': match_type
            })
    
    # Sort by score (descending)
    scored_contractors.sort(key=lambda x: x['score'], reverse=True)
    
    # Apply max results
    return scored_contractors[:max_results]

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

#  automatic selection of winning bid
@app.route('/api/projects/<int:project_id>/select-winner', methods=['POST'])
@jwt_required()
@role_required([UserRole.ADMIN, UserRole.CUSTOMER])
def select_winner(project_id):
    try:
        project = Job.query.get_or_404(project_id)
        current_user = get_current_user()
        
        # Verify permissions
        if current_user.role == UserRole.CUSTOMER and project.customer_id != current_user.id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Only allow if project is still open
        if project.status != JobStatus.OPEN:
            return jsonify({
                'success': False,
                'error': 'Project is not open for bidding'
            }), 400
        
        # Select winning bid
        winning_bid, winning_score = select_winning_bid(project_id)
        
        if not winning_bid:
            return jsonify({
                'success': False,
                'error': 'No suitable bids found'
            }), 404
        
        # Update project and bid status
        project.assigned_contractor_id = winning_bid.professional_id
        project.status = JobStatus.AWARDED
        winning_bid.status = BidStatus.ACCEPTED
        
        # Update contractor's successful bids count
        contractor = winning_bid.contractor
        contractor.total_bids += 1
        contractor.successful_bids += 1
        
        # Recalculate success rate
        if contractor.total_bids > 0:
            contractor.average_rating = (
                (contractor.average_rating * (contractor.total_bids - 1) + winning_score) 
                / contractor.total_bids
            )
        
        db.session.commit()
        
        # Notify winner and other bidders
        notify_bid_accepted(winning_bid)
        
        return jsonify({
            'success': True,
            'message': 'Winning bid selected successfully',
            'data': {
                'bid_id': winning_bid.id,
                'contractor_id': winning_bid.professional_id,
                'score': winning_score
            }
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


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
    
    # bid submission to include location matching
@app.route('/api/projects/<int:project_id>/bids', methods=['POST'])
@jwt_required()
    
def submit_bid(project_id):
        try:
            data = validate_json()
            required_fields = ['amount', 'proposal', 'timeline_weeks']
            validate_required_fields(data, required_fields)
            
            project = Job.query.get_or_404(project_id)
            contractor = get_current_user()
            
            # Verify contractor role
            if contractor.role != UserRole.PROFESSIONAL:
                return jsonify({'error': 'Only professionals can submit bids'}), 403
            
            # Check if project is open
            if project.status != JobStatus.OPEN:
                return jsonify({'error': 'Project is not accepting bids'}), 400
            
            # Check for existing bid
            existing_bid = Bid.query.filter_by(
                project_id=project_id,
                professional_id=contractor.id
            ).first()
            
            if existing_bid:
                return jsonify({'error': 'You have already submitted a bid for this project'}), 400
            
            # Calculate location match score
            location_score, match_type = location_match_score(project.location, contractor.location)
            
            # Create bid
            bid = Bid(
                project_id=project_id,
                professional_id=contractor.id,
                amount=float(data['amount']),
                proposal=data['proposal'],
                timeline_weeks=int(data['timeline_weeks']),
                location_score=location_score,
                location_match_type=match_type,
                status=BidStatus.PENDING
            )
            
            db.session.add(bid)
            db.session.commit()
            
            # Notify project owner
            send_notification(
                project.customer_id,
                "New Bid Received",
                f"A new bid has been submitted for your project: {project.title}",
                "new_bid"
            )
            
            return jsonify({
                'success': True,
                'message': 'Bid submitted successfully',
                'data': {
                    'bid_id': bid.id,
                    'location_score': location_score,
                    'match_type': match_type
                }
            })
            
        except ValueError as e:
            return jsonify({'success': False, 'error': str(e)}), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': 'Failed to submit bid'}), 500

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

@app.route('/api/projects/<int:project_id>/recommended-contractors', methods=['GET'])
@jwt_required()
def get_recommended_contractors(project_id):
    try:
        project = Job.query.get_or_404(project_id)
        current_user = get_current_user()
        
        # Verify access
        if current_user.id != project.customer_id and current_user.role != UserRole.ADMIN:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Get recommended contractors
        contractors = find_contractors_for_project(project_id)
        
        # Format response
        result = [{
            'id': item['contractor'].id,
            'name': item['contractor'].name,
            'company': item['contractor'].company_name,
            'location': item['contractor'].location,
            'match_score': item['score'],
            'match_type': item['match_type'],
            'nca_level': item['contractor'].nca_level,
            'rating': item['contractor'].average_rating,
            'success_rate': (item['contractor'].successful_bids / item['contractor'].total_bids * 100) if item['contractor'].total_bids > 0 else 0
        } for item in contractors]
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

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

# Create project
@app.route('/api/projects', methods=['POST'])
@jwt_required()
@role_required([UserRole.CUSTOMER])
def create_project():
    try:
        data = validate_json()
        required_fields = ['title', 'description', 'budget', 'location', 'category_id']
        validate_required_fields(data, required_fields)
        
        current_user = get_current_user()
        
        # Create project
        project = Job(
            title=data['title'],
            description=data['description'],
            budget=float(data['budget']),
            location=data['location'],
            category_id=data['category_id'],
            customer_id=current_user.id,
            status=JobStatus.OPEN
        )
        
        db.session.add(project)
        db.session.commit()
        
        # TODO: Add file attachment handling
        # TODO: Trigger contractor matching
        
        return jsonify({
            'success': True,
            'message': 'Project created successfully',
            'data': {
                'project_id': project.id
            }
        }), 201
        
    except ValueError as e:
        return jsonify({'success': False, 'message': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Failed to create project'}), 500

def find_matching_contractors(project_id):
    """
    Find matching contractors for a project based on location and other criteria
    """
    project = Job.query.get(project_id)
    if not project:
        return []
    
    # Get all professionals
    professionals = User.query.filter_by(role=UserRole.PROFESSIONAL).all()
    
    # Score and sort professionals by location match
    professionals_with_scores = []
    for pro in professionals:
        score = location_match_score(project.location, pro.location)
        if score > 0:  # Only include contractors with some location match
            professionals_with_scores.append({
                'professional': pro,
                'location_score': score,
                'avg_rating': 0,  # TODO: Calculate actual average rating
                'nca_level': 0    # TODO: Get NCA level
            })
    
    # Sort by location score (descending), then NCA level, then rating
    professionals_with_scores.sort(
        key=lambda x: (x['location_score'], x['nca_level'], x['avg_rating']),
        reverse=True
    )
    
    return [p['professional'] for p in professionals_with_scores[:20]]  # Return top 10 matches

# mpesa payment
def get_mpesa_auth_token():
    """
    Get M-Pesa API auth token
    """
    global MPESA_AUTH_TOKEN, MPESA_AUTH_TOKEN_EXPIRY
    
    if MPESA_AUTH_TOKEN and datetime.utcnow() < MPESA_AUTH_TOKEN_EXPIRY:
        return MPESA_AUTH_TOKEN
    
    auth = (f"{MPESA_CONSUMER_KEY}:{MPESA_CONSUMER_SECRET}").encode('utf-8')
    auth = base64.b64encode(auth).decode('utf-8')
    
    headers = {
        'Authorization': f'Basic {auth}',
        'Content-Type': 'application/json'
    }
    
    response = requests.get(
        'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials',
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()
        MPESA_AUTH_TOKEN = data['access_token']
        MPESA_AUTH_TOKEN_EXPIRY = datetime.utcnow() + timedelta(seconds=data['expires_in'] - 60)
        return MPESA_AUTH_TOKEN
    else:
        raise Exception("Failed to get M-Pesa auth token")

def initiate_stk_push(phone, amount, account_reference, description):
    """
    Initiate STK push to customer
    """
    token = get_mpesa_auth_token()
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    password = base64.b64encode(
        f"{MPESA_SHORTCODE}{MPESA_PASSKEY}{timestamp}".encode()
    ).decode()
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'BusinessShortCode': MPESA_SHORTCODE,
        'Password': password,
        'Timestamp': timestamp,
        'TransactionType': 'CustomerPayBillOnline',
        'Amount': amount,
        'PartyA': phone,
        'PartyB': MPESA_SHORTCODE,
        'PhoneNumber': phone,
        'CallBackURL': MPESA_CALLBACK_URL,
        'AccountReference': account_reference,
        'TransactionDesc': description
    }
    
    response = requests.post(
        'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest',
        headers=headers,
        json=payload
    )
    
    return response.json()

# Mpesa callback
@app.route('api/mpesa/callback', methods=['POST'])
def mpesa_callback():
    try:
        data = request.get_json()
        #verify callback is from mpesa
        # TODO:add proper validation
        result = data['Body']['stkCallback']['ResultCode']
        checkout_request_id = data['Body']['stkCallback']['CheckoutRequestID']
        merchant_request_id = data['Body']['stkCallback']['MerchantRequestID']
        metadata = data['Body']['stkCallback']['CallbackMetadata']['Item']
        
        amount = None
        mpesa_receipt = None
        phone = None
        
        for item in metadata:
            if item['Name'] == 'Amount':
                amount = item['Value']
            elif item['Name'] == 'MpesaReceiptNumber':
                mpesa_receipt = item['Value']
            elif item['Name'] == 'PhoneNumber':
                phone = item['Value']
                
        if result_code == 0 and mpesa_receipt and phone:
            return jsonify({
                'success': True,
                'message': 'Payment successful',
                'data': {
                    'amount': amount,
                    'mpesa_receipt': mpesa_receipt,
                    'phone': phone
                }
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Payment failed',
                'data': {
                    'result_code': result_code,
                    'checkout_request_id': checkout_request_id,
                    'merchant_request_id': merchant_request_id,
                    'amount': amount,
                    'mpesa_receipt': mpesa_receipt,
                    'phone': phone
                }
            }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Payment failed',
            'data': {
                'error': str(e)
            }
        }), 500
        
    

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

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx', 'txt'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/projects/<int:project_id>/documents', methods=['POST'])
@jwt_required()
def upload_document(project_id):
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        if file and allowed_file(file.filename):
            # Create upload directory if it doesn't exist
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            
            # Generate a secure filename and save the file
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, f"project_{project_id}_{filename}")
            file.save(filepath)
            
            # Save document info to database
            document = Document(
                project_id=project_id,
                filename=filename,
                filepath=filepath,
                uploaded_by=get_jwt_identity()
            )
            db.session.add(document)
            db.session.commit()
            
            # Notify relevant parties
            notify_document_upload(document)
            
            return jsonify({
                'success': True,
                'message': 'File uploaded successfully',
                'document_id': document.id
            }), 201
            
        return jsonify({'error': 'File type not allowed'}), 400
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    


def notify_bid_accepted(bid):
    """Notify contractor that their bid was accepted"""
    send_notification(
        bid.contractor_id,
        "Bid Accepted",
        f"Your bid for project {bid.project.title} has been accepted!",
        "bid_accepted"
    )
    
    db.session.commit()    
    
# Notification system
def send_notification(user_id, title, message, notification_type):
    notification = Notification(
        user_id=user_id,
        title=title,
        message=message,
        type=notification_type,
        read=False
    )
    db.session.add(notification)
    db.session.commit()
    
    # Optionally send email/SMS
    user = User.query.get(user_id)
    if user.email:
        send_email(user.email, title, message)
    if user.phone:
        send_sms(user.phone, f"{title}: {message}")

def notify_document_upload(document):
    project = document.project
    if document.uploaded_by == project.customer_id:
        recipient_id = project.assigned_contractor_id
    else:
        recipient_id = project.customer_id
    
    send_notification(
        recipient_id,
        "New Document Uploaded",
        f"A new document was uploaded to project {project.title}",
        "document_upload"
    )

# def update_project_status(project_id, new_status, notes=None):
    project = Job.query.get(project_id)
    if not project:
        return False
    
    # Status transition validation
    valid_transitions = {
        JobStatus.OPEN: [JobStatus.AWARDED, JobStatus.CANCELLED],
        JobStatus.AWARDED: [JobStatus.PAID, JobStatus.CANCELLED],
        JobStatus.PAID: [JobStatus.IN_PROGRESS, JobStatus.CANCELLED],
        JobStatus.IN_PROGRESS: [JobStatus.COMPLETED, JobStatus.DISPUTED],
        JobStatus.COMPLETED: [JobStatus.CLOSED],
        JobStatus.DISPUTED: [JobStatus.IN_PROGRESS, JobStatus.CANCELLED]
    }
    
    if new_status not in valid_transitions.get(project.status, []):
        return False
    
    # Update status
    old_status = project.status
    project.status = new_status
    
    # Log status change
    status_change = ProjectStatusHistory(
        project_id=project_id,
        from_status=old_status,
        to_status=new_status,
        changed_by=get_jwt_identity(),
        notes=notes
    )
    db.session.add(status_change)
    db.session.commit()
    
    # Notify relevant parties
    notify_status_change(project, old_status, new_status)
    
    return True
@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG', False))