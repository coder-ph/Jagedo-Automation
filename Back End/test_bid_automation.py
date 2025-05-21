import pytest
import time
import os
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from models import db, User, Job, Bid, JobStatus, BidStatus, UserRole
from bid_automation import BidAutomation
from app import app

# Test configuration
class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'test-secret-key'

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app.config.from_object(TestConfig)
    
    with app.app_context():
        db.create_all()
        
        # Create test data
        customer = User(
            email='customer@test.com',
            password='testpass',
            name='Test Customer',
            role=UserRole.CUSTOMER,
            location='Nairobi, Kenya',
            company_name='Customer Company',
            nca_level=1
        )
        
        contractor1 = User(
            email='contractor1@test.com',
            password='testpass',
            name='Test Contractor 1',
            role=UserRole.PROFESSIONAL,
            location='Nairobi, Kenya',
            company_name='Contractor Company 1',
            nca_level=5,
            average_rating=4.8,
            total_ratings=10,
            successful_bids=8,
            total_bids=10
        )
        
        contractor2 = User(
            email='contractor2@test.com',
            password='testpass',
            name='Test Contractor 2',
            role=UserRole.PROFESSIONAL,
            location='Nairobi, Kenya',
            company_name='Contractor Company 2',
            nca_level=3,
            average_rating=4.2,
            total_ratings=5,
            successful_bids=4,
            total_bids=5
        )
        
        admin = User(
            email='admin@test.com',
            password='testpass',
            name='Test Admin',
            role=UserRole.ADMIN,
            location='Nairobi, Kenya'
        )
        
        project = Job(
            title='Test Project',
            description='Test project description',
            customer_id=1,  # Will be set after user creation
            location='Nairobi, Kenya',
            status=JobStatus.OPEN,
            budget=10000.00,
            max_timeline=12  
        )
        
        db.session.add_all([customer, contractor1, contractor2, admin, project])
        db.session.commit()
        
        
        project.customer_id = customer.id
        db.session.commit()
        
    yield app
    
    # Clean up
    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def automation():
    """Create a BidAutomation instance with test settings."""
    return BidAutomation(min_bids=2, evaluation_period_hours=24)

def test_calculate_bid_score_high_rating(automation, app):
    """Test bid score calculation for a high-rated contractor."""
    with app.app_context():
        # Get test data
        project = Job.query.first()
        contractor = User.query.filter_by(email='contractor1@test.com').first()
        
        # Create a bid
        bid = Bid(
            job_id=project.id,
            professional_id=contractor.id,
            amount=8000.00,
            proposal='Test proposal',
            timeline_weeks=10,
            location_score=0.8,
            location_match_type='city',
            status=BidStatus.PENDING
        )
        
        # Calculate score
        score = automation.calculate_bid_score(bid, project)
        
        # Assert the score is calculated correctly
        # NCA: 5/8 * 40 = 25
        # Rating: 4.8/5 * 30 = 28.8
        # Amount: (10000-8000)/10000 * 20 = 4
        # Timeline: (12-10)/12 * 10 = 1.67
        # Expected: ~59.47
        assert 59 <= score <= 60
        assert score > 50  # Should be a good score

def test_automation_accepts_good_bid(automation, app):
    """Test that a good bid is automatically accepted."""
    with app.app_context():
        # Get test data
        project = Job.query.first()
        contractor = User.query.filter_by(email='contractor1@test.com').first()
        
        # Create a good bid
        bid = Bid(
            job_id=project.id,
            professional_id=contractor.id,
            amount=8000.00,
            proposal='Test proposal',
            timeline_weeks=10,
            location_score=0.9,
            location_match_type='city',
            status=BidStatus.PENDING
        )
        db.session.add(bid)
        db.session.commit()
        
        # Process the bid
        with patch.object(automation, 'accept_bid') as mock_accept_bid:
            # We need to mock the async method
            async def mock_async(*args, **kwargs):
                mock_accept_bid(*args, **kwargs)
            
            with patch('bid_automation.BidAutomation.accept_bid', new=mock_async):
                import asyncio
                asyncio.run(automation.evaluate_project(project.id))
        
        # Verify the bid was accepted
        mock_accept_bid.assert_called_once()
        accepted_bid = mock_accept_bid.call_args[0][0]
        assert accepted_bid.id == bid.id

