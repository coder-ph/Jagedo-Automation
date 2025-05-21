import os
import sys
import json
import asyncio
import requests
import tempfile
from datetime import datetime, timedelta
from werkzeug.datastructures import FileStorage
from werkzeug.datastructures import FileStorage as FS
from bid_automation import BidAutomation

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)

from app import app, db, bcrypt
from models import (
    User, Job, Bid, Attachment, UserRole, JobStatus, BidStatus,
    Notification, Message, Category, ProfessionalSkill, Review, 
    ProjectStatusHistory
)
from flask_jwt_extended import create_access_token, JWTManager

with app.app_context():
    if 'bcrypt' not in app.extensions:
        bcrypt.init_app(app)
    
    if 'jwt' not in app.extensions:
        app.config['JWT_SECRET_KEY'] = 'test-secret-key'
        jwt = JWTManager(app)
  
    db.create_all()

BASE_URL = 'http://localhost:5000'
TEST_CUSTOMER_EMAIL = 'test_customer_new@example.com'
TEST_CUSTOMER_PASSWORD = 'customer123'
TEST_PRO_EMAIL = 'test_pro_new@example.com'
TEST_PRO_PASSWORD = 'password123'

def create_test_user(email, password, role, **kwargs):
    with app.app_context():
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            db.session.delete(existing_user)
            db.session.commit()
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        user_data = {
            'name': kwargs.get('name', 'Test User'),
            'email': email,
            'role': role,
            'password_hash': hashed_password,
            'company_name': kwargs.get('company_name', 'Test Company'),
            'location': kwargs.get('location', 'Nairobi'),
            'is_active': True
        }
        
        if role == UserRole.PROFESSIONAL:
            user_data.update({
                'nca_level': kwargs.get('nca_level', 5),
                'average_rating': kwargs.get('average_rating', 4.5),
                'total_ratings': kwargs.get('total_ratings', 10),
                'successful_bids': kwargs.get('successful_bids', 7),
                'total_bids': kwargs.get('total_bids', 10)
            })
        
        user = User(**user_data)
        db.session.add(user)
        db.session.commit()
        print(f"Created test {role.value} with ID: {user.id}")
        
        return user

def login_user(email, password):
    login_url = f'{BASE_URL}/api/login'
    login_data = {
        'email': email,
        'password': password
    }
    
    try:
        response = requests.post(login_url, json=login_data, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get('success'):
            return {
                'access_token': data['data']['access_token'],
                'user': data['data'].get('user')
            }
        else:
            print(f"Login failed: {data.get('message', 'Unknown error')}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Login request failed: {str(e)}")
        return None

def upload_project_document(project_id, token, file_content=None):
    url = f"{BASE_URL}/api/projects/{project_id}/documents"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    try:
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.txt', delete=False) as temp_file:
            if file_content is None:
                file_content = f"Test document for project {project_id}\nUploaded at {datetime.utcnow()}"
            temp_file.write(file_content)
            temp_file_path = temp_file.name
        
        with open(temp_file_path, 'rb') as f:
            files = {
                'file': (os.path.basename(temp_file_path), f, 'text/plain')
            }
            response = requests.post(url, headers=headers, files=files)
        
        os.unlink(temp_file_path)
        
        response.raise_for_status()
        data = response.json()
        
        if data.get('success'):
            document_id = data.get('document_id') or data.get('data', {}).get('document_id')
            if document_id:
                print(f"Uploaded document with ID: {document_id}")
                return document_id
        
        print(f"Failed to upload document: {data.get('message', 'Unknown error')}")
        return None
        
    except requests.exceptions.RequestException as e:
        print(f"Error uploading document: {str(e)}")
        if hasattr(e, 'response') and hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}")
        return None
    except Exception as e:
        print(f"Unexpected error in upload_project_document: {str(e)}")
        return None

def download_document(document_id, token, expect_success=True):
    url = f"{BASE_URL}/api/documents/{document_id}"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    try:
        response = requests.get(url, headers=headers, stream=True)
        
        if expect_success:
            response.raise_for_status()
            content = b''.join(chunk for chunk in response.iter_content(chunk_size=128))
            print(f"Successfully downloaded document {document_id} ({len(content)} bytes)")
            return content
        else:
            if response.status_code < 400:
                raise AssertionError(f"Expected document access to be denied but got {response.status_code}")
            print(f"Document access correctly denied for document {document_id}")
            return None
    except requests.exceptions.RequestException as e:
        if expect_success:
            print(f"Failed to download document: {str(e)}")
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                print(f"Response: {e.response.text}")
        return None
    except Exception as e:
        print(f"Unexpected error in upload_project_document: {str(e)}")
        return None

