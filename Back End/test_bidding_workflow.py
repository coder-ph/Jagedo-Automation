import os
import sys
import json
import asyncio
import requests
import tempfile
import threading
import time
from datetime import datetime, timedelta
from werkzeug.datastructures import FileStorage
from werkzeug.datastructures import FileStorage as FS
from sqlalchemy import text
from werkzeug.serving import make_server

# Add the parent directory to the path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import Flask and extensions
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token

# Import app factory and models
from app import create_app
from app.extensions import db, jwt
from app.models import (
    User, Job, Bid, Attachment, UserRole, JobStatus, BidStatus,
    Notification, Message, Category, ProfessionalSkill, Review, 
    ProjectStatusHistory
)

# Create test app
app = create_app('testing')
app.config.update({
    'TESTING': True,
    'DEBUG': True,
    'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'JWT_SECRET_KEY': 'test-secret-key',
    'JWT_ACCESS_TOKEN_EXPIRES': timedelta(hours=1),
    'JWT_REFRESH_TOKEN_EXPIRES': timedelta(days=30),
    'CACHE_TYPE': 'SimpleCache',
    'CACHE_DEFAULT_TIMEOUT': 300,
    'SERVER_NAME': 'localhost:5001',
    'PREFERRED_URL_SCHEME': 'http',
    'WTF_CSRF_ENABLED': False
})

# Initialize bcrypt
bcrypt = Bcrypt(app)

# Create all database tables
with app.app_context():
    db.create_all()

# Import BidAutomation after app is created
from bid_automation import BidAutomation

with app.app_context():
    # Ensure bcrypt is initialized
    if 'bcrypt' not in app.extensions:
        app.extensions['bcrypt'] = bcrypt
    
    # Create all database tables
    db.create_all()

# Base URL for API requests
BASE_URL = 'http://localhost:5001'
TEST_CUSTOMER_EMAIL = 'test_customer_new@example.com'
TEST_CUSTOMER_PASSWORD = 'customer123'
TEST_PRO_EMAIL = 'test_pro_new@example.com'
TEST_PRO_PASSWORD = 'password123'
TEST_PRO_EMAIL_2 = 'test_pro2_new@example.com'
TEST_PRO_PASSWORD_2 = 'password123'

