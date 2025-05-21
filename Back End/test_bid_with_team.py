import unittest
import json
import os
import sys
import time
sys.path.append(os.path.abspath('.'))

from app import app, db
from models import User, Job, Bid, BidTeamMember, UserRole, JobStatus, BidStatus
from datetime import datetime, timedelta, timezone
import bcrypt

class TestBidWithTeam(unittest.TestCase):    
    def setUp(self):
        """Set up test variables and initialize app."""
        # Configure test database
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        
        self.app = app
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Create test database
        with self.app.app_context():
            db.drop_all()
            db.create_all()
        
        # Create test users with unique emails based on timestamp
        timestamp = int(time.time())
        self.customer_email = f'customer{timestamp}@test.com'
        self.contractor_email = f'contractor{timestamp}@test.com'
        
        self.customer = self.create_user(
            email=self.customer_email,
            password='testpass123',
            role=UserRole.CUSTOMER,
            name='Test Customer',
            company_name='Customer Inc.',
            location='Nairobi, Kenya'
        )
        
        self.contractor = self.create_user(
            email=self.contractor_email,
            password='testpass123',
            role=UserRole.PROFESSIONAL,
            name='Test Contractor',
            company_name='Contractor Co.',
            location='Nairobi, Kenya'
        )
        
        # Create a test project
        self.project = Job(
            title='Test Project',
            description='Test project description',
            budget=10000,
            location='Nairobi, Kenya',
            status=JobStatus.OPEN,
            customer_id=self.customer.id,
            created_at=datetime.now(timezone.utc),
        )
        db.session.add(self.project)
        db.session.commit()
        
        # Get auth tokens
        self.customer_token = self.authenticate(self.customer_email, 'testpass123')
        self.contractor_token = self.authenticate(self.contractor_email, 'testpass123')
    
    def tearDown(self):
        """Clean up after each test."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
        self.app_context.pop()
    
    def create_user(self, email, password, role, **kwargs):
        """Helper method to create a user."""
        user = User(
            email=email,
            password_hash=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            role=role,
            **kwargs
        )
        db.session.add(user)
        db.session.commit()
        return user
    
    def authenticate(self, email, password):
        """Helper method to authenticate a user and get token."""
        response = self.client.post(
            '/api/login',
            data=json.dumps({
                'email': email,
                'password': password
            }),
            content_type='application/json'
        )
        data = json.loads(response.data)
        if not data.get('success'):
            print(f"Login failed. Response: {data}")
            return None
            
        # The access token is in data.data.access_token
        return data['data']['access_token']
    
    def test_submit_bid_with_team_members(self):
        """Test submitting a bid with team members."""
        # Prepare team members data
        team_members = [
            {
                'email': 'team1@example.com',
                'name': 'John Doe',
                'role': 'Lead Developer',
                'hourly_rate': 50,
                'hours': 40
            },
            {
                'email': 'team2@example.com',
                'name': 'Jane Smith',
                'role': 'UI/UX Designer',
                'hourly_rate': 45,
                'hours': 30
            }
        ]
        
        # Submit bid with team members
        bid_data = {
            'amount': 5000,
            'proposal': 'Test proposal with team',
            'timeline_weeks': 4,
            'team_members': team_members
        }
        
        response = self.client.post(
            f'/api/projects/{self.project.id}/bids',
            headers={'Authorization': f'Bearer {self.contractor_token}', 'Content-Type': 'application/json'},
            json=bid_data
        )
        
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200, 
                         f"Expected status code 200, got {response.status_code}. Response: {response_data}")
        self.assertTrue(response_data['success'], 
                      f"Expected success: true, got {response_data}. Response: {response_data}")
        self.assertIn('data', response_data, 
                     f"Expected 'data' in response. Response: {response_data}")
        self.assertIn('bid_id', response_data['data'], 
                     f"Expected 'bid_id' in response data. Response: {response_data}")
        self.assertEqual(response_data['data'].get('team_members_count', 0), 2,
                         f"Expected 2 team members. Response: {response_data}")
        
        # Verify the bid was created with team members
        bid = db.session.get(Bid, response_data['data']['bid_id'])
        self.assertIsNotNone(bid)
        self.assertEqual(len(bid.team_members), 2)
        
        # Verify team members data
        for i, member in enumerate(team_members):
            self.assertEqual(bid.team_members[i].email, member['email'])
            self.assertEqual(bid.team_members[i].name, member['name'])
            self.assertEqual(bid.team_members[i].role, member['role'])
            self.assertEqual(float(bid.team_members[i].hourly_rate), member['hourly_rate'])
            self.assertEqual(bid.team_members[i].hours, member['hours'])
            self.assertEqual(
                float(bid.team_members[i].total_cost),
                member['hourly_rate'] * member['hours']
            )
    
    def test_get_bids_with_team_members(self):
        """Test retrieving bids with team members."""
        # First, submit a bid with team members
        team_members = [
            {
                'email': 'team1@example.com',
                'name': 'John Doe',
                'role': 'Lead Developer',
                'hourly_rate': 50,
                'hours': 40
            }
        ]
        
        bid_data = {
            'amount': 5000,
            'proposal': 'Test proposal with team',
            'timeline_weeks': 4,
            'team_members': team_members
        }
        
        # Submit the bid
        response = self.client.post(
            f'/api/projects/{self.project.id}/bids',
            headers={'Authorization': f'Bearer {self.contractor_token}', 'Content-Type': 'application/json'},
            json=bid_data
        )
        
        self.assertEqual(response.status_code, 200, f"Expected status code 200, got {response.status_code}. Response: {response.data}")
        data = json.loads(response.data)
        self.assertTrue(data['success'], f"Expected success: true, got {data}")
        self.assertIn('data', data, f"Expected 'data' in response. Response: {data}")
        self.assertIn('bid_id', data['data'], f"Expected 'bid_id' in response data. Response: {data}")
        bid_id = data['data']['bid_id']
        
        # Now get the project's bids and verify team members are included
        response = self.client.get(
            f'/api/projects/{self.project.id}/bids',
            headers={'Authorization': f'Bearer {self.customer_token}'}
        )
        
        self.assertEqual(response.status_code, 200, 
                         f"Expected status code 200, got {response.status_code}. Response: {response.data}")
        data = json.loads(response.data)
        self.assertTrue(data['success'], 
                      f"Expected success: true, got {data}")
        self.assertIn('data', data, 
                     f"Expected 'data' in response. Response: {data}")
        bids = data['data']
        self.assertGreater(len(bids), 0, 
                         f"Expected at least one bid. Response: {data}")
        bid = bids[0]  # Get the first bid
        self.assertEqual(len(bid.get('team_members', [])), 1,
                         f"Expected 1 team member. Response: {bid}")
        self.assertEqual(bid['team_members'][0]['name'], 'John Doe',
                         f"Expected team member name 'John Doe'. Response: {bid}")
        
        # Verify team members are included in the response
        self.assertIn('team_members', bid)
        self.assertEqual(len(bid['team_members']), 1)
        team_member = bid['team_members'][0]
        self.assertEqual(team_member['email'], team_members[0]['email'])
        self.assertEqual(team_member['name'], team_members[0]['name'])
        self.assertEqual(team_member['role'], team_members[0]['role'])
        self.assertEqual(team_member['hourly_rate'], team_members[0]['hourly_rate'])
        self.assertEqual(team_member['hours'], team_members[0]['hours'])
        self.assertEqual(
            team_member['total_cost'],
            team_members[0]['hourly_rate'] * team_members[0]['hours']
        )

if __name__ == '__main__':
    unittest.main()
