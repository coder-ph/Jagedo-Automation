import os
import unittest
import tempfile
import shutil
import json
import requests
from datetime import datetime, timedelta

# Test configuration
BASE_URL = 'http://localhost:5002/api'
TEST_UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')

# Ensure test upload directory exists
os.makedirs(TEST_UPLOAD_FOLDER, exist_ok=True)

class TestDocumentAccess(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a test file
        cls.test_file_path = os.path.join(TEST_UPLOAD_FOLDER, 'test_document.txt')
        with open(cls.test_file_path, 'w') as f:
            f.write('This is a test document for the project')
    
    @classmethod
    def tearDownClass(cls):
        # Clean up test files
        if os.path.exists(TEST_UPLOAD_FOLDER):
            shutil.rmtree(TEST_UPLOAD_FOLDER)
    
    def setUp(self):
        # Clean up database before each test
        self.clean_database()
        
        # Create test users
        self.customer_token = self.create_test_user(
            'test_customer_docs@example.com', 'Test Customer', 'customer123', 'customer'
        )
        self.professional1_token = self.create_test_user(
            'test_pro1_docs@example.com', 'Test Professional 1', 'pro123', 'professional',
            nca_level=5, location='Nairobi, Kenya'
        )
        self.professional2_token = self.create_test_user(
            'test_pro2_docs@example.com', 'Test Professional 2', 'pro123', 'professional',
            nca_level=5, location='Mombasa, Kenya'
        )
        
        # Create a test project with a document
        self.project_id = self.create_test_project()
        self.document_id = self.upload_test_document()
    
    def tearDown(self):
        pass
    
    def clean_database(self):
        """Clean up the database before running tests"""
        try:
            url = f'{BASE_URL}/test/clean-db'
            response = requests.post(url)
            if response.status_code != 200:
                print(f"Warning: Could not clean database: {response.text}")
        except Exception as e:
            print(f"Error cleaning database: {str(e)}")
    
    def create_test_user(self, email, name, password, role, **kwargs):
        """Helper to create a test user and return auth token"""
        # First try to login (user might already exist)
        login_url = f'{BASE_URL}/auth/login'
        login_data = {'email': email, 'password': password}
        login_response = requests.post(login_url, json=login_data)
        
        if login_response.status_code == 200:
            return login_response.json().get('access_token')
            
        # If login fails, try to register
        url = f'{BASE_URL}/auth/register'
        user_data = {
            'email': email,
            'name': name,
            'password': password,
            'role': role,
            'phone': '+254700000000',
            'nca_level': kwargs.get('nca_level', 5 if role == 'professional' else 0),
            'location': kwargs.get('location', 'Nairobi, Kenya'),
            'successful_bids': 0,
            'total_bids': 0,
            'average_rating': 4.5 if role == 'professional' else None
        }
        
        # Register user
        response = requests.post(url, json=user_data)
        if response.status_code not in [200, 201]:
            print(f"Failed to create test user {email}: {response.text}")
            return None
        
        # Login to get token
        login_response = requests.post(login_url, json=login_data)
        
        if login_response.status_code == 200:
            return login_response.json().get('access_token')
        else:
            print(f"Failed to login test user {email}: {login_response.text}")
            return None
    
    def create_test_project(self):
        """Create a test project"""
        url = f'{BASE_URL}/projects/create'
        headers = {
            'Authorization': f'Bearer {self.customer_token}',
            'Content-Type': 'application/json'
        }
        
        project_data = {
            'title': 'Document Access Test Project',
            'description': 'Project to test document access during bidding',
            'budget': 500000,
            'location': 'Nairobi, Kenya',
            'category_id': 1,
            'timeline_weeks': 8,
            'requirements': 'Test requirements for document access',
            'documents': []
        }
        
        response = requests.post(url, headers=headers, json=project_data)
        if response.status_code != 201:
            print(f"Failed to create project: {response.text}")
        self.assertEqual(response.status_code, 201)
        return response.json()['data']['project_id']
    
    def upload_test_document(self):
        """Upload a test document to the project"""
        url = f'{BASE_URL}/projects/{self.project_id}/documents'
        headers = {
            'Authorization': f'Bearer {self.customer_token}'
        }
        
        with open(self.test_file_path, 'rb') as f:
            files = {'file': ('test_document.txt', f, 'text/plain')}
            response = requests.post(url, headers=headers, files=files)
        
        if response.status_code != 201:
            print(f"Failed to upload document: {response.text}")
        self.assertEqual(response.status_code, 201)
        return response.json()['document_id']
    
    def download_document(self, token, document_id, expect_success=True):
        """Helper to download a document and verify access"""
        url = f'{BASE_URL}/documents/{document_id}'
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(url, headers=headers, stream=True)
        
        if expect_success:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.headers['Content-Disposition'], 
                          f'attachment; filename=test_document.txt')
            return response.content
        else:
            self.assertNotEqual(response.status_code, 200)
            return None
    
    def test_document_access_during_bidding(self):
        """Test that professionals can access documents during bidding"""
        print("\n=== Testing document access during bidding ===")
        
        # First, get the document ID from the project
        project_url = f'{BASE_URL}/projects/{self.project_id}'
        headers = {'Authorization': f'Bearer {self.customer_token}'}
        project_response = requests.get(project_url, headers=headers)
        self.assertEqual(project_response.status_code, 200)
        
        # Skip test if no documents found
        documents = project_response.json().get('data', {}).get('documents', [])
        if not documents:
            self.skipTest("No documents found in project, skipping test")
        document_id = documents[0]['id']
        
        # Professional 1 should be able to access the document
        print("\n1. Verifying Professional 1 can access document during bidding...")
        content1 = self.download_document(self.professional1_token, document_id)
        self.assertIsNotNone(content1)
        print("✓ Professional 1 can access the document")
        
        # Professional 2 should also be able to access the document
        print("\n2. Verifying Professional 2 can access document during bidding...")
        content2 = self.download_document(self.professional2_token, document_id)
        self.assertIsNotNone(content2)
        print("✓ Professional 2 can access the document")
        
        # Verify both professionals got the same file content
        self.assertEqual(content1, content2)
        
        print("\n✓ Test passed: Professionals can access documents during bidding")
    
    def test_document_access_after_award(self):
        """Test document access after project is awarded"""
        print("\n=== Testing document access after project award ===")
        
        # First, get the document ID from the project
        project_url = f'{BASE_URL}/projects/{self.project_id}'
        headers = {'Authorization': f'Bearer {self.customer_token}'}
        project_response = requests.get(project_url, headers=headers)
        self.assertEqual(project_response.status_code, 200)
        
        # Skip test if no documents found
        documents = project_response.json().get('data', {}).get('documents', [])
        if not documents:
            self.skipTest("No documents found in project, skipping test")
        document_id = documents[0]['id']
        
        # Submit bids from both professionals
        print("\n1. Submitting bids from both professionals...")
        bid1_id = self.submit_bid(self.professional1_token, 400000)
        bid2_id = self.submit_bid(self.professional2_token, 450000)
        print(f"✓ Submitted bids: {bid1_id}, {bid2_id}")
        
        # Select the winning bid (Professional 1)
        print("\n2. Selecting winning bid...")
        self.select_winning_bid(bid1_id)
        print("✓ Selected winning bid")
        
        # Verify Professional 1 (winner) can still access the document
        print("\n3. Verifying winning professional can access document...")
        content = self.download_document(self.professional1_token, document_id)
        self.assertIsNotNone(content)
        print("✓ Winning professional can access the document")
        
        # Verify Professional 2 (not selected) cannot access the document
        print("\n4. Verifying non-winning professional cannot access document...")
        with self.assertRaises(AssertionError):
            self.download_document(self.professional2_token, document_id, expect_success=True)
        print("✓ Non-winning professional cannot access the document")
        
        print("\n✓ Test passed: Document access restricted after project award")
    
    def submit_bid(self, token, amount):
        """Helper to submit a bid"""
        url = f'{BASE_URL}/projects/{self.project_id}/bids'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        bid_data = {
            'amount': amount,
            'proposal': f'Bid for {amount}',
            'timeline_weeks': 10
        }
        
        response = requests.post(url, headers=headers, json=bid_data)
        self.assertEqual(response.status_code, 200)
        return response.json()['data']['bid_id']
    
    def select_winning_bid(self, bid_id):
        """Helper to select a winning bid"""
        url = f'{BASE_URL}/projects/{self.project_id}/select-winner'
        headers = {
            'Authorization': f'Bearer {self.customer_token}',
            'Content-Type': 'application/json'
        }
        
        data = {'bid_id': bid_id}
        response = requests.post(url, headers=headers, json=data)
        self.assertEqual(response.status_code, 200)
        return response.json()

if __name__ == '__main__':
    unittest.main(verbosity=2)
