from flask import Flask, jsonify, request, send_file
from flask_migrate import Migrate
from flask_cors import CORS
from datetime import datetime, timedelta
from models import db, User, UserRole, BidStatus, JobStatus, Message, Attachment as Document, Job, Bid, Notification
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import HTTPException
from werkzeug.utils import secure_filename
import os
import time
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    JWTManager, create_access_token,
    jwt_required, get_jwt_identity
)
from functools import wraps
import base64
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from twilio.rest import Client
import requests
import json

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

def send_notification(user_id, title, message, notification_type):
    """
    Send a notification to a user
    
    This is a wrapper around NotificationService.send for backward compatibility
    """
    return NotificationService.send(user_id, title, message, notification_type)

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
CORS(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Constants
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx', 'txt'}

# Utility Classes
class FileHandler:
    @staticmethod
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    @staticmethod
    def save_file(file, project_id):
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, f"project_{project_id}_{int(time.time())}_{filename}")
        file.save(filepath)
        return filename, filepath
    
    @staticmethod
    def get_mime_type(filename):
        if '.' not in filename:
            return 'application/octet-stream'
        ext = filename.rsplit('.', 1)[1].lower()
        return {
            'pdf': 'application/pdf',
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'png': 'image/png',
            'doc': 'application/msword',
            'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'txt': 'text/plain'
        }.get(ext, 'application/octet-stream')

class NotificationService:
    @staticmethod
    def send(user_id, title, message, notification_type):
        try:
            notification = Notification(
                user_id=user_id,
                title=title,
                message=message,
                notification_type=notification_type,
                created_at=datetime.utcnow()
            )
            db.session.add(notification)
            db.session.commit()
            
            # Send email notification if user has email
            user = User.query.get(user_id)
            if user and user.email:
                NotificationService._send_email(user.email, title, message)
                
            # Send SMS if user has phone
            if user and user.phone:
                NotificationService._send_sms(user.phone, f"{title}: {message}")
                
            return True
            
        except Exception as e:
            print(f"Error sending notification: {e}")
            db.session.rollback()
            return False
    
    @staticmethod
    def _send_email(to_email, subject, message):
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
        except Exception as e:
            print(f"Error sending email: {e}")
    
    @staticmethod
    def _send_sms(to_phone, message):
        try:
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            client.messages.create(
                body=message,
                from_=TWILIO_PHONE_NUMBER,
                to=to_phone
            )
        except Exception as e:
            print(f"Error sending SMS: {e}")

class AccessControl:
    @staticmethod
    def project_required(f):
        @wraps(f)
        def decorated(project_id, *args, **kwargs):
            project = Job.query.get_or_404(project_id)
            current_user = get_current_user()
            
            if current_user.role == UserRole.ADMIN:
                return f(project, *args, **kwargs)
                
            if current_user.role == UserRole.CUSTOMER and project.customer_id != current_user.id:
                return jsonify({'error': 'Access denied'}), 403
                
            if current_user.role == UserRole.PROFESSIONAL and \
               (not project.assigned_contractor_id or project.assigned_contractor_id != current_user.id):
                return jsonify({'error': 'Access denied'}), 403
                
            return f(project, *args, **kwargs)
        return decorated

def get_current_user():
    current_user_id = get_jwt_identity()
    return User.query.get(int(current_user_id))


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
    # Use the professional relationship instead of contractor
    professional = bid.professional
    
    # NCA Level: 40 points max (1-8 scale)
    nca_score = (professional.nca_level / 8) * 40
    
    # Rating: 25 points max (0-5 scale)
    # The rating is already on a 5-point scale, so we just multiply by 5 to get to 25 points
    rating_score = (professional.average_rating * 5) if professional.average_rating is not None else 0
    
    # Success Rate: 15 points max (based on successful_bids / total_bids)
    success_rate = 0
    if professional.total_bids > 0:
        success_rate = (professional.successful_bids / professional.total_bids) * 100
    success_score = (success_rate / 100) * 15
    
    # Location Score: 20 points max (0-1 scale)
    location_score = (bid.location_score or 0) * 20
    
    # Calculate total score (max 100 points)
    total_score = nca_score + rating_score + success_score + location_score
    
    # Ensure score is between 0 and 100
    return max(0, min(100, total_score))

