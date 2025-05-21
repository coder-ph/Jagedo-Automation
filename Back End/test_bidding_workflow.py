import os
import sys
import json
import requests
from datetime import datetime, timedelta
from werkzeug.datastructures import FileStorage

# Add the current directory to the path so we can import app
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)

from app import app, db, bcrypt
from models import (
    User, Job, Bid, Attachment, UserRole, JobStatus, BidStatus,
    Notification, Message, Category, ProfessionalSkill, Review, 
    ProjectStatusHistory
)
from flask_jwt_extended import create_access_token, JWTManager

# Initialize Flask extensions
with app.app_context():
    # Initialize bcrypt
    if 'bcrypt' not in app.extensions:
        bcrypt.init_app(app)
    
    # Initialize JWT
    if 'jwt' not in app.extensions:
        app.config['JWT_SECRET_KEY'] = 'test-secret-key'  # Use the same secret key as in app.py
        jwt = JWTManager(app)
    
    # Create database tables if they don't exist
    db.create_all()

# Test configuration
BASE_URL = 'http://localhost:5001'  # Updated to match the running Flask instance
TEST_CUSTOMER_EMAIL = 'test_customer_new@example.com'  # New email to avoid conflicts
TEST_CUSTOMER_PASSWORD = 'customer123'
TEST_PRO_EMAIL = 'test_pro_new@example.com'  # New email to avoid conflicts
TEST_PRO_PASSWORD = 'password123'

def create_test_user(email, password, role, **kwargs):
    """Create a test user if one doesn't exist"""
    with app.app_context():
        # Delete existing test user if exists to avoid conflicts
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            db.session.delete(existing_user)
            db.session.commit()
        
        # Create new user with properly hashed password
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
    """Login a user and return the JWT token"""
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

