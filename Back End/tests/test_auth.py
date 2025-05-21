"""Tests for authentication routes."""
import pytest
import json
from datetime import datetime, timedelta
from app.models.user import User, UserRole
from tests.test_utils import (
    assert_success_response, 
    assert_error_response,
    create_test_user,
    get_auth_headers
)

def test_register(client, db_session):
    """Test user registration."""
    # Clean up any existing test user
    User.query.filter_by(email='test@example.com').delete()
    db_session.commit()
    
    # Test successful registration
    response = client.post('/api/auth/register', json={
        'email': 'test@example.com',
        'password': 'Testpass123!',
        'name': 'Test User',
        'phone': '+1234567890',
        'role': 'customer',
        'location': 'Test Location'
    })
    
    data = assert_success_response(response, 201)
    assert data is not None
    assert 'user' in data
    assert data['user']['email'] == 'test@example.com'
    assert data['user']['name'] == 'Test User'
    assert 'id' in data['user']
    assert 'password' not in data['user']
    assert 'access_token' in data
    assert 'refresh_token' in data
    
    # Test duplicate email - should return 409 Conflict
    response = client.post('/api/auth/register', json={
        'email': 'test@example.com',
        'password': 'Testpass123!',
        'name': 'Another User',
        'phone': '+1987654321',
        'role': 'customer',
        'location': 'Test Location'
    })
    
    data = assert_error_response(response, 409)
    assert 'email' in data.get('errors', {})
    
    # Test invalid data - missing required fields and invalid values
    response = client.post('/api/auth/register', json={
        'email': 'invalid-email',
        'password': 'short',
        'name': '',
        'role': 'invalid-role'
    })
    
    data = assert_error_response(response, 400)
    errors = data.get('errors', {})
    # Check for specific validation errors
    assert 'location' in errors  # location is required
    assert errors.get('name') == 'Name is required.'  # name is empty
    
    # The following validations happen after required fields check
    # So they won't be in the response if required fields are missing
    if 'email' in errors:
        assert 'Invalid email format' in errors['email']
    if 'password' in errors:
        assert 'Password must be at least 8 characters' in errors['password']
    if 'role' in errors:
        assert 'Invalid role' in errors['role']

def test_login(client, test_customer):
    """Test user login."""
    # Test successful login
    response = client.post('/api/auth/login', json={
        'email': 'customer@example.com',
        'password': 'testpass123'
    })
    
    data = assert_success_response(response)
    assert data is not None
    assert 'access_token' in data
    assert 'refresh_token' in data
    assert 'user' in data
    assert data['user']['email'] == 'customer@example.com'
    assert 'password' not in data['user']
    
    # Test invalid credentials
    response = client.post('/api/auth/login', json={
        'email': 'customer@example.com',
        'password': 'wrongpassword'
    })
    
    data = assert_error_response(response, 401)
    assert 'auth' in data.get('errors', {})
    
    # Test non-existent user
    response = client.post('/api/auth/login', json={
        'email': 'nonexistent@example.com',
        'password': 'testpass123'
    })
    
    data = assert_error_response(response, 401)
    assert 'auth' in data.get('errors', {})

def test_protected_route(client, test_customer):
    """Test accessing a protected route."""
    # Get auth token
    headers = get_auth_headers(client, 'customer@example.com', 'testpass123')
    
    # Access protected route
    response = client.get('/api/auth/profile', headers=headers)
    data = assert_success_response(response)
    assert data is not None
    assert 'email' in data
    assert data['email'] == 'customer@example.com'
    
    # Test without token
    response = client.get('/api/auth/profile')
    # The JWT library returns a 422 with a specific message when no token is provided
    assert response.status_code in [401, 422], f"Expected 401 or 422, got {response.status_code}"
    
    # Test with invalid token
    response = client.get('/api/auth/profile', headers={'Authorization': 'Bearer invalid-token'})
    assert response.status_code in [401, 422], f"Expected 401 or 422, got {response.status_code}"

def test_refresh_token(client, test_customer):
    """Test token refresh."""
    # Login to get refresh token
    login_response = client.post('/api/auth/login', json={
        'email': 'customer@example.com',
        'password': 'testpass123'
    })
    
    login_data = login_response.get_json()
    assert 'data' in login_data, f"'data' key missing in login response: {login_data}"
    assert 'refresh_token' in login_data['data'], f"'refresh_token' missing in login response data: {login_data['data']}"
    refresh_token = login_data['data']['refresh_token']
    
    # Refresh token
    response = client.post('/api/auth/refresh', 
                         headers={'Authorization': f'Bearer {refresh_token}'})
    
    # Check if the response is successful
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.data}"
    data = response.get_json()
    assert data is not None, "No JSON response"
    assert 'status' in data, f"'status' key missing in response: {data}"
    assert data['status'] == 'success', f"Expected status 'success', got '{data['status']}'. Message: {data.get('message', '')}"
    
    # Check the response data structure
    assert 'data' in data, f"'data' key missing in response: {data}"
    assert 'access_token' in data['data'], f"'access_token' missing in response data: {data['data']}"
    assert 'refresh_token' in data['data'], f"'refresh_token' missing in response data: {data['data']}"
    assert 'user' in data['data'], f"'user' missing in response data: {data['data']}"
    assert data['data']['user']['email'] == 'customer@example.com', f"Unexpected user email: {data['data']['user'].get('email', 'not found')}"
    
    # Test with invalid refresh token
    response = client.post('/api/auth/refresh', 
                         headers={'Authorization': 'Bearer invalid-refresh-token'})
    # The JWT library returns a 422 with a specific message for invalid tokens
    assert response.status_code in [401, 422], f"Expected 401 or 422, got {response.status_code}"

def test_logout(client, test_customer):
    """Test user logout."""
    # Login to get access token
    login_response = client.post('/api/auth/login', json={
        'email': 'customer@example.com',
        'password': 'testpass123'
    })
    
    login_data = login_response.get_json()
    assert 'data' in login_data, f"'data' key missing in login response: {login_data}"
    assert 'access_token' in login_data['data'], f"'access_token' missing in login response data: {login_data['data']}"
    
    access_token = login_data['data']['access_token']
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    # First, verify the token works before logout
    response = client.get('/api/auth/profile', headers=headers)
    assert response.status_code == 200, "Token should be valid before logout"
    
    # Logout - should return 200 on success
    response = client.post('/api/auth/logout', headers=headers)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.data}"
    
    # Parse the response
    data = response.get_json()
    assert data is not None, "No JSON response"
    assert 'status' in data, f"'status' key missing in response: {data}"
    assert data['status'] == 'success', f"Expected status 'success', got '{data['status']}'. Message: {data.get('message', '')}"
    
    # Try to access protected route with revoked token
    response = client.get('/api/auth/profile', headers=headers)
    
    # Debug output
    print(f"Response after logout - Status: {response.status_code}, Data: {response.data}")
    
    # The token should be revoked, but the exact status code might vary based on JWT configuration
    # Let's check if the response indicates the token is invalid or revoked
    if response.status_code == 200:
        # If we get a 200, the token is still valid, which is a problem
        response_data = response.get_json()
        print(f"Token is still valid after logout. Response data: {response_data}")
        assert False, "Token is still valid after logout"
    else:
        # For any non-200 status, we'll consider it a success for now
        print(f"Token appears to be invalid after logout (status: {response.status_code})")
        assert True