def select_winning_bid(project_id):
    """
    Select the winning bid for a project based on the highest score
    Returns: (winning_bid, score) or (None, None) if no valid bids
    """
    project = Job.query.get(project_id)
    if not project or project.status != JobStatus.OPEN:
        return None, None
    
    # Get all pending bids for the job
    bids = Bid.query.filter_by(
        job_id=project_id,  # Changed from project_id to job_id
        status=BidStatus.PENDING
    ).all()
    
    if not bids:
        return None, None
    
    # Calculate score for each bid
    scored_bids = []
    for bid in bids:
        score = calculate_bid_score(bid)
        scored_bids.append((bid, score))
        print(f"Bid ID: {bid.id}, Professional: {bid.professional_id}, Score: {score:.2f}")
    
    # Sort by score (descending)
    scored_bids.sort(key=lambda x: x[1], reverse=True)
    
    return scored_bids[0] if scored_bids else (None, None)
    
def find_contractors_for_project(project_id, min_score=0.3, max_results=20):
    project = Job.query.get(project_id)
    if not project:
        return []
    
    professionals = User.query.filter_by(
        role=UserRole.PROFESSIONAL,
        is_active=True 
    ).all()
    
    scored_contractors = []
    for pro in professionals:
        score, match_type = location_match_score(project.location, pro.location)
        if score >= min_score:
            scored_contractors.append({
                'contractor': pro,
                'score': score,
                'match_type': match_type
            })
    
    scored_contractors.sort(key=lambda x: x['score'], reverse=True)
  
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
        
        # Verify the current user is the project owner or admin
        if current_user.role == UserRole.CUSTOMER and project.customer_id != current_user.id:
            return jsonify({
                'success': False,
                'message': 'Only the project owner can select a winner'
            }), 403
            
        # Check if a winner has already been selected
        if project.status == JobStatus.AWARDED:
            return jsonify({
                'success': False,
                'message': 'A winner has already been selected for this project'
            }), 400
            
        # Find the winning bid (highest score)
        winning_bid, winning_score = select_winning_bid(project_id)
        
        if not winning_bid:
            return jsonify({
                'success': False,
                'message': 'No suitable bids found for this project'
            }), 400
            
        # Update all bids for this project
        for bid in project.bids:
            if bid.id == winning_bid.id:
                bid.status = BidStatus.ACCEPTED
                
                # Update professional's stats for the winner
                professional = bid.professional
                professional.successful_bids += 1
                professional.total_bids += 1
                
                # Update the professional's average rating based on the winning score
                if professional.average_rating is None:
                    professional.average_rating = winning_score
                else:
                    professional.average_rating = (
                        (professional.average_rating * (professional.total_bids - 1) + winning_score) 
                        / professional.total_bids
                    )
                
                # Notify the winner
                notify_bid_accepted(bid)
            else:
                # Reject all other bids and notify the bidders
                if bid.status != BidStatus.REJECTED:  # Only update if not already rejected
                    bid.status = BidStatus.REJECTED
                    send_notification(
                        bid.professional_id,
                        "Bid Not Selected",
                        f"Your bid for project {project.title} was not selected.",
                        "bid_rejected"
                    )
        
        # Update project status to AWARDED
        project.status = JobStatus.AWARDED
        project.assigned_contractor_id = winning_bid.professional_id
        
        db.session.commit()
        
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
@role_required([UserRole.PROFESSIONAL])
def submit_bid(project_id):
    try:
        data = validate_json()
        required_fields = ['amount', 'proposal', 'timeline_weeks']
        validate_required_fields(data, required_fields)
        
        project = Job.query.get_or_404(project_id)
        contractor = get_current_user()
    
        # Check if project is open for bidding
        if project.status != JobStatus.OPEN:
            return jsonify({
                'success': False,
                'message': 'This project is no longer accepting bids'
            }), 400

        # Check if a winner has already been selected
        if project.status == JobStatus.AWARDED:
            return jsonify({
                'success': False,
                'message': 'A winner has already been selected for this project'
            }), 400
    
        # Check for existing bid from this professional
        existing_bid = Bid.query.filter_by(
            project_id=project_id,
            professional_id=contractor.id
        ).first()
        
        if existing_bid:
            return jsonify({
                'success': False,
                'message': 'You have already submitted a bid for this project'
            }), 400
      
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
      
        # Notify project owner about the new bid
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
        
        if current_user.id != project.customer_id and current_user.role != UserRole.ADMIN:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Get recommended contractors
        contractors = find_contractors_for_project(project_id)

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