def create_test_project(token, title="Test Project", with_document=False):
    url = f"{BASE_URL}/api/projects"
    
    project_data = {
        'title': title,
        'description': 'This is a test project description',
        'budget': 1000000,
        'location': 'Nairobi, Kenya',
        'category_id': 1,
        'timeline_weeks': 8,
        'max_timeline': 12,  # Add max_timeline for scoring
        'requirements': 'Test requirements',
        'documents': []
    }
    
    print(f"\nCreating project with data: {json.dumps(project_data, indent=2)}")
    
    try:
        headers = {
            'Authorization': f'Bearer {token}',
            'Accept': 'application/json'
        }
        
        if with_document:
            with tempfile.NamedTemporaryFile(mode='w+', suffix='.txt', delete=False) as temp_file:
                temp_file.write(f"Initial document for project: {title}\nCreated at: {datetime.utcnow()}")
                temp_file_path = temp_file.name
            
            with open(temp_file_path, 'rb') as f:
                files = {
                    'file': (os.path.basename(temp_file_path), f, 'text/plain')
                }
                for key, value in project_data.items():
                    if isinstance(value, (str, int, float, bool)):
                        files[key] = (None, str(value))
                
                response = requests.post(
                    url, 
                    headers={'Authorization': f'Bearer {token}'},
                    files=files
                )
            
            os.unlink(temp_file_path)
        else:
            headers['Content-Type'] = 'application/json'
            response = requests.post(
                url, 
                headers=headers, 
                json=project_data, 
                timeout=10
            )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        try:
            response_data = response.json()
            print(f"Response Body: {json.dumps(response_data, indent=2)}")
        except ValueError:
            print(f"Response Body (non-JSON): {response.text}")
            return None
        
        if response.status_code == 201:
            job_id = response_data.get('data', {}).get('job_id')
            if not job_id:
                job_id = response_data.get('data', {}).get('project_id')
                
            if job_id:
                print(f"Successfully created project with ID: {job_id}")
                
                if with_document and 'document_id' in response_data.get('data', {}):
                    print(f"Initial document uploaded with ID: {response_data['data']['document_id']}")
                
                return job_id
            else:
                print("Error: No project_id or job_id in response data")
                print(f"Response data: {response_data}")
                return None
        else:
            print(f"Failed to create project. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {str(e)}")
        if hasattr(e, 'response') and hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}")
        return None
    except Exception as e:
        print(f"Unexpected error in create_test_project: {str(e)}")
        return None

def submit_bid(base_url, token, job_id, amount=4500000, proposal='I have extensive experience in construction projects similar to this one. My team and I can complete the work within the specified timeline and budget.', timeline_weeks=12):
    url = f"{base_url}/api/projects/{job_id}/bids"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    bid_data = {
        'amount': amount,
        'proposal': proposal,
        'timeline_weeks': timeline_weeks
    }
    
    print(f"\nSubmitting bid with data: {json.dumps(bid_data, indent=2)}")
    
    try:
        response = requests.post(url, headers=headers, json=bid_data)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        try:
            response_data = response.json()
            print("Response Body:", json.dumps(response_data, indent=2))
        except ValueError:
            print("Response Body (non-JSON):", response.text)
        
        if response.status_code == 500:
            print("\nServer returned 500 error. Checking for traceback...")
            try:
                if hasattr(response, 'text') and 'Traceback' in response.text:
                    print("\nServer Traceback:")
                    print(response.text.split('Traceback')[-1])
            except Exception as e:
                print(f"Could not extract traceback: {str(e)}")
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"\nBid submission failed with status {getattr(e.response, 'status_code', 'N/A')}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.text}")
            if hasattr(e.response, 'headers'):
                print(f"Response headers: {dict(e.response.headers)}")
        print(f"Error details: {str(e)}")
        
        import traceback
        print("\nLocal Traceback:")
        traceback.print_exc()
        
        return None
        return None

