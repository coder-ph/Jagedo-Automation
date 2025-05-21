"""
Test utilities and helper functions.
"""
import json
from datetime import datetime, timedelta

def assert_datetime_iso_format(dt_str):
    """Assert that a string is in ISO 8601 format."""
    try:
        datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        return True
    except (ValueError, TypeError):
        return False

def assert_response_structure(response, expected_status_code=200):
    """Assert common response structure and status code."""
    assert response.status_code == expected_status_code, \
        f"Expected status code {expected_status_code}, got {response.status_code}. Response: {response.data}"
    data = response.get_json()
    assert data is not None, "Response data is None"
    assert 'status' in data, f"'status' key missing in response: {data}"
    assert 'message' in data, f"'message' key missing in response: {data}"
    if 'data' in data:
        assert isinstance(data['data'], (dict, list, type(None))), \
            f"'data' should be dict, list or None, got {type(data['data'])}"
    return data

def assert_error_response(response, expected_status_code, expected_message=None):
    """Assert error response structure and content."""
    data = assert_response_structure(response, expected_status_code)
    assert data['status'] == 'error', f"Expected status 'error', got '{data['status']}'"
    if expected_message:
        assert expected_message.lower() in data['message'].lower(), \
            f"Expected message containing '{expected_message}', got '{data['message']}'"
    return data['data'] if 'data' in data else None

def assert_success_response(response, expected_status_code=200):
    """Assert success response structure and content."""
    data = assert_response_structure(response, expected_status_code)
    assert data['status'] == 'success', f"Expected status 'success', got '{data['status']}'"
    return data['data'] if 'data' in data else None

def create_test_user(db_session, **kwargs):
    """Create a test user with the given attributes."""
    from app.models.user import User, UserRole
    
    user_data = {
        'email': 'test@example.com',
        'password': 'testpass123',
        'name': 'Test User',
        'role': UserRole.CUSTOMER,
        'phone': '+1234567890',
        'is_verified': True,
        'location': 'Test Location'
    }
    user_data.update(kwargs)
    
    if 'password' in user_data:
        password = user_data.pop('password')
        user = User.create(**user_data)
        user.password = password
    else:
        user = User.create(**user_data)
        
    db_session.add(user)
    db_session.commit()
    return user

def create_test_job(db_session, customer_id, **kwargs):
    """Create a test job with the given attributes."""
    from app.models.job import Job, JobStatus
    from datetime import datetime, timedelta
    
    job_data = {
        'title': 'Test Job',
        'description': 'Test job description',
        'budget': 1000.00,
        'status': JobStatus.OPEN,
        'customer_id': customer_id,
        'location': 'Test Location',
        'category': 'Test Category',
        'duration_days': 30,
        'start_date': (datetime.utcnow() + timedelta(days=7)).date().isoformat(),
        'end_date': (datetime.utcnow() + timedelta(days=37)).date().isoformat(),
    }
    job_data.update(kwargs)
    
    job = Job(**job_data)
    db_session.add(job)
    db_session.commit()
    return job

def create_test_bid(db_session, job_id, professional_id, **kwargs):
    """Create a test bid with the given attributes."""
    from app.models.bid import Bid, BidStatus
    
    bid_data = {
        'job_id': job_id,
        'professional_id': professional_id,
        'amount': 800.00,
        'message': 'Test bid message',
        'status': BidStatus.PENDING,
        'estimated_days': 25,
    }
    bid_data.update(kwargs)
    
    bid = Bid(**bid_data)
    db_session.add(bid)
    db_session.commit()
    return bid

def get_auth_headers(client, email, password='testpass123'):
    """Get authentication headers for the given user."""
    response = client.post('/api/auth/login', json={
        'email': email,
        'password': password
    })
    assert response.status_code == 200, f"Login failed: {response.data}"
    data = response.get_json()
    assert data is not None, "No JSON response"
    assert 'status' in data, f"'status' key missing in response: {data}"
    assert data['status'] == 'success', f"Login failed: {data.get('message', 'Unknown error')}"
    assert 'data' in data, f"'data' key missing in response: {data}"
    assert 'access_token' in data['data'], f"'access_token' missing in response data: {data['data']}"
    return {
        'Authorization': f'Bearer {data["data"]["access_token"]}',
        'Content-Type': 'application/json'
    }