def test_automation_notifies_admin_on_low_scores(automation, app):
    """Test that admin is notified when no bids meet the minimum score."""
    with app.app_context():
        # Get test data
        project = Job.query.first()
        contractor = User.query.filter_by(email='contractor2@test.com').first()
        
        # Create a low-scoring bid
        bid = Bid(
            job_id=project.id,
            professional_id=contractor.id,
            amount=9500.00,  # High amount
            proposal='Test proposal',
            timeline_weeks=15,  # Slow timeline
            location_score=0.3,  # Low location score
            location_match_type='country',
            status=BidStatus.PENDING
        )
        db.session.add(bid)
        db.session.commit()
        
        # Process the bid
        with patch.object(automation, 'notify_admin_manual_review') as mock_notify:
            # We need to mock the async method
            async def mock_async(*args, **kwargs):
                mock_notify(*args, **kwargs)
            
            with patch('bid_automation.BidAutomation.notify_admin_manual_review', new=mock_async):
                import asyncio
                asyncio.run(automation.evaluate_project(project.id))
        
        # Verify admin was notified
        mock_notify.assert_called_once()
        called_project = mock_notify.call_args[0][0]
        called_bid = mock_notify.call_args[0][1]
        called_score = mock_notify.call_args[0][2]
        
        assert called_project.id == project.id
        assert called_bid.id == bid.id
        assert called_score < 60  # Should be below minimum winning score

def test_automation_waits_for_min_bids(automation, app):
    """Test that evaluation waits for minimum number of bids."""
    with app.app_context():
        # Get test data
        project = Job.query.first()
        contractor = User.query.filter_by(email='contractor1@test.com').first()
        
        # Create first bid
        bid1 = Bid(
            job_id=project.id,
            professional_id=contractor.id,
            amount=8000.00,
            proposal='Test proposal 1',
            timeline_weeks=10,
            location_score=0.9,
            location_match_type='city',
            status=BidStatus.PENDING
        )
        db.session.add(bid1)
        db.session.commit()
        
        # Process the bid
        with patch.object(automation, 'evaluate_project') as mock_evaluate:
            automation.handle_new_bid(bid1.id)
            
            # Should not evaluate yet (min_bids=2)
            mock_evaluate.assert_not_called()
            
            # Create second bid
            bid2 = Bid(
                job_id=project.id,
                professional_id=contractor.id + 1,  # Different contractor
                amount=8500.00,
                proposal='Test proposal 2',
                timeline_weeks=11,
                location_score=0.8,
                location_match_type='city',
                status=BidStatus.PENDING
            )
            db.session.add(bid2)
            db.session.commit()
            
            # Now it should evaluate
            automation.handle_new_bid(bid2.id)
            mock_evaluate.assert_called_once_with(project.id)

def test_automation_evaluates_after_timeout(automation, app):
    """Test that evaluation happens after timeout even without enough bids."""
    with app.app_context():
        # Get test data
        project = Job.query.first()
        contractor = User.query.filter_by(email='contractor1@test.com').first()
        
        # Create a single bid
        bid = Bid(
            job_id=project.id,
            professional_id=contractor.id,
            amount=8000.00,
            proposal='Test proposal',
            timeline_weeks=10,
            location_score=0.9,
            location_match_type='city',
            status=BidStatus.PENDING
        )
        db.session.add(bid)
        
        # Set project creation time to 25 hours ago
        project.created_at = datetime.utcnow() - timedelta(hours=25)
        db.session.commit()
        
        # Process the bid
        with patch.object(automation, 'evaluate_project') as mock_evaluate:
            automation.handle_new_bid(bid.id)
            
            # Should evaluate immediately due to timeout
            mock_evaluate.assert_called_once_with(project.id)