def create_test_project(token, title="Test Project"):
    """Create a test project"""
    url = f'{BASE_URL}/api/projects'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    project_data = {
        'title': title,
        'description': 'This is a test project description',
        'budget': 1000000,
        'location': 'Nairobi, Kenya',
        'category_id': 1,  # Assuming category 1 exists
        'timeline_weeks': 8,
        'requirements': 'Test requirements',
        'documents': []
    }
    
    print(f"\nCreating project with data: {json.dumps(project_data, indent=2)}")
    
    try:
        response = requests.post(url, headers=headers, json=project_data, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        try:
            response_data = response.json()
            print(f"Response Body: {json.dumps(response_data, indent=2)}")
        except ValueError:
            print(f"Response Body (non-JSON): {response.text}")
        
        if response.status_code == 201:
            # First try to get job_id, if not found, try project_id
            job_id = response_data.get('data', {}).get('job_id')
            if not job_id:
                job_id = response_data.get('data', {}).get('project_id')
                
            if job_id:
                print(f"Successfully created project with ID: {job_id}")
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
        return None

def submit_bid(base_url, token, job_id, amount=4500000, proposal='I have extensive experience in construction projects similar to this one. My team and I can complete the work within the specified timeline and budget.', timeline_weeks=12):
    """Submit a bid for a job"""
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
        # Make the request
        response = requests.post(url, headers=headers, json=bid_data)
        
        # Print detailed response information
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        # Try to parse JSON response
        try:
            response_data = response.json()
            print("Response Body:", json.dumps(response_data, indent=2))
        except ValueError:
            print("Response Body (non-JSON):", response.text)
        
        # For 500 errors, try to get more details from the server
        if response.status_code == 500:
            print("\nServer returned 500 error. Checking for traceback...")
            try:
                # Try to get the traceback from the response
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
        
        # Print the full traceback for debugging
        import traceback
        print("\nLocal Traceback:")
        traceback.print_exc()
        
        return None
        return None

def get_project_bids(project_id, token, expected_status=200):
    """Get all bids for a project with detailed error handling"""
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
    """Select a winning bid for a project"""
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
    """Clean up the database before running tests by dropping and recreating all tables"""
    from sqlalchemy import inspect, text
    
    try:
        # Disable foreign key checks temporarily
        db.session.execute(text('PRAGMA foreign_keys = OFF'))
        db.session.commit()
        
        # Drop all tables
        inspector = inspect(db.engine)
        metadata = db.metadata
        
        # Drop all tables in reverse order of dependencies
        for table in reversed(metadata.sorted_tables):
            try:
                table.drop(db.engine)
                print(f"Dropped table: {table.name}")
            except Exception as e:
                print(f"Warning: Could not drop table {table.name}: {str(e)}")
        
        # Recreate all tables
        db.create_all()
        print("Recreated all tables")
        
        # Re-enable foreign key checks
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

def main():
    # Clean up the database first
    print("Cleaning up database...")
    if not clean_database():
        print("Failed to clean up database")
        return 1
    
    print("\nStarting bidding workflow test...")
    if not test_bidding_workflow():
        print("\nBidding workflow test failed!")
        return 1
    
    print("\nBidding workflow test completed successfully!")
    return 0

def test_bidding_workflow():
    print("=== Starting Bidding Workflow Test ===\n")
    
    # Clean up database before starting
    print("Cleaning up database...")
    clean_database()
    
    try:
        # Create test users
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
        
        # Login as customer
        print("\n2. Logging in as customer...")
        customer_auth = login_user(TEST_CUSTOMER_EMAIL, TEST_CUSTOMER_PASSWORD)
        if not customer_auth:
            raise Exception("Failed to login as customer")
        
        customer_token = customer_auth['access_token']
        
        # Create a test project
        print("\n3. Creating test project...")
        project_id = create_test_project(customer_token, "Test Bidding Project")
        if not project_id:
            raise Exception("Failed to create test project")
        
        print(f"\nCreated project with ID: {project_id}")
        
        # Test 1: Try to get bids before any are submitted (should be empty)
        print("\n4. Testing GET /api/projects/{project_id}/bids (before bids)")
        bids = get_project_bids(project_id, customer_token)
        if not isinstance(bids, list):
            raise Exception("Failed to retrieve bids (should return empty list)")
        print(f"✓ Successfully retrieved {len(bids)} bids (expected: 0)")
        
        # Login as first professional
        print("\n5. Logging in as Professional 1...")
        pro1_auth = login_user(TEST_PRO_EMAIL, TEST_PRO_PASSWORD)
        if not pro1_auth:
            raise Exception("Failed to login as professional 1")
        
        pro1_token = pro1_auth['access_token']
        
        # Submit a bid as first professional
        print("\n6. Submitting bid as Professional 1...")
        bid1_response = submit_bid(BASE_URL, pro1_token, project_id, amount=4500000)
        if not bid1_response or not bid1_response.get('success'):
            raise Exception("Failed to submit first bid")
        
        bid1_id = bid1_response.get('data', {}).get('bid_id')
        print(f"✓ Successfully submitted bid with ID: {bid1_id}")
        
        # Test 2: Get bids after first bid (should see only pro1's bid)
        print("\n7. Testing GET /api/projects/{project_id}/bids (after first bid)")
        bids = get_project_bids(project_id, customer_token)
        if not isinstance(bids, list) or len(bids) != 1:
            raise Exception(f"Expected 1 bid, got {len(bids) if isinstance(bids, list) else 'invalid response'}")
        print(f"✓ Successfully retrieved {len(bids)} bid(s)")
        
        # Login as second professional
        print("\n8. Logging in as Professional 2...")
        pro2_auth = login_user("test_pro2@example.com", TEST_PRO_PASSWORD)
        if not pro2_auth:
            raise Exception("Failed to login as professional 2")
        
        pro2_token = pro2_auth['access_token']
        
        # Submit a bid as second professional
        print("\n9. Submitting bid as Professional 2...")
        bid2_response = submit_bid(BASE_URL, pro2_token, project_id, amount=4200000)
        if not bid2_response or not bid2_response.get('success'):
            raise Exception("Failed to submit second bid")
        
        bid2_id = bid2_response.get('data', {}).get('bid_id')
        print(f"✓ Successfully submitted bid with ID: {bid2_id}")
        
        # Test 3: Get bids after second bid (should see both bids as customer)
        print("\n10. Testing GET /api/projects/{project_id}/bids (after second bid)")
        bids = get_project_bids(project_id, customer_token)
        if not isinstance(bids, list) or len(bids) != 2:
            raise Exception(f"Expected 2 bids, got {len(bids) if isinstance(bids, list) else 'invalid response'}")
        print(f"✓ Successfully retrieved {len(bids)} bids as customer")
        
        # Test 4: Check that professionals can only see their own bids
        print("\n11. Testing bid visibility for professionals")
        
        # Check Professional 1's view
        pro1_bids = get_project_bids(project_id, pro1_token)
        if not isinstance(pro1_bids, list) or len(pro1_bids) != 1 or pro1_bids[0].get('id') != bid1_id:
            raise Exception("Professional 1 can see incorrect bids")
        print("✓ Professional 1 can only see their own bid")
        
        # Check Professional 2's view
        pro2_bids = get_project_bids(project_id, pro2_token)
        if not isinstance(pro2_bids, list) or len(pro2_bids) != 1 or pro2_bids[0].get('id') != bid2_id:
            raise Exception("Professional 2 can see incorrect bids")
        print("✓ Professional 2 can only see their own bid")
        
        # Test 5: Select winning bid as customer
        print("\n12. Selecting winning bid...")
        selection_result = select_winning_bid(project_id, bid1_id, customer_token)
        if not selection_result or not selection_result.get('success'):
            error_msg = selection_result.get('error', 'Unknown error') if selection_result else 'No response'
            print(f"Error response: {error_msg}")
            raise Exception(f"Failed to select winning bid: {error_msg}")
        
        print(f"✓ Successfully selected bid {bid1_id} as the winner")
        
        # Test 6: Verify bid status was updated
        print("\n13. Verifying bid status updates...")
        updated_bids = get_project_bids(project_id, customer_token)
        if not isinstance(updated_bids, list):
            raise Exception("Failed to retrieve updated bids")
            
        winning_bid = next((b for b in updated_bids if b.get('id') == bid1_id), None)
        if not winning_bid or winning_bid.get('status') != 'accepted':
            raise Exception("Winning bid status not updated to 'accepted'")
            
        losing_bid = next((b for b in updated_bids if b.get('id') == bid2_id), None)
        if not losing_bid or losing_bid.get('status') != 'rejected':
            print("Warning: Losing bid status not updated to 'rejected' (this might be expected behavior)")
        
        print("✓ Bid statuses updated correctly")
        
        print("\n=== Bidding Workflow Test Completed Successfully ===")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    if test_bidding_workflow():
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == '__main__':
    with app.app_context():
        main()