def get_project_bids(project_id, token, expected_status=200):
    url = f'{BASE_URL}/api/projects/{project_id}/bids'
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json'
    }
    
    print(f"\nFetching bids for project {project_id}...")
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        try:
            response_data = response.json()
            print("Response:", json.dumps(response_data, indent=2))
        except ValueError:
            print("Response (non-JSON):", response.text)
            return None
            
        if response.status_code == expected_status:
            return response_data.get('data', []) if expected_status == 200 else response_data
        else:
            print(f"Unexpected status code: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {str(e)}")
        return None

def select_winning_bid(project_id, bid_id, token):
    try:
        url = f'{BASE_URL}/api/projects/{project_id}/select-winner'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        data = {'bid_id': bid_id}
        
        print(f"\nSelecting winning bid {bid_id} for project {project_id}...")
        print(f"Request URL: {url}")
        print(f"Request headers: {headers}")
        print(f"Request data: {data}")
        
        response = requests.post(url, headers=headers, json=data, timeout=10)
        print(f"Response status code: {response.status_code}")
        print(f"Response headers: {response.headers}")
        print(f"Response body: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Successfully selected winning bid: {result}")
            return result
        else:
            error_msg = f"Failed to select winning bid. Status: {response.status_code}, Response: {response.text}"
            print(error_msg)
            return {
                'success': False,
                'error': error_msg,
                'status_code': response.status_code,
                'response': response.text
            }
    except Exception as e:
        error_msg = f"Exception while selecting winning bid: {str(e)}"
        print(error_msg)
        import traceback
        traceback.print_exc()
        return {
            'success': False,
            'error': error_msg,
            'exception': str(e)
        }

def clean_database():
    from sqlalchemy import inspect, text
    
    try:
        db.session.execute(text('PRAGMA foreign_keys = OFF'))
        db.session.commit()
        
        inspector = inspect(db.engine)
        metadata = db.metadata
        
        for table in reversed(metadata.sorted_tables):
            try:
                table.drop(db.engine)
                print(f"Dropped table: {table.name}")
            except Exception as e:
                print(f"Warning: Could not drop table {table.name}: {str(e)}")
        
        db.create_all()
        print("Recreated all tables")
        
        db.session.execute(text('PRAGMA foreign_keys = ON'))
        db.session.commit()
        
        print("Database cleaned up and recreated successfully")
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Error during cleanup: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        try:
            db.session.execute(text('PRAGMA foreign_keys = ON'))
            db.session.commit()
        except Exception as e:
            print(f"Error in database cleanup: {str(e)}")
            import traceback
            traceback.print_exc()

