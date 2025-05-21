"""
Pytest configuration and fixtures for testing.
"""
import os
import tempfile
import pytest
from werkzeug.security import generate_password_hash
from app import create_app
from app.extensions import db as _db
from app.models import User, Job, Bid, Message, Notification, UserRole
from flask_jwt_extended import create_access_token

@pytest.fixture(scope='session')
def app():
    """Create and configure a new app instance for each test."""
    db_fd, db_path = tempfile.mkstemp()
    
    app = create_app('testing')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    app.config['TESTING'] = True
    
    with app.app_context():
        _db.create_all()
    
    yield app
    
    with app.app_context():
        _db.session.remove()
        _db.drop_all()
    
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def db(app):
    """Provide the transactional fixtures with access to the database."""
    with app.app_context():
        _db.session.begin()
        yield _db
        _db.session.rollback()
        _db.session.close()

@pytest.fixture
def db_session(db):
    """Provides a database session for testing."""
    connection = db.engine.connect()
    transaction = connection.begin()
    
    session_factory = db.sessionmaker(bind=connection)
    session = db.scoped_session(session_factory)
    
    old_session = db.session
    db.session = session
    
    yield session
    
    
    session.remove()
    transaction.rollback()
    connection.close()
    db.session = old_session

@pytest.fixture
def test_customer(db_session):
   
    
    existing_user = User.query.filter_by(email='customer@example.com').first()
    if existing_user:
        db_session.delete(existing_user)
        db_session.commit()
    
    user = User(
        email='customer@example.com',
        _password=generate_password_hash('testpass123'),
        name='Test Customer',
        role=UserRole.CUSTOMER,
        phone='+1234567890',
        is_verified=True,
        location='Test Location',
        company_name='Test Company'
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
def test_professional(db_session):
    
    existing_user = User.query.filter_by(email='professional@example.com').first()
    if existing_user:
        db_session.delete(existing_user)
        db_session.commit()
    
    user = User(
        email='professional@example.com',
        _password=generate_password_hash('testpass123'),
        name='Test Professional',
        role=UserRole.PROFESSIONAL,
        phone='+1987654321',
        is_verified=True,
        location='Test Location',
        company_name='Test Business',
        profile_description='Test Business Description',
        business_name='Test Business',
        business_description='Test Business Description',
        business_address='123 Test St',
        business_phone='+1987654321',
        business_website='https://test.com',
        business_logo='https://test.com/logo.png',
        business_banner='https://test.com/banner.png'
    )
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def test_job(db_session, test_customer):
    """Create a test job."""
    job = Job(
        title='Test Job',
        description='A test job description',
        budget=1000.00,
        status=JobStatus.OPEN,
        customer_id=test_customer.id,
        location='Test Location',
        category='Test Category',
        duration_days=30,
        start_date='2025-06-01',
        end_date='2025-06-30'
    )
    db_session.add(job)
    db_session.commit()
    return job

@pytest.fixture
def test_bid(db_session, test_job, test_professional):
    """Create a test bid."""
    bid = Bid(
        job_id=test_job.id,
        professional_id=test_professional.id,
        amount=800.00,
        message='Test bid message',
        status=BidStatus.PENDING,
        estimated_days=25
    )
    db_session.add(bid)
    db_session.commit()
    return bid

@pytest.fixture
def auth_headers(test_customer, client):
    """Get authentication headers for the test customer."""
    response = client.post('/api/auth/login', json={
        'email': test_customer.email,
        'password': 'testpass123'
    })
    token = response.json['access_token']
    return {
        'Authorization': f'Bearer {token}'
    }