@app.route('/api/projects/<int:project_id>', methods=['GET'])
@jwt_required()
def get_project(project_id):
    try:
        project = Job.query.get_or_404(project_id)
        current_user = get_current_user()
        
        # Check if user has access to this project
        has_access = (
            current_user.role == UserRole.ADMIN or
            project.customer_id == current_user.id or
            (project.assigned_contractor_id and project.assigned_contractor_id == current_user.id)
        )
        
        if not has_access:
            return jsonify({
                'success': False,
                'message': 'You do not have permission to view this project'
            }), 403
        
        # Prepare project data
        project_data = {
            'id': project.id,
            'title': project.title,
            'description': project.description,
            'status': project.status.value,
            'created_at': project.created_at.isoformat() if project.created_at else None,
            'category_id': project.category_id,
            'location': project.location,
            'customer_id': project.customer_id,
            'assigned_contractor_id': project.assigned_contractor_id
        }
        
        # Only include budget and bids for the project owner or admin
        if current_user.role in [UserRole.ADMIN, UserRole.CUSTOMER] and project.customer_id == current_user.id:
            project_data['budget'] = str(project.budget)
            
            # Include all bids for the project owner
            bids_data = []
            for bid in project.bids:
                bid_data = {
                    'id': bid.id,
                    'amount': str(bid.amount),
                    'status': bid.status.value,
                    'created_at': bid.created_at.isoformat() if bid.created_at else None,
                    'professional_id': bid.professional_id,
                    'professional_name': bid.professional.name if bid.professional else None
                }
                bids_data.append(bid_data)
            
            project_data['bids'] = bids_data
        
        return jsonify({
            'success': True,
            'data': project_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to fetch project details'
        }), 500

@app.route('/api/projects', methods=['POST'])
@jwt_required()
@role_required([UserRole.ADMIN, UserRole.CUSTOMER])
def create_project():
    try:
        data = validate_json()
        required_fields = ['title', 'description', 'budget', 'location', 'category_id']
        validate_required_fields(data, required_fields)
        
        current_user = get_current_user()
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
    
def has_document_access(user_id, document):
    """Check if a user has access to a document"""
    try:
        user = User.query.get(user_id)
        if not user:
            return False, "User not found"
            
        # Admin can access any document
        if user.role == UserRole.ADMIN:
            return True, "Admin access"
            
        # Document uploader can access their own documents
        if document.uploaded_by == user_id:
            return True, "Document owner"
            
        # Project participants can access project documents
        if document.project_id:
            project = Job.query.get(document.project_id)
            if not project:
                return False, "Project not found"
                
            # Project owner can access all project documents
            if project.customer_id == user_id:
                return True, "Project owner"
                
            # Assigned contractor can access project documents
            if project.assigned_contractor_id == user_id:
                return True, "Assigned contractor"
        
        # Bid documents can be accessed by the bid owner
        if document.bid_id:
            bid = Bid.query.get(document.bid_id)
            if bid and bid.professional_id == user_id:
                return True, "Bid owner"
                
        return False, "Access denied"
        
    except Exception as e:
        print(f"Error checking document access: {e}")
        return False, "Error checking access"