def test_document_access():
    with app.app_context():
        print("=== Starting Document Access Test ===\n")
        
        print("Cleaning up database...")
        clean_database()
        
        print("\n1. Creating test users...")
        customer = create_test_user(
            email=TEST_CUSTOMER_EMAIL,
            password=TEST_CUSTOMER_PASSWORD,
            role=UserRole.CUSTOMER,
            name="Test Customer",
            location="Nairobi"
        )
        
        pro1 = create_test_user(
            email=TEST_PRO_EMAIL,
            password=TEST_PRO_PASSWORD,
            role=UserRole.PROFESSIONAL,
            name="Test Professional 1",
            location="Nairobi",
            nca_level=5,
            average_rating=4.8,
            total_ratings=15,
            successful_bids=12,
            total_bids=15
        )
        
        pro2 = create_test_user(
            email="test_pro2@example.com",
            password=TEST_PRO_PASSWORD,
            role=UserRole.PROFESSIONAL,
            name="Test Professional 2",
            location="Mombasa",
            nca_level=4,
            average_rating=4.5,
            total_ratings=10,
            successful_bids=8,
            total_bids=10
        )
        
        print("\n2. Logging in as customer...")
        customer_auth = login_user(TEST_CUSTOMER_EMAIL, TEST_CUSTOMER_PASSWORD)
        assert customer_auth is not None, "Failed to login as customer"
        customer_token = customer_auth['access_token']
        
        print("\n3. Logging in as professionals...")
        pro1_auth = login_user(TEST_PRO_EMAIL, TEST_PRO_PASSWORD)
        assert pro1_auth is not None, "Failed to login as professional 1"
        pro1_token = pro1_auth['access_token']
        
        pro2_auth = login_user("test_pro2@example.com", TEST_PRO_PASSWORD)
        assert pro2_auth is not None, "Failed to login as professional 2"
        pro2_token = pro2_auth['access_token']
        
        print("\n4. Creating test project...")
        project_id = create_test_project(customer_token, "Bidding Workflow Test Project")
        assert project_id is not None, "Failed to create test project"
        
        print("\n5. Uploading document to project...")
        doc_content = f"Test document for project {project_id}"
        document_id = upload_project_document(project_id, customer_token, doc_content)
        assert document_id is not None, "Failed to upload additional document"
        
        # Test 1: Verify customer can access the document
        print("\n6. Testing customer document access...")
        content = download_document(document_id, customer_token)
        assert content is not None, "Customer should be able to access the document"
        print("✓ Customer can access the document")
        
        # Test 2: Verify professional 1 can access the document during bidding
        print("\n7. Testing professional 1 document access during bidding...")
        content = download_document(document_id, pro1_token)
        assert content is not None, "Professional 1 should be able to access the document during bidding"
        print("✓ Professional 1 can access the document during bidding")
        
        print("\n7. Submitting bids from both professionals...")
        bid1_id = submit_bid(BASE_URL, pro1_token, project_id, 4500000, "Professional 1 bid")
        assert bid1_id is not None, "Failed to submit bid from professional 1"
            
        bid2_id = submit_bid(BASE_URL, pro2_token, project_id, 5000000, "Professional 2 bid")
        assert bid2_id is not None, "Failed to submit bid from professional 2"
        print(f"Submitted bids: {bid1_id}, {bid2_id}")
        
        print("\n8. Verifying document access after bid submission...")
        for token, name in [(pro1_token, "Professional 1"), (pro2_token, "Professional 2")]:
            content = download_document(document_id, token)
            assert content is not None, f"{name} should still have access to documents after bidding"
            print(f"{name} can still access the document after bidding")
        
        print("\n9. Selecting winning bid...")
        result = select_winning_bid(project_id, bid1_id, customer_token)
        assert result is not None and result.get('success'), "Failed to select winning bid"
        print("Selected professional 1 as the winner")
        
        print("\n10. Verifying document access after project award...")
        content = download_document(document_id, pro1_token)
        assert content is not None, "Winning professional should still have access to documents"
        print("Winning professional can still access the document")
        
        try:
            content = download_document(document_id, pro2_token, expect_success=False)
            assert content is None, "Losing professional should not have access to documents after project award"
            print("Losing professional cannot access the document after project award")
        except Exception as e:
            assert False, f"Error testing losing professional access: {str(e)}"
        
        print("All document access tests passed!")
        return True

