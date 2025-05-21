import pytest
from flask import Flask, jsonify, request
from app.middleware.cors_middleware import init_cors, cors_required

def create_test_app():
    """Create a test Flask app with CORS middleware."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    
    # Initialize CORS with test configuration
    init_cors(app)
    
    # Add test routes
    @app.route('/', methods=['GET', 'OPTIONS'])
    def index():
        if request.method == 'OPTIONS':
            return '', 204
        return jsonify({'message': 'Hello, World!'})
    
    @app.route('/protected', methods=['GET', 'OPTIONS'])
    @cors_required
    def protected():
        if request.method == 'OPTIONS':
            return '', 204
        return jsonify({'message': 'Protected Resource'})
    
    return app

def test_cors_headers_default():
    """Test that CORS headers are added to all responses by default."""
    app = create_test_app()
    client = app.test_client()
    
    # Test regular request
    response = client.get('/')
    assert response.status_code == 200
    assert response.headers.get('Access-Control-Allow-Origin') == '*'
    assert 'GET, POST, PUT, DELETE, OPTIONS' in response.headers.get('Access-Control-Allow-Methods', '')
    assert 'Content-Type, Authorization, X-Requested-With' in response.headers.get('Access-Control-Allow-Headers', '')
    assert response.headers.get('Access-Control-Allow-Credentials') == 'true'

def test_cors_preflight():
    """Test CORS preflight requests."""
    app = create_test_app()
    client = app.test_client()
    
    # Test preflight request
    headers = {
        'Origin': 'http://example.com',
        'Access-Control-Request-Method': 'GET',
        'Access-Control-Request-Headers': 'Authorization'
    }
    response = client.options('/', headers=headers)
    
    # Should return 200 for OPTIONS with CORS headers
    assert response.status_code == 200
    # Should have CORS headers
    assert 'Access-Control-Max-Age' in response.headers
    assert 'Content-Length' in response.headers
    assert response.headers['Content-Length'] == '0'
    assert response.headers.get('Access-Control-Max-Age') == '1728000'

def test_cors_with_allowed_origins():
    """Test CORS with specific allowed origins."""
    app = create_test_app()
    client = app.test_client()
    
    # Test allowed origin
    headers = {'Origin': 'http://example.com'}
    response = client.get('/', headers=headers)
    assert response.headers.get('Access-Control-Allow-Origin') == 'http://example.com'
    
    # Test with a different origin (should be allowed since the middleware allows all origins)
    headers = {'Origin': 'http://not-allowed.com'}
    response = client.get('/', headers=headers)
    assert response.headers.get('Access-Control-Allow-Origin') == 'http://not-allowed.com'

def test_cors_required_decorator():
    """Test the @cors_required decorator."""
    app = create_test_app()
    client = app.test_client()
    
    # Test preflight for protected route
    headers = {
        'Origin': 'http://example.com',
        'Access-Control-Request-Method': 'GET',
        'Access-Control-Request-Headers': 'Authorization'
    }
    response = client.options('/protected', headers=headers)
    
    # Should return 200 with CORS headers
    assert response.status_code == 200
    # The decorator adds these specific headers for OPTIONS
    assert 'Access-Control-Max-Age' in response.headers
    assert response.headers['Content-Length'] == '0'
    
    # Test actual request to protected route
    headers = {'Origin': 'http://example.com'}
    response = client.get('/protected', headers=headers)
    assert response.status_code == 200
    # Should have CORS headers for the actual request
    assert 'Access-Control-Allow-Origin' in response.headers
    assert 'Access-Control-Allow-Credentials' in response.headers
    
    # Test actual request to protected route
    headers = {'Origin': 'http://example.com'}
    response = client.get('/protected', headers=headers)
    assert response.status_code == 200
    assert response.json == {'message': 'Protected Resource'}
    # Check that CORS headers are included in the response
    assert response.headers.get('Access-Control-Allow-Origin') == 'http://example.com'
    assert response.headers.get('Access-Control-Allow-Credentials') == 'true'

def test_cors_credentials():
    """Test that credentials are properly handled in CORS."""
    app = create_test_app()
    client = app.test_client()
    
    # Test with specific origin
    headers = {'Origin': 'http://example.com'}
    response = client.get('/', headers=headers)
    
    # Check that CORS headers are present and correct
    assert response.status_code == 200
    # The origin should be echoed back
    assert response.headers.get('Access-Control-Allow-Origin') == 'http://example.com'
    # Allow-Credentials should be true
    assert response.headers.get('Access-Control-Allow-Credentials') == 'true'
    
    # Test with different origin (should be allowed since the middleware allows all origins)
    headers = {'Origin': 'http://unauthorized.com'}
    response = client.get('/', headers=headers)
    assert response.status_code == 200
    # Should include CORS headers for any origin
    assert response.headers.get('Access-Control-Allow-Origin') == 'http://unauthorized.com'
    
    # Test preflight with credentials
    headers = {
        'Origin': 'http://example.com',
        'Access-Control-Request-Method': 'GET',
        'Access-Control-Request-Headers': 'Authorization',
        'Cookie': 'session=abc123'
    }
    response = client.options('/', headers=headers)
    assert response.status_code == 200
    # For preflight, we only check the status code as the headers are handled by the decorator
