import pytest
from unittest.mock import patch, MagicMock
from flask import Flask, request, g, jsonify
from app.middleware.request_logging import init_request_logging
import logging
import time

def create_test_app():
    """Create and configure a test Flask app with request logging."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    
    # Configure test logging
    logger = logging.getLogger('request')
    logger.setLevel(logging.INFO)
    logger.propagate = True  # Allow propagation to capture logs
    
    # Clear any existing handlers
    if logger.hasHandlers():
        logger.handlers.clear()
    
    # Add a memory handler to capture logs
    log_capture = logging.StreamHandler()
    log_capture.setLevel(logging.INFO)
    logger.addHandler(log_capture)
    
    # Initialize request logging
    init_request_logging(app)
    
    # Add test routes
    @app.route('/')
    def index():
        return jsonify({'message': 'Hello, World!'})
    
    @app.route('/health')
    def health():
        return jsonify({'status': 'ok'})
    
    @app.route('/test', methods=['POST'])
    def test_post():
        if request.is_json:
            return jsonify({'received': request.get_json()})
        return jsonify({'received': request.form.to_dict()})
    
    @app.route('/error')
    def error():
        return jsonify({'error': 'Not found'}), 404
    
    return app

@pytest.fixture
def app():
    """Create and configure a test Flask app with request logging."""
    return create_test_app()

@pytest.fixture
def client(app):
    """Create a test client for the Flask app."""
    with app.test_client() as client:
        with app.app_context():
            yield client

class TestRequestLogging:
    def test_request_logging_basic(self, client, caplog):
        """Test basic request logging."""
        # Clear any existing log records
        caplog.clear()
        
        # Enable logging for the 'request' logger
        with caplog.at_level(logging.INFO, logger='request'):
            # Make a request to trigger logging
            response = client.get('/')
            assert response.status_code == 200
            
            # Get all records for the request logger
            records = [r for r in caplog.records if r.name == 'request']
            assert len(records) > 0, f"No log records found for 'request' logger. All records: {caplog.records}"
            
            # Get the most recent log record
            record = records[-1]
            
            # Check the log message contains expected fields
            log_message = record.getMessage()
            assert '127.0.0.1' in log_message, f"IP not in log message: {log_message}"
            assert 'GET' in log_message, f"Method not in log message: {log_message}"
            assert '/' in log_message, f"Path not in log message: {log_message}"
            assert '200' in log_message, f"Status not in log message: {log_message}"
            
            # Check extra fields are present in the record's request dict
            assert 'request' in record.__dict__, f"Request data not in record: {record.__dict__}"
            request_data = record.request
            assert 'method' in request_data, f"Method not in request data: {request_data}"
            assert request_data['method'] == 'GET', f"Unexpected method: {request_data['method']}"
            assert request_data['path'] == '/', f"Unexpected path: {request_data['path']}"
            assert request_data['status'] == 200, f"Unexpected status: {request_data['status']}"
            assert 'duration' in request_data, f"Duration not in request data: {request_data}"
            assert isinstance(record.duration, float), f"Duration is not float: {type(record.duration)}"
    
    def test_request_logging_with_query_params(self, client, caplog):
        """Test logging of requests with query parameters."""
        caplog.clear()
        
        with caplog.at_level(logging.INFO, logger='request'):
            response = client.get('/?test=1&foo=bar')
            
            assert response.status_code == 200
            
            records = [r for r in caplog.records if r.name == 'request']
            assert len(records) > 0, f"No log records found for 'request' logger. All records: {caplog.records}"
            
            record = records[-1]
            
            # Check that the query string is in the log message
            log_message = record.getMessage()
            assert any(param in log_message for param in ['test=1', 'foo=bar']), \
                f"Query params not in log message: {log_message}"
            
            # Check the query_params in the request data
            assert 'request' in record.__dict__, f"Request data not in record: {record.__dict__}"
            request_data = record.request
            assert 'query_params' in request_data, \
                f"query_params not in request data: {request_data}"
            query_params = request_data['query_params']
            assert isinstance(query_params, dict), \
                f"query_params is not a dict: {type(query_params)}"
            assert set(query_params.keys()) == {'test', 'foo'}, \
                f"Unexpected query params: {query_params.keys()}"
    
    def test_post_request_logging(self, client, caplog):
        """Test logging of POST requests with JSON data."""
        caplog.clear()
        test_data = {'key': 'value', 'nested': {'a': 1}}
        
        with caplog.at_level(logging.INFO, logger='request'):
            response = client.post(
                '/test',
                json=test_data,
                headers={'Content-Type': 'application/json'}
            )
            
            assert response.status_code == 200
            
            records = [r for r in caplog.records if r.name == 'request']
            assert len(records) > 0, f"No log records found for 'request' logger. All records: {caplog.records}"
            
            record = records[-1]
            assert 'request' in record.__dict__, f"Request data not in record: {record.__dict__}"
            request_data = record.request
            assert request_data['method'] == 'POST', f"Unexpected method: {request_data['method']}"
            assert request_data['path'] == '/test', f"Unexpected path: {request_data['path']}"
            
            # Check that request_data is in the request data
            assert 'request_data' in request_data, \
                f"request_data not in request data: {request_data}"
            assert request_data['request_data'] == test_data, \
                f"Unexpected request_data: {request_data['request_data']}"
    
    def test_error_logging(self, client, caplog):
        """Test logging of error responses."""
        caplog.clear()
        
        with caplog.at_level(logging.INFO, logger='request'):
            response = client.get('/error')
            
            assert response.status_code == 404
            
            records = [r for r in caplog.records if r.name == 'request']
            assert len(records) > 0, f"No log records found for 'request' logger. All records: {caplog.records}"
            
            record = records[-1]
            assert 'request' in record.__dict__, f"Request data not in record: {record.__dict__}"
            request_data = record.request
            assert request_data['status'] == 404, f"Unexpected status: {request_data['status']}"
            
            # Check that the status code is in the log message
            log_message = record.getMessage()
            assert '404' in log_message, \
                f"Status code 404 not found in log message: {log_message}"
    
    def test_health_check_not_logged(self, client, caplog):
        """Test that health check requests are not logged."""
        with caplog.at_level(logging.INFO, logger='request'):
            response = client.get('/health')
            
            assert response.status_code == 200
            assert len(caplog.records) == 0  # No log records should be created
    
    def test_request_duration(self, client, caplog):
        """Test that request duration is logged correctly."""
        caplog.clear()
        
        with caplog.at_level(logging.INFO, logger='request'):
            response = client.get('/')
            assert response.status_code == 200
            
            records = [r for r in caplog.records if r.name == 'request']
            assert len(records) > 0, f"No log records found for 'request' logger. All records: {caplog.records}"
            
            record = records[-1]
            # Check that the duration is in the log message
            log_message = record.getMessage()
            assert 'ms' in log_message, f"Duration not in log message: {log_message}"
    
    def test_user_id_logging(self, client, caplog):
        """Test that user ID is logged for authenticated requests."""
        caplog.clear()
        
        # Create a test user
        test_user_id = 123
        
        # Create a test app with a route that sets g.user_id
        app = create_test_app()
        
        @app.route('/auth')
        def auth_route():
            from flask import g
            g.user_id = test_user_id
            return jsonify({'status': 'ok'})
            
        # Use the test client with the new route
        test_client = app.test_client()
        
        with caplog.at_level(logging.INFO, logger='request'):
            response = test_client.get('/auth')
            assert response.status_code == 200
            
            records = [r for r in caplog.records if r.name == 'request']
            assert len(records) > 0, f"No log records found for 'request' logger. All records: {caplog.records}"
            
            # The first record is for the OPTIONS preflight, second is the actual request
            record = records[-1]
            log_message = record.getMessage()
            assert 'auth' in log_message, f"Auth route not in log message: {log_message}"
            
            # Check the request data in the record's __dict__
            assert 'request' in record.__dict__, f"Request data not in record: {record.__dict__}"
            request_data = record.__dict__['request']
            assert 'user_id' in request_data, f"User ID not in request data: {request_data}"
            assert request_data['user_id'] == test_user_id, f"Unexpected user ID: {request_data['user_id']}"
    
    def test_content_length_logging(self, client, caplog):
        """Test that content length is logged correctly."""
        caplog.clear()
        test_data = {'key': 'value' * 100}  # Large enough to be noticeable
    
        with caplog.at_level(logging.INFO, logger='request'):
            response = client.post(
                '/test',
                json=test_data,
                headers={'Content-Type': 'application/json'}
            )
    
            assert response.status_code == 200
    
            records = [r for r in caplog.records if r.name == 'request']
            assert len(records) > 0, f"No log records found for 'request' logger. All records: {caplog.records}"
            
            record = records[-1]
            log_message = record.getMessage()
            assert 'POST' in log_message, f"POST not in log message: {log_message}"
            
            # Check the request data in the record's __dict__
            assert 'request' in record.__dict__, f"Request data not in record: {record.__dict__}"
            request_data = record.__dict__['request']
            assert 'content_length' in request_data, f"content_length not in request data: {request_data}"
            assert request_data['content_length'] > 0, f"content_length should be positive: {request_data['content_length']}"

    def test_form_data_logging(self, client, caplog):
        """Test logging of form data."""
        caplog.clear()
        form_data = {
            'username': 'testuser',
            'password': 'testpass'
        }
    
        with caplog.at_level(logging.INFO, logger='request'):
            response = client.post(
                '/test',
                data=form_data,
                content_type='application/x-www-form-urlencoded',
                headers={'Accept': 'application/json'}
            )
    
            assert response.status_code == 200, f"Unexpected status code: {response.status_code}. Response: {response.data}"
            
            records = [r for r in caplog.records if r.name == 'request']
            assert len(records) > 0, f"No log records found for 'request' logger. All records: {caplog.records}"
            
            record = records[-1]
            log_message = record.getMessage()
            assert 'POST' in log_message, f"POST not in log message: {log_message}"
            
            # Check the request data in the record's __dict__
            assert 'request' in record.__dict__, f"Request data not in record: {record.__dict__}"
            request_data = record.__dict__['request']
            assert 'form_data' in request_data, f"form_data not in request data: {request_data}"
            assert request_data['form_data'] == form_data, f"Unexpected form data: {request_data['form_data']}"