@app.route('/api/projects/<int:project_id>/documents', methods=['GET'])
@jwt_required()
@AccessControl.project_required
def list_project_documents(project):
    """List all documents for a project"""
    try:
        documents = Document.query.filter_by(project_id=project.id).all()
        current_user = get_current_user()
        
        result = [{
            'id': doc.id,
            'filename': doc.filename,
            'uploaded_at': doc.uploaded_at.isoformat(),
            'uploaded_by': doc.uploaded_by,
            'file_type': FileHandler.get_mime_type(doc.filename),
            'size': os.path.getsize(doc.filepath) if os.path.exists(doc.filepath) else 0,
            'is_owner': doc.uploaded_by == current_user.id
        } for doc in documents]
        
        return jsonify({
            'success': True,
            'documents': result
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/documents/<int:document_id>', methods=['GET'])
@jwt_required()
def download_document(document_id):
    """Download a document"""
    try:
        document = Document.query.get_or_404(document_id)
        current_user = get_current_user()
        
        # Check document access
        has_access, message = has_document_access(current_user.id, document)
        if not has_access:
            return jsonify({'error': message}), 403
    
        if not os.path.exists(document.filepath):
            return jsonify({'error': 'File not found'}), 404
   
        return send_file(
            document.filepath,
            as_attachment=True,
            download_name=document.filename,
            mimetype=FileHandler.get_mime_type(document.filename)
        )
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/documents/<int:document_id>', methods=['DELETE'])
@jwt_required()
def delete_document(document_id):
   
    try:
        document = Document.query.get_or_404(document_id)
        current_user = get_current_user()
        
        if document.uploaded_by != current_user.id and current_user.role != UserRole.ADMIN:
            return jsonify({'error': 'Access denied'}), 403
        
        if os.path.exists(document.filepath):
            os.remove(document.filepath)
        
        db.session.delete(document)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Document deleted successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

def find_matching_contractors(project_id):
    project = Job.query.get(project_id)
    if not project:
        return []
    professionals = User.query.filter_by(role=UserRole.PROFESSIONAL).all()

    professionals_with_scores = []
    for pro in professionals:
        score = location_match_score(project.location, pro.location)
        if score > 0:  
            professionals_with_scores.append({
                'professional': pro,
                'location_score': score,
                'avg_rating': 0,  # TODO: Calculate actual average rating
                'nca_level': 0    # TODO: Get NCA level
            })
    
    professionals_with_scores.sort(
        key=lambda x: (x['location_score'], x['nca_level'], x['avg_rating']),
        reverse=True
    )
    
    return [p['professional'] for p in professionals_with_scores[:20]]  # Return top 10 matches

# mpesa payment
def get_mpesa_auth_token():
   
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

@app.route('/api/mpesa/callback', methods=['POST'])
def mpesa_callback():
    try:
        data = request.get_json()
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

# File handling constants and functions moved to FileHandler class

@app.route('/api/projects/<int:project_id>/documents', methods=['POST'])
@jwt_required()
@AccessControl.project_required
def upload_document(project):
    """Upload a document for a project"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
            
        if not FileHandler.allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed'}), 400
            
        filename, filepath = FileHandler.save_file(file, project.id)
        current_user = get_current_user()
        
        document = Document(
            project_id=project.id,
            filename=filename,
            filepath=filepath,
            uploaded_by=current_user.id
        )
        db.session.add(document)
        db.session.commit()
        
        # Notify relevant users
        notify_document_upload(document)
        
        return jsonify({
            'success': True,
            'message': 'File uploaded successfully',
            'document_id': document.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

def notify_document_upload(document):
    """Notify relevant users about a new document upload"""
    try:
        project = document.project
        uploader = User.query.get(document.uploaded_by)
        current_user = get_current_user()
        
        # Determine who to notify
        recipient_ids = set()
        
        # Notify project owner if not the uploader
        if project.customer_id != document.uploaded_by:
            recipient_ids.add(project.customer_id)
            
        # Notify assigned contractor if exists and not the uploader
        if project.assigned_contractor_id and project.assigned_contractor_id != document.uploaded_by:
            recipient_ids.add(project.assigned_contractor_id)
        
        # Send notifications
        for recipient_id in recipient_ids:
            if recipient_id != current_user.id:  # Don't notify self
                NotificationService.send(
                    recipient_id,
                    "New Document Uploaded",
                    f"User {uploader.first_name} {uploader.last_name} uploaded a new document to project {project.title}",
                    "document_upload"
                )
                
    except Exception as e:
        print(f"Error in notify_document_upload: {e}")
        return False

@app.route('/api/projects/<int:project_id>/bid-scores', methods=['GET'])
@jwt_required()
@role_required([UserRole.ADMIN, UserRole.CUSTOMER])
def get_bid_scores(project_id):
    """Get detailed scoring information for all bids on a project"""
    project = Job.query.get_or_404(project_id)
    current_user = get_current_user()
    
    # Verify permissions
    if current_user.role == UserRole.CUSTOMER and project.customer_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Use job_id instead of project_id to match the database schema
    bids = Bid.query.filter_by(job_id=project_id).all()
    
    result = []
    for bid in bids:
        score = calculate_bid_score(bid)
        # Use the professional relationship which is defined in the Bid model
        professional = bid.professional
        result.append({
            'bid_id': bid.id,
            'contractor_id': professional.id,
            'contractor_name': f"{professional.name}",  # Using name field since first_name/last_name don't exist in the model
            'company': professional.company_name,
            'amount': float(bid.amount),
            'nca_level': professional.nca_level,
            'rating': professional.average_rating,
            'success_rate': (professional.successful_bids / professional.total_bids * 100) if professional.total_bids > 0 else 0,
            'location_score': bid.location_score,
            'location_match_type': bid.location_match_type,
            'total_score': score,
            'status': bid.status.value
        })
    
    # Sort by total score (descending)
    result.sort(key=lambda x: x['total_score'], reverse=True)
    
    return jsonify({
        'success': True,
        'project_id': project_id,
        'project_title': project.title,
        'bids': result
    })

def notify_bid_accepted(bid):
    """Notify contractor that their bid was accepted"""
    message = f"Your bid for project {bid.job.title} has been accepted!"
    send_notification(
        bid.professional_id,  # Use professional_id instead of contractor_id
        "Bid Accepted",
        message,
        "bid_accepted"
    )
    
    # Also update the notification content in the database
    notification = Notification.query.filter_by(
        user_id=bid.professional_id,
        title="Bid Accepted",
        message=message
    ).order_by(Notification.created_at.desc()).first()
    
    if notification:
        notification.content = message
        db.session.commit()
    
# Mock email function for testing
def send_email(to, subject, body):
    print(f"[MOCK] Email sent to {to} with subject '{subject}' and body: {body}")
    return True

# Mock SMS function for testing
def send_sms(to, message):
    print(f"[MOCK] SMS sent to {to}: {message}")
    return True

# Notification system
def send_notification(user_id, title, message, notification_type):
    # Use the message as the content if not provided
    content = message
    notification = Notification(
        user_id=user_id,
        title=title,
        message=message,
        content=content,  # Set content to the same as message
        notification_type=notification_type,
        read=False
    )
    db.session.add(notification)
    db.session.commit()
    
    # Optionally send email/SMS
    user = User.query.get(user_id)
    if user and hasattr(user, 'email') and user.email:
        send_email(user.email, title, message)
    if user and hasattr(user, 'phone') and user.phone:
        send_sms(user.phone, f"{title}: {message}")

def notify_status_change(project, old_status, new_status):
    """Notify relevant parties about project status changes"""
    try:
        if new_status == JobStatus.AWARDED and project.assigned_contractor_id:
            NotificationService.send(
                project.assigned_contractor_id,
                "Project Awarded",
                f"You have been awarded project {project.title}",
                "project_awarded"
            )
        elif new_status == JobStatus.PAID and project.assigned_contractor_id:
            NotificationService.send(
                project.assigned_contractor_id,
                "Project Paid",
                f"Project {project.title} has been paid",
                "project_paid"
            )
        elif new_status == JobStatus.IN_PROGRESS and project.assigned_contractor_id:
            NotificationService.send(
                project.assigned_contractor_id,
                "Project Started",
                f"Project {project.title} has started",
                "project_started"
            )
        elif new_status == JobStatus.COMPLETED:
            NotificationService.send(
                project.customer_id,
                "Project Completed",
                f"Project {project.title} has been completed",
                "project_completed"
            )
        elif new_status == JobStatus.DISPUTED:
            NotificationService.send(
                project.customer_id,
                "Project Disputed",
                f"Project {project.title} has been disputed",
                "project_disputed"
            )
        elif new_status == JobStatus.CLOSED:
            NotificationService.send(
                project.customer_id,
                "Project Closed",
                f"Project {project.title} has been closed",
                "project_closed"
            )
    except Exception as e:
        print(f"Error in notify_status_change: {e}")

def update_project_status(project_id, new_status, notes=None):
    """Update project status and notify relevant parties"""
    try:
        project = Job.query.get(project_id)
        if not project:
            return False
            
        old_status = project.status
        
        if old_status == new_status:
            return True
            
        valid_transitions = {
            JobStatus.DRAFT: [JobStatus.OPEN, JobStatus.CANCELLED],
            JobStatus.OPEN: [JobStatus.AWARDED, JobStatus.CANCELLED],
            JobStatus.AWARDED: [JobStatus.IN_PROGRESS, JobStatus.CANCELLED],
            JobStatus.IN_PROGRESS: [JobStatus.COMPLETED, JobStatus.DISPUTED],
            JobStatus.COMPLETED: [JobStatus.PAID, JobStatus.DISPUTED],
            JobStatus.DISPUTED: [JobStatus.IN_PROGRESS, JobStatus.CANCELLED],
            JobStatus.PAID: [JobStatus.CLOSED],
            JobStatus.CANCELLED: [JobStatus.OPEN],
        }
        
        if new_status not in valid_transitions.get(old_status, []):
            return False
            
        project.status = new_status
        
        if notes:
            project.notes = notes
            
        status_change = ProjectStatusHistory(
            project_id=project_id,
            from_status=old_status,
            to_status=new_status,
            changed_by=get_jwt_identity(),
            notes=notes
        )
        db.session.add(status_change)
        db.session.commit()
        
        notify_status_change(project, old_status, new_status)
        
        return True
        
    except Exception as e:
        print(f"Error updating project status: {e}")
        db.session.rollback()
        return False
@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG', False))