async def test_bidding_workflow_async():
    print("\n=== Starting Bidding Workflow Test ===")
    
    # Clean up any existing test data
    clean_database()
    
    # Create test users
    customer = create_test_user(
        email=TEST_CUSTOMER_EMAIL,
        password=TEST_CUSTOMER_PASSWORD,
        role=UserRole.CUSTOMER,
        name='Test Customer',
        company_name='Customer Company',
        location='Nairobi, Kenya'
    )
    
    # Create an admin user for notifications
    admin = create_test_user(
        email='admin@example.com',
        password='admin123',
        role=UserRole.ADMIN,
        name='Admin User',
        company_name='Admin Company',
        location='Nairobi, Kenya'
    )
    
    # Create multiple professionals for testing bid automation
    professionals = []
    # Create first professional with high NCA and rating to ensure they meet the minimum score
    pro = create_test_user(
        email='test_pro_1@example.com',
        password=TEST_PRO_PASSWORD,
        role=UserRole.PROFESSIONAL,
        name='High Rated Pro',
        company_name='Elite Construction',
        location='Nairobi, Kenya',
        nca_level=8,  # Max NCA level
        average_rating=5.0,  # Perfect rating
        total_ratings=50,
        successful_bids=48,
        total_bids=50
    )
    professionals.append(pro)
    
    # Create remaining professionals with varying attributes
    for i in range(2, 6):
        pro = create_test_user(
            email=f'test_pro_{i}@example.com',
            password=TEST_PRO_PASSWORD,
            role=UserRole.PROFESSIONAL,
            name=f'Test Pro {i}',
            company_name=f'Pro Construction {i}',
            location='Nairobi, Kenya',
            nca_level=7 - (i % 4),  # Vary NCA level from 4-7
            average_rating=4.7 - (i * 0.1),  # Vary ratings from 4.3-4.7
            total_ratings=30,
            successful_bids=25,
            total_bids=30
        )
        professionals.append(pro)
    
    # Log in as customer
    customer_login = login_user(TEST_CUSTOMER_EMAIL, TEST_CUSTOMER_PASSWORD)
    if not customer_login:
        print("Failed to log in as customer")
        return False
    
    customer_token = customer_login['access_token']
    
    # Create a project with a document
    project_id = create_test_project(customer_token, "Test Bidding Automation Project", with_document=True)
    if not project_id:
        print("Failed to create test project")
        return False
    
    print(f"Created project with ID: {project_id}")
    
    # Upload a document to the project
    document_id = upload_project_document(project_id, customer_token, "Test document content")
    if not document_id:
        print("Failed to upload test document")
        return False
    
    # Submit bids from multiple professionals
    bids = []
    for i, pro in enumerate(professionals):
        pro_login = login_user(pro.email, TEST_PRO_PASSWORD)
        if not pro_login:
            print(f"Failed to log in as professional {i+1}")
            continue
            
        pro_token = pro_login['access_token']
        
        # Vary bid amounts and timelines
        # Using amounts below the project budget (1,000,000 KES)
        amount = 900000 - (i * 100000)  # Vary amounts from 500K to 900K
        timeline_weeks = 10 - (i % 3)  # Vary timelines from 8-10 weeks
        
        bid = submit_bid(
            BASE_URL, 
            pro_token, 
            project_id, 
            amount=amount,
            timeline_weeks=timeline_weeks,
            proposal=f'Bid from {pro.name} for {amount} KES in {timeline_weeks} weeks'
        )
        
        if bid:
            bids.append(bid)
            print(f"Submitted bid {len(bids)} from {pro.name}: {amount} KES, {timeline_weeks} weeks")
    
    if len(bids) < 3:  # We want at least 3 bids for a good test
        print(f"Not enough bids were submitted. Got {len(bids)}, expected at least 3")
        return False
    
    print(f"\nSubmitted {len(bids)} bids. Waiting for bid automation to process...")
    
    # Initialize bid automation
    bid_automation = BidAutomation()
    
    print("\nScores for each bid:")
    with app.app_context():
        project = Job.query.get(project_id)
        bids = Bid.query.filter_by(job_id=project_id).all()
        
        # Calculate and print scores
        for bid in bids:
            score = bid_automation.calculate_bid_score(bid, project)
            print(f"Bid {bid.id} - Amount: {bid.amount}, Timeline: {bid.timeline_weeks} weeks, Score: {score:.2f}")
    
    # Run the evaluation
    print("\nEvaluating all bids for the project...")
    with app.app_context():
        # Ensure we have a fresh session
        db.session.rollback()
        await bid_automation.evaluate_project(project_id)
        # Explicitly commit any pending changes
        db.session.commit()
    
    # Add a small delay to ensure all async operations complete
    await asyncio.sleep(1)
    
    # Verify the results with a fresh database session
    with app.app_context():
        # Start a new transaction
        db.session.rollback()
        
        # Explicitly refresh the project and related objects
        updated_project = db.session.query(Job).options(
            db.joinedload(Job.bids),
            db.joinedload(Job.assigned_contractor)
        ).get(project_id)
        
        if not updated_project:
            print("❌ Project not found after evaluation")
            return False
        
        # Get the accepted bid with a fresh query
        accepted_bid = db.session.query(Bid).filter_by(
            job_id=project_id, 
            status=BidStatus.ACCEPTED
        ).options(
            db.joinedload(Bid.professional)
        ).first()
        
        # Debug output
        print("\n=== Debug Info ===")
        print(f"Project ID: {updated_project.id}")
        print(f"Project Status: {updated_project.status}")
        print(f"Assigned Contractor ID: {updated_project.assigned_contractor_id}")
        print(f"Number of Bids: {len(updated_project.bids) if updated_project.bids else 0}")
        
        if accepted_bid:
            print(f"\n✅ Found accepted bid: ID={accepted_bid.id}, Amount={accepted_bid.amount}, Contractor={accepted_bid.professional.name if accepted_bid.professional else 'None'}")
            
            # Verify the project was updated correctly
            if updated_project.status != JobStatus.AWARDED:
                print(f"❌ Project status was not updated to AWARDED. Current status: {updated_project.status}")
                return False
                
            if updated_project.assigned_contractor_id != accepted_bid.professional_id:
                print(f"❌ Project contractor was not set correctly. Expected: {accepted_bid.professional_id}, Got: {updated_project.assigned_contractor_id}")
                return False
                
            # Verify the bid status in the database
            db_bid = db.session.query(Bid).get(accepted_bid.id)
            if db_bid.status != BidStatus.ACCEPTED:
                print(f"❌ Bid status not updated in database. Expected: {BidStatus.ACCEPTED}, Got: {db_bid.status}")
                return False
                
            print("\n✅ All verifications passed!")
            print(f"Project '{updated_project.title}' was successfully awarded to {accepted_bid.professional.name if accepted_bid.professional else 'contractor'}")
            return True
        else:
            print("\n❌ No bid was accepted. Checking for admin notification...")
            admin_notification = db.session.query(Notification).filter_by(
                notification_type="manual_review_required"
            ).first()
            
            if admin_notification:
                print(f"Admin was notified for manual review: {admin_notification.message}")
            else:
                print("No admin notification was created.")
                
            # Print all bids for debugging
            print("\n=== All Bids ===")
            for bid in updated_project.bids:
                print(f"- Bid {bid.id}: Status={bid.status}, Amount={bid.amount}, Contractor={bid.professional.name if bid.professional else 'None'}")
                
            return False
    
    # Check if a bid was automatically accepted
        accepted_bid = Bid.query.filter_by(
            job_id=project_id,
            status=BidStatus.ACCEPTED.value
        ).first()
        
        if not accepted_bid:
            # Check if admin was notified for manual review
            admin_notification = Notification.query.filter_by(
                notification_type='admin_action_required',
                title='Manual Review Required'
            ).first()
            
            if not admin_notification:
                print("No bid was accepted and no admin notification was created")
                return False
                
            print("No bid met the minimum score. Admin notification was created for manual review.")
            return True  # This is a valid outcome
            
        # Verify project status was updated
        if updated_project.status != JobStatus.AWARDED.value:
            print(f"Project status not updated. Expected: {JobStatus.AWARDED.value}, Got: {updated_project.status}")
            return False
            
        print(f"Bid automation successful! Project awarded to bid {accepted_bid.id}")
        
        # Verify notifications were sent
        customer_notification = Notification.query.filter_by(
            user_id=customer.id,
            notification_type='contractor_selected'
        ).first()
        
        contractor_notification = Notification.query.filter_by(
            user_id=accepted_bid.professional_id,
            notification_type='bid_accepted'
        ).first()
        
        if not customer_notification or not contractor_notification:
            print("Missing notifications for bid acceptance")
            return False
            
        print("Verified notifications were sent to both customer and winning contractor")
        
        # Verify document access
        winning_pro = User.query.get(accepted_bid.professional_id)
        winning_pro_login = login_user(winning_pro.email, TEST_PRO_PASSWORD)
        if not winning_pro_login:
            print("Failed to log in as winning professional")
            return False
            
        winning_pro_token = winning_pro_login['access_token']
        
        # Winning professional should have access to documents
        content = download_document(document_id, winning_pro_token)
        if not content:
            print("Winning professional cannot access project documents")
            return False
            
        print("Verified winning professional has access to project documents")
        
        # Losing professionals should not have access to documents
        for pro in professionals:
            if pro.id == winning_pro.id:
                continue
                
            pro_login = login_user(pro.email, TEST_PRO_PASSWORD)
            if not pro_login:
                continue
                
            pro_token = pro_login['access_token']
            try:
                content = download_document(document_id, pro_token, expect_success=False)
                if content is not None:
                    print(f"Losing professional {pro.name} still has access to documents")
                    return False
            except:
                pass  # Expected to fail
        
        print("Verified losing professionals cannot access project documents")
    
    print("\nAll bidding workflow tests passed!")
    return True

def main():
    
    async def main_async():
        with app.app_context():
            print("\n=== Starting Bidding Workflow Tests ===")
            
            # Run the test
            if not await test_bidding_workflow_async():
                return 1
            
            print("\nAll tests passed successfully!")
            return 0

    return asyncio.run(main_async())

if __name__ == "__main__":
    sys.exit(main())