def create_test_user(email, password, role, **kwargs):
    with app.app_context():
        try:
            # Start a new transaction
            db.session.begin()
            
            # Check for existing user and delete if exists
            existing_user = db.session.query(User).filter_by(email=email).first()
            if existing_user:
                db.session.delete(existing_user)
                db.session.commit()
            
            # Prepare user data without password
            user_data = {
                'name': kwargs.get('name', 'Test User'),
                'email': email,
                'role': role,
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
            
            # Create user with plain password - the setter will hash it
            user = User(**user_data)
            user.password = password  # This will use the password setter to hash it
            db.session.add(user)
            db.session.commit()
            print(f"Created test {role.value} with ID: {user.id}")
            
            return user
            
        except Exception as e:
            db.session.rollback()
            print(f"Error creating test user {email}: {e}")
            raise

def login_user(email, password, client=None):
    """Login a user using the test client or requests."""
    if client:
        # Use test client
        response = client.post('/api/auth/login', json={
            'email': email,
            'password': password
        })
        data = response.get_json()
    else:
        # Fallback to requests
        login_url = f'{BASE_URL}/api/auth/login'
        try:
            response = requests.post(login_url, json={
                'email': email,
                'password': password
            }, timeout=10)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Login request failed: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    print(f"Error response: {error_data}")
                except:
                    print(f"Raw response: {e.response.text}")
            return None
    
    if data.get('status') == 'success':
        return {
            'access_token': data['data']['access_token'],
            'user': data['data'].get('user')
        }
    else:
        error_msg = data.get('message', 'Unknown error')
        if 'data' in data and 'errors' in data['data']:
            error_msg = str(data['data']['errors'])
        print(f"Login failed: {error_msg}")
        return None

def upload_project_document(project_id, token, file_content=None, client=None):
    """Upload a document to a project using either the test client or direct HTTP requests.
    
    Args:
        project_id: ID of the project to upload the document to
        token: Authentication token
        file_content: Optional content for the file (default: auto-generated)
        client: Flask test client (if using test client)
    """
    if file_content is None:
        file_content = f"Test document for project {project_id}\nUploaded at {datetime.utcnow()}"
    
    try:
        if client is not None:
            # Use test client
            headers = {
                'Authorization': f'Bearer {token}'
            }
            
            # Create a temporary file for the test client
            with tempfile.NamedTemporaryFile(mode='w+', suffix='.txt', delete=False) as temp_file:
                temp_file.write(file_content)
                temp_file_path = temp_file.name
            
            try:
                with open(temp_file_path, 'rb') as f:
                    data = {
                        'file': (f, 'test_document.txt')
                    }
                    
                    # Use the correct document upload endpoint with document_type and job_id
                    response = client.post(
                        '/api/documents/upload',
                        data={
                            'file': (open(temp_file_path, 'rb'), 'test_document.txt'),
                            'document_type': 'job',
                            'job_id': str(project_id)  # Use job_id to associate the document with the project
                        },
                        headers=headers,
                        content_type='multipart/form-data'
                    )
                    
                    print(f"Document upload response status: {response.status_code}")
                    print(f"Response data: {response.data.decode('utf-8')}")
                    
                    if response.status_code != 201:
                        print(f"Failed to upload document: {response.status_code}")
                        return None
                    
                    data = response.get_json()
                    print(f"Upload response data: {json.dumps(data, indent=2)}")
                    
                    # Extract document ID from the response
                    document_id = None
                    if data.get('attachment'):
                        document_id = data['attachment'].get('id')
                    
                    if document_id:
                        print(f"Uploaded document with ID: {document_id}")
                        return document_id
                    else:
                        print("Error: Could not extract document ID from response")
                        print(f"Response data: {data}")
                        return None
                        
            finally:
                # Clean up the temporary file
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)
        
        # Fall back to direct HTTP requests
        url = f"{BASE_URL}/api/documents/upload"
        headers = {
            'Authorization': f'Bearer {token}'
        }
        
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.txt', delete=False) as temp_file:
            temp_file.write(file_content)
            temp_file_path = temp_file.name
        
        try:
            with open(temp_file_path, 'rb') as f:
                files = {
                    'file': (os.path.basename(temp_file_path), f, 'text/plain'),
                    'project_id': (None, str(project_id))  # Add project_id as form data
                }
                response = requests.post(url, headers=headers, files=files)
            
            response.raise_for_status()
            data = response.json()
            print(f"Upload response data (direct HTTP): {json.dumps(data, indent=2)}")
            
            if data.get('success'):
                # Extract document ID from the response
                document_id = None
                if data.get('attachment'):
                    document_id = data['attachment'].get('id')
                
                if document_id:
                    print(f"Uploaded document with ID: {document_id}")
                    return document_id
            
            error_msg = data.get('message', 'Unknown error')
            print(f"Failed to upload document: {error_msg}")
            print(f"Response data: {data}")
            return None
            
        finally:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
            
    except requests.exceptions.RequestException as e:
        print(f"Error uploading document: {str(e)}")
        if hasattr(e, 'response') and hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}")
        return None
    except Exception as e:
        print(f"Unexpected error in upload_project_document: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def download_document(document_id, token, expect_success=True, client=None):
    """Download a document using either the test client or direct HTTP requests.
    
    Args:
        document_id: ID of the document to download
        token: Authentication token
        expect_success: Whether to expect a successful response (default: True)
        client: Flask test client (if using test client)
    
    Returns:
        The document content if successful, None otherwise
    """
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    # Use Flask test client if available
    if client is not None:
        try:
            response = client.get(
                f'/api/documents/download/{document_id}',
                headers=headers
            )
            
            if expect_success:
                if response.status_code != 200:
                    print(f"Failed to download document: {response.status_code} - {response.data.decode()}")
                    return None
                return response.data
            else:
                if response.status_code == 200:
                    return response.data
                return None
                
        except Exception as e:
            if expect_success:
                print(f"Failed to download document using test client: {e}")
            return None
    
    # Fall back to direct HTTP requests
    try:
        response = requests.get(
            f'{BASE_URL}/api/documents/download/{document_id}',
            headers=headers,
            stream=True
        )
        
        if expect_success:
            response.raise_for_status()
            return response.content
        else:
            if response.status_code == 200:
                return response.content
            return None
            
    except requests.exceptions.RequestException as e:
        if expect_success:
            print(f"Failed to download document: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error in download_document: {str(e)}")
        return None

def create_test_project(token, title="Test Project", with_document=False, category_id=None, client=None):
    """Create a test project using either the test client or direct HTTP requests.
    
    Args:
        token (str): Authentication token
        title (str): Project title
        with_document (bool): Whether to include a document with the project
        category_id (int, optional): Category ID for the project
        client: Flask test client (if using test client)
    """
    if category_id is None:
        # Create a default category if none provided
        with app.app_context():
            category_id = create_test_category()
    
    # Prepare form data
    project_data = {
        'title': title,
        'description': 'This is a test project description',
        'budget': '1000000',  # Convert to string for form data
        'location': 'Nairobi, Kenya',
        'category_id': str(category_id),  # Use the provided or created category ID
        'timeline_weeks': '8',  # Convert to string for form data
        'max_timeline': '12',  # Convert to string for form data
        'requirements': 'Test requirements'
    }
    
    print(f"\nCreating project with data: {json.dumps(project_data, indent=2)}")
    
    try:
        if client is not None:
            # Use test client
            headers = {
                'Authorization': f'Bearer {token}',
                'Accept': 'application/json'
            }
            
            if with_document:
                # Create a temporary file for the test client
                with tempfile.NamedTemporaryFile(mode='w+', suffix='.txt', delete=False) as temp_file:
                    temp_file.write(f"Initial document for project: {title}\nCreated at: {datetime.utcnow()}")
                    temp_file_path = temp_file.name
                
                try:
                    with open(temp_file_path, 'rb') as f:
                        data = {}
                        for key, value in project_data.items():
                            data[key] = (None, str(value))
                        data['file'] = (f, 'test_document.txt')
                        
                        response = client.post(
                            '/api/projects',
                            data=data,
                            content_type='multipart/form-data',
                            headers=headers
                        )
                finally:
                    # Clean up the temporary file
                    if os.path.exists(temp_file_path):
                        os.unlink(temp_file_path)
            else:
                # No file upload, just form data
                # Convert all values to strings and ensure proper form data format
                data = {}
                for key, value in project_data.items():
                    data[key] = str(value)
                
                print(f"Sending request to /api/projects with data: {data}")
                response = client.post(
                    '/api/projects',
                    data=data,
                    headers=headers,
                    content_type='multipart/form-data'  # Ensure proper content type
                )
                print(f"Response status: {response.status_code}")
                print(f"Response data: {response.data.decode('utf-8')}")
            
            if response.status_code != 201:
                print(f"Failed to create project: {response.status_code}")
                print(f"Response: {response.data.decode('utf-8')}")
                return None
                
            data = response.get_json()
            print(f"Project creation response: {json.dumps(data, indent=2)}")
            
            # Extract project ID from the response
            project_id = data.get('project', {}).get('id')
            if project_id:
                print(f"Successfully created project with ID: {project_id}")
                return project_id
            else:
                print("Error: Could not extract project ID from response")
                return None
        
        # Fall back to direct HTTP requests
        url = f"{BASE_URL}/api/projects"
        headers = {
            'Authorization': f'Bearer {token}',
            'Accept': 'application/json'
        }
        
        if with_document:
            with tempfile.NamedTemporaryFile(mode='w+', suffix='.txt', delete=False) as temp_file:
                temp_file.write(f"Initial document for project: {title}\nCreated at: {datetime.utcnow()}")
                temp_file_path = temp_file.name
            
            with open(temp_file_path, 'rb') as f:
                
                response = requests.post(
                    url,
                    files=files,
                    data=data,  # Send as form data
                    headers=headers
                )
                
                # Clean up the temporary file
                try:
                    os.unlink(temp_file_path)
                except Exception as e:
                    print(f"Warning: Failed to delete temporary file {temp_file_path}: {e}")
        else:
            # Send as form data
            response = requests.post(
                url,
                data=project_data,  # Send as form data
                headers=headers
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

def submit_bid(base_url, token, job_id, amount=4500000, proposal='I have extensive experience in construction projects similar to this one. My team and I can complete the work within the specified timeline and budget.', timeline_weeks=12, team_members=None, client=None):
    """Submit a bid for a job.
    
    Args:
        base_url: Base URL of the API
        token: Authentication token
        job_id: ID of the job to bid on
        amount: Bid amount
        proposal: Bid proposal text
        timeline_weeks: Estimated timeline in weeks
        team_members: Optional list of team members
        client: Flask test client (if using test client)
    """
    url = "/api/bids"  # Updated to use the correct endpoint
    
    bid_data = {
        'job_id': job_id,  # Include job_id in the request data
        'amount': amount,
        'proposal': proposal,
        'timeline_weeks': timeline_weeks
    }
    
    if team_members is not None:
        bid_data['team_members'] = team_members
    
    print(f"\nSubmitting bid with data: {json.dumps(bid_data, indent=2)}")
    
    try:
        if client is not None:
            # Use test client with form data
            headers = {
                'Authorization': f'Bearer {token}'
            }
            # Convert all values to strings as expected by form data
            form_data = {k: str(v) for k, v in bid_data.items()}
            response = client.post(
                url,
                headers=headers,
                data=form_data,
                content_type='application/x-www-form-urlencoded'
            )
            response_data = response.get_json()
        else:
            # Use direct HTTP request with form data
            headers = {
                'Authorization': f'Bearer {token}'
            }
            # Convert all values to strings as expected by form data
            form_data = {k: str(v) for k, v in bid_data.items()}
            full_url = f"{base_url}{url}"
            response = requests.post(full_url, headers=headers, data=form_data)
            response.raise_for_status()
            response_data = response.json()
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {json.dumps(response_data, indent=2) if response_data else 'None'}")
        
        if hasattr(response, 'status_code') and response.status_code == 500:
            print("\nServer returned 500 error.")
            if hasattr(response, 'data'):
                print("Response data:", response.data.decode('utf-8'))
        
        return response_data
        
    except Exception as e:
        print(f"\nBid submission failed: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Status code: {getattr(e.response, 'status_code', 'N/A')}")
            if hasattr(e.response, 'text'):
                print(f"Response content: {e.response.text}")
        
        import traceback
        print("\nTraceback:")
        traceback.print_exc()
        return None
        
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

def select_winning_bid(project_id, bid_id, token, client=None):
    """Accept a bid for a project.
    
    Args:
        project_id: ID of the project (unused in the actual request, kept for backward compatibility)
        bid_id: ID of the bid to accept
        token: Authentication token
        client: Flask test client (if using test client)
    """
    url = f'/api/bids/{bid_id}/accept'
    
    print(f"\nAccepting bid {bid_id}...")
    
    try:
        if client is not None:
            # Use test client
            headers = {
                'Authorization': f'Bearer {token}'
            }
            response = client.post(
                url,
                headers=headers
            )
            response_data = response.get_json()
        else:
            # Use direct HTTP request
            headers = {
                'Authorization': f'Bearer {token}'
            }
            full_url = f"{BASE_URL}{url}"
            response = requests.post(full_url, headers=headers)
            response.raise_for_status()
            response_data = response.json()
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {json.dumps(response_data, indent=2) if response_data else 'None'}")
        
        return response_data
        
    except Exception as e:
        print(f"\nError accepting bid: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Status code: {getattr(e.response, 'status_code', 'N/A')}")
            if hasattr(e.response, 'text'):
                print(f"Response content: {e.response.text}")
        
        import traceback
        print("\nTraceback:")
        traceback.print_exc()
        return {
            'success': False,
            'error': f"Exception while accepting bid: {str(e)}",
            'exception': str(e)
        }

def clean_database():
    """Clean up the test database by dropping and recreating all tables."""
    print("Cleaning up test database...")
    with app.app_context():
        try:
            # Drop all tables
            db.drop_all()
            print("Dropped all tables")
            
            # Recreate all tables
            db.create_all()
            print("Recreated all tables")
            
            # Commit the changes
            db.session.commit()
            print("Database cleaned up successfully")
            return True
        except Exception as e:
            print(f"Error in database cleanup: {e}")
            db.session.rollback()
            return False

def create_test_category(name="Test Category"):
    """Create a test category if it doesn't exist."""
    from app.models import Category
    
    # Check if category already exists
    category = db.session.scalars(
        db.select(Category).filter_by(name=name)
    ).first()
    if not category:
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
    return category.id

def test_document_access():
    print("\n=== Starting Document Access Test ===")
    
    # Create a test client
    with app.test_client() as client:
        with app.app_context():
            # Clean up any existing data first
            clean_database()
            
            print("\n1. Creating test category...")
            category_id = create_test_category()
            print(f"Created/retrieved category with ID: {category_id}")
            
            print("\n2. Creating test users...")
            customer = create_test_user(
                email=TEST_CUSTOMER_EMAIL,
                password=TEST_CUSTOMER_PASSWORD,
                role=UserRole.CUSTOMER,
                name="Test Customer",
                location="Nairobi, Kenya"
            )
            print(f"Created test customer with ID: {customer.id}")
            
            professional1 = create_test_user(
                email=TEST_PRO_EMAIL,
                password=TEST_PRO_PASSWORD,
                role=UserRole.PROFESSIONAL,
                name="Test Professional 1",
                location="Nairobi, Kenya"
            )
            print(f"Created test professional with ID: {professional1.id}")
            
            professional2 = create_test_user(
                email=TEST_PRO_EMAIL_2,
                password=TEST_PRO_PASSWORD_2,
                role=UserRole.PROFESSIONAL,
                name="Test Professional 2",
                location="Nairobi, Kenya"
            )
            print(f"Created test professional with ID: {professional2.id}")
            
            print("\n3. Logging in as customer...")
            customer_auth = login_user(TEST_CUSTOMER_EMAIL, TEST_CUSTOMER_PASSWORD, client)
            assert customer_auth is not None, "Failed to login as customer"
            customer_token = customer_auth['access_token']
            print("Successfully logged in as customer")
            
            print("\n4. Logging in as professionals...")
            pro1_auth = login_user(TEST_PRO_EMAIL, TEST_PRO_PASSWORD, client)
            assert pro1_auth is not None, "Failed to login as professional 1"
            pro1_token = pro1_auth['access_token']
            
            pro2_auth = login_user(TEST_PRO_EMAIL_2, TEST_PRO_PASSWORD_2, client)
            assert pro2_auth is not None, "Failed to login as professional 2"
            pro2_token = pro2_auth['access_token']
            
            print("\n5. Creating test project...")
            # Create project with the category we created earlier and pass the test client
            project_id = create_test_project(
                customer_token, 
                "Document Access Test Project", 
                category_id=category_id,
                client=client
            )
            assert project_id is not None, "Failed to create test project"
            print(f"Created test project with ID: {project_id}")
            
            print("\n6. Uploading document to project...")
            doc_content = f"Test document for project {project_id}"
            document_id = upload_project_document(project_id, customer_token, doc_content, client=client)
            assert document_id is not None, "Failed to upload document"
            print(f"Uploaded document with ID: {document_id}")
            
            # Test 1: Verify customer can access the document
            print("\n7. Testing customer document access...")
            content = download_document(document_id, customer_token, client=client)
            assert content is not None, "Customer should be able to access the document"
            print("✅ Customer can access the document")
            
            # Submit bids from both professionals before testing document access
            print("\n8. Submitting bids from both professionals...")
            
            # Debug: Check project status before submitting bids
            print(f"Project ID: {project_id}")
            print(f"Professional 1 token: {pro1_token[:10]}...")
            print(f"Professional 2 token: {pro2_token[:10]}...")
            
            # Submit first bid
            print("\nSubmitting first bid...")
            bid1_response = submit_bid(BASE_URL, pro1_token, project_id, 4500000, "Professional 1 bid", client=client)
            print(f"Bid 1 response: {json.dumps(bid1_response, indent=2) if bid1_response else 'None'}")
            assert bid1_response is not None, "Failed to submit bid from professional 1"
            assert bid1_response.get('success') is True, f"Bid 1 submission failed: {bid1_response.get('error', 'Unknown error')}"
            assert 'bid' in bid1_response, "Bid 1 response missing 'bid' object"
            bid1_id = bid1_response['bid'].get('id')
            assert bid1_id is not None, "Bid 1 response missing 'id' field in bid object"
            
            # Submit second bid
            print("\nSubmitting second bid...")
            bid2_response = submit_bid(BASE_URL, pro2_token, project_id, 5000000, "Professional 2 bid", client=client)
            print(f"Bid 2 response: {json.dumps(bid2_response, indent=2) if bid2_response else 'None'}")
            assert bid2_response is not None, "Failed to submit bid from professional 2"
            assert bid2_response.get('success') is True, f"Bid 2 submission failed: {bid2_response.get('error', 'Unknown error')}"
            assert 'bid' in bid2_response, "Bid 2 response missing 'bid' object"
            bid2_id = bid2_response['bid'].get('id')
            assert bid2_id is not None, "Bid 2 response missing 'id' field in bid object"
            
            print(f"✅ Submitted bids: {bid1_id}, {bid2_id}")
            
            # Debug: Check if bids were created in the database
            with app.app_context():
                from app.models import Bid
                bids = Bid.query.filter(Bid.job_id == project_id).all()
                print(f"Found {len(bids)} bids in the database for project {project_id}:")
                for bid in bids:
                    print(f"- Bid ID: {bid.id}, Professional ID: {bid.professional_id}, Amount: {bid.amount}")
            
            # Test 2: Verify professionals can access the document after bidding
            print("\n9. Verifying document access after bid submission...")
            for token, name in [(pro1_token, "Professional 1"), (pro2_token, "Professional 2")]:
                content = download_document(document_id, token, client=client)
                assert content is not None, f"{name} should be able to access documents after bidding"
                print(f"✅ {name} can access the document after bidding")
            
            print("\n10. Selecting winning bid from professional 1...")
            result = select_winning_bid(project_id, bid1_id, customer_token, client=client)
            assert result is not None and result.get('success') is True, "Failed to select winning bid"
            print(f"✅ Selected winning bid: {bid1_id}")
            
            print("\n11. Verifying document access after project award...")
            content = download_document(document_id, pro1_token, client=client)
            assert content is not None, "Winning professional should still have access to documents"
            print("✅ Winning professional can still access the document")
            
            try:
                content = download_document(document_id, pro2_token, expect_success=False, client=client)
                assert content is None, "Losing professional should not have access to documents after project award"
                print("✅ Losing professional cannot access the document after project award")
            except Exception as e:
                assert False, f"Error testing losing professional access: {str(e)}"
            
            print("\n✅ All document access tests passed!")

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
        project = db.session.get(Job, project_id)
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
            db_bid = db.session.get(Bid, accepted_bid.id)
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
        winning_pro = db.session.get(User, accepted_bid.professional_id)
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
        
    # Test bidding with team members
    print("\n=== Testing Bidding with Team Members ===")
    
    # Create a new project for team bidding test
    team_project = create_test_project(
        customer_token, 
        title="Team Project",
        with_document=False
    )
    if not team_project:
        print("Failed to create team project")
        return False
        
    team_project_id = team_project['id']
    print(f"Created team project with ID: {team_project_id}")
    
    # Define team members
    team_members = [
        {
            'email': 'john.doe@example.com',
            'name': 'John Doe',
            'role': 'Lead Developer',
            'hourly_rate': 50,
            'hours': 40
        },
        {
            'email': 'jane.smith@example.com',
            'name': 'Jane Smith',
            'role': 'Senior Developer',
            'hourly_rate': 45,
            'hours': 35
        }
    ]
    
    # Submit a bid with team members
    print("\nSubmitting bid with team members...")
    bid_result = submit_bid(
        BASE_URL,
        winning_pro_token,
        team_project_id,
        amount=5000000,
        proposal='This bid includes a full team of experienced professionals.',
        timeline_weeks=10,
        team_members=team_members
    )
    
    if not bid_result or not bid_result.get('success'):
        print("Failed to submit bid with team members")
        return False
        
    print("Successfully submitted bid with team members")
    
    # Verify the bid was created with team members
    bids = get_project_bids(team_project_id, customer_token)
    if not bids or not bids.get('success') or not bids.get('data'):
        print("Failed to retrieve bids for team project")
        return False
        
    team_bid = None
    for bid in bids['data']:
        if 'team_members' in bid and len(bid['team_members']) > 0:
            team_bid = bid
            break
            
    if not team_bid:
        print("No bid with team members found")
        return False
        
    print(f"Found bid with {len(team_bid['team_members'])} team members")
    
    # Verify team member details
    for i, member in enumerate(team_members):
        if i >= len(team_bid['team_members']):
            print(f"Missing team member at index {i}")
            return False
            
        bid_member = team_bid['team_members'][i]
        for key in ['name', 'email', 'role']:
            if bid_member[key] != member[key]:
                print(f"Mismatch in team member {i} {key}: expected {member[key]}, got {bid_member[key]}")
                return False
    
    print("Verified all team member details")
    
    print("\nAll bidding workflow tests passed, including team bidding!")
    return True

def run_flask_app():
    """Run the Flask app in a separate thread."""
    server = make_server('localhost', 5001, app)
    server.serve_forever()

def main():
    """Main function to run the test."""
    # Start Flask server in a separate thread
    flask_thread = threading.Thread(target=run_flask_app, daemon=True)
    flask_thread.start()
    
    # Give the server a moment to start
    time.sleep(2)
    
    try:
        # Initialize database first
        with app.app_context():
            if not clean_database():
                print("Failed to initialize test database")
                return 1
            
            # Initialize BidAutomation with the Flask app
            bid_automation = BidAutomation(app)
        
        async def main_async():
            try:
                # Run the document access test
                print("\n=== Starting Document Access Test ===")
                if not test_document_access():
                    return 1
                
                # Clean up after document test
                with app.app_context():
                    if not clean_database():
                        print("Failed to clean up after document test")
                        return 1
                
                # Run the main test
                print("\n=== Starting Main Bidding Workflow Test ===")
                if not await test_bidding_workflow_async():
                    return 1
                
                # Clean up after first test
                with app.app_context():
                    if not clean_database():
                        print("Failed to clean up after first test")
                        return 1
                
                # Run the admin notification test
                print("\n=== Starting Admin Notification Flow Test ===")
                if not await test_admin_notification_flow():
                    return 1
                    
                return 0
                
            except Exception as e:
                print(f"Error in test execution: {e}")
                import traceback
                traceback.print_exc()
                return 1
            finally:
                # Always clean up at the end
                with app.app_context():
                    clean_database()
        
        # Run the async test suite
        return asyncio.run(main_async())
        
    except Exception as e:
        print(f"Error in main: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return asyncio.run(main_async())

async def test_admin_notification_flow():
    print("\n=== Testing Admin Notification Flow ===")
    
    # Clean up any existing test data
    clean_database()
    
    # Create test users
    customer = create_test_user(
        email='admin_flow_customer@example.com',
        password=TEST_CUSTOMER_PASSWORD,
        role=UserRole.CUSTOMER,
        name='Admin Flow Customer',
        company_name='Customer Company',
        location='Nairobi, Kenya'
    )
    
    # Create an admin user for notifications
    admin = create_test_user(
        email='admin_flow_admin@example.com',
        password='admin123',
        role=UserRole.ADMIN,
        name='Admin Flow Admin',
        company_name='Admin Company',
        location='Nairobi, Kenya'
    )
    
    # Create a professional who will be manually assigned
    manual_assign_pro = create_test_user(
        email='manual_assign_pro@example.com',
        password=TEST_PRO_PASSWORD,
        role=UserRole.PROFESSIONAL,
        name='Manual Assign Pro',
        company_name='Manual Assign Construction',
        location='Nairobi, Kenya',
        nca_level=5,
        average_rating=4.0,
        total_ratings=10,
        successful_bids=8,
        total_bids=10
    )
    
    # Log in as customer
    customer_login = login_user('admin_flow_customer@example.com', TEST_CUSTOMER_PASSWORD)
    if not customer_login:
        print("Failed to log in as customer")
        return False
    
    customer_token = customer_login['access_token']
    
    # Create a project with a very low budget to ensure no bids meet the minimum score
    project_data = {
        'title': 'Admin Flow Test Project',
        'description': 'This project will test admin notification flow',
        'budget': 100000,  # Very low budget
        'location': 'Nairobi, Kenya',
        'category_id': 1,
        'timeline_weeks': 4,
        'max_timeline': 8,
        'requirements': 'Test requirements for admin flow'
    }
    
    response = requests.post(
        f'{BASE_URL}/api/projects',
        headers={'Authorization': f'Bearer {customer_token}'},
        json=project_data
    )
    
    if response.status_code != 201:
        print(f"Failed to create test project: {response.text}")
        return False
    
    project_id = response.json()['data']['project_id']
    print(f"Created low-budget project with ID: {project_id}")
    
    # Create several low-quality professionals who will submit bids below the minimum score
    low_quality_pros = []
    for i in range(3):
        pro = create_test_user(
            email=f'low_quality_pro_{i}@example.com',
            password=TEST_PRO_PASSWORD,
            role=UserRole.PROFESSIONAL,
            name=f'Low Quality Pro {i}',
            company_name=f'Low Quality Construction {i}',
            location='Nairobi, Kenya',
            nca_level=1,  # Very low NCA level
            average_rating=2.0,  # Low rating
            total_ratings=5,
            successful_bids=1,
            total_bids=10  # Low success rate
        )
        low_quality_pros.append(pro)
    
    # Submit low-quality bids that won't meet the minimum score
    for i, pro in enumerate(low_quality_pros):
        pro_login = login_user(pro.email, TEST_PRO_PASSWORD)
        if not pro_login:
            print(f"Failed to log in as professional {pro.email}")
            continue
            
        pro_token = pro_login['access_token']
        
        # Submit bid with high amount (relative to budget) and poor quality
        bid = submit_bid(
            BASE_URL, 
            pro_token, 
            project_id, 
            amount=90000 + (i * 5000),  # High amount for the budget
            timeline_weeks=7,  # Longer than ideal
            proposal=f'Low quality bid from {pro.name}'
        )
        
        if bid:
            print(f"Submitted low-quality bid from {pro.name}")
    
    # Initialize bid automation and set a high minimum score
    bid_automation = BidAutomation()
    bid_automation.min_winning_score = 80  # Set high to ensure no bid meets it
    
    # Run the evaluation
    print("\nEvaluating bids (expecting no automatic acceptance)...")
    with app.app_context():
        await bid_automation.evaluate_project(project_id)
        db.session.commit()
    
    # Add a small delay to ensure all async operations complete
    await asyncio.sleep(1)
    
    # Verify the results
    with app.app_context():
        # Start a new transaction
        db.session.rollback()
        
        # Get the updated project
        project = db.session.get(Job, project_id)
        if not project:
            print("❌ Project not found after evaluation")
            return False
        
        # Check that no bid was accepted
        accepted_bid = db.session.query(Bid).filter_by(
            job_id=project_id, 
            status=BidStatus.ACCEPTED
        ).first()
        
        if accepted_bid:
            print(f"❌ A bid was unexpectedly accepted: {accepted_bid.id}")
            return False
        
        # Check if admin received a notification
        admin_notification = db.session.query(Notification).filter_by(
            notification_type='admin_action_required',
            user_id=admin.id
        ).order_by(Notification.created_at.desc()).first()
        
        if not admin_notification:
            print("❌ Admin was not notified about the need for manual review")
            return False
            
        print(f"✅ Admin was notified about the need for manual review (Notification ID: {admin_notification.id})")
        print(f"Notification content: {admin_notification.message}")
        
        # Now test admin's ability to manually assign the project
        admin_login = login_user('admin_flow_admin@example.com', 'admin123')
        if not admin_login:
            print("❌ Failed to log in as admin")
            return False
            
        # Test admin manual assignment
        print("\nTesting admin manual assignment...")
        
        # Admin assigns the project to a professional
        assigned_professional = db.session.query(User).filter(
            User.role == UserRole.PROFESSIONAL,
            User.id != admin.id
        ).first()
        
        if not assigned_professional:
            print("❌ No professional found for manual assignment")
            return False
            
        # Update project status and assigned contractor
        project.status = JobStatus.AWARDED
        project.contractor_id = assigned_professional.id
        
        # Create a notification for the assigned professional
        pro_notification = Notification(
            user_id=assigned_professional.id,
            title="Project Assigned",
            message=f"You have been assigned to project: {project.title}",
            notification_type="project_assigned",
            content=json.dumps({"project_id": project.id})
        )
        db.session.add(pro_notification)
        
        # Create a notification for the customer
        customer_notification = Notification(
            user_id=project.customer_id,
            title="Professional Assigned",
            message=f"A professional has been assigned to your project: {project.title}",
            notification_type="professional_assigned",
            content=json.dumps({
                "project_id": project.id,
                "professional_id": assigned_professional.id,
                "professional_name": assigned_professional.name
            })
        )
        db.session.add(customer_notification)
        
        db.session.commit()
        
        print(f"✅ Admin manually assigned project to {assigned_professional.name}")
        # Verify the project was updated
        updated_project = db.session.get(Job, project_id)
        if updated_project.status != JobStatus.AWARDED:
            print(f"❌ Project status not updated to AWARDED. Current status: {updated_project.status}")
            return False
            
        if updated_project.contractor_id != assigned_professional.id:
            print(f"❌ Project not assigned to the correct professional. Expected: {assigned_professional.id}, Got: {updated_project.contractor_id}")
            return False
            
        print(f"✅ Project successfully assigned to professional {assigned_professional.name} (ID: {assigned_professional.id})")
        
        # Verify the notification was sent to the assigned professional
        pro_notification = db.session.query(Notification).filter_by(
            user_id=assigned_professional.id,
            notification_type="project_assigned"
        ).order_by(Notification.created_at.desc()).first()
        
        if not pro_notification:
            print("❌ No assignment notification sent to the professional")
            return False
            
        print(f"✅ Professional was notified about the assignment (Notification ID: {pro_notification.id})")
        
        # Verify the customer was notified
        customer_notification = db.session.query(Notification).filter_by(
            user_id=customer.id,
            notification_type="professional_assigned"
        ).order_by(Notification.created_at.desc()).first()
        
        if not customer_notification:
            print("❌ No notification sent to customer about project assignment")
            return False
            
        print(f"✅ Customer was notified about project assignment (Notification ID: {customer_notification.id})")
        
        # For manual assignment, we don't expect any bid to be marked as accepted
        # since we're assigning directly to a professional without accepting a specific bid
        accepted_bid = db.session.query(Bid).filter_by(
            job_id=project_id,
            status=BidStatus.ACCEPTED
        ).first()
        
        if accepted_bid:
            print(f"❌ Expected no bids to be marked as accepted in manual assignment, but found bid {accepted_bid.id}")
            return False
            
        print("✅ No bids were marked as accepted (expected for manual assignment)")
        
        print("\n✅ Admin notification and manual assignment flow test passed!")
        return True

if __name__ == "__main__":
    sys.exit(main())
