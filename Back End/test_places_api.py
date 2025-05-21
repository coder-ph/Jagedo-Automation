import unittest
import os
import json
import unittest.mock as mock
from dotenv import load_dotenv
from app import app, db

# Load environment variables
load_dotenv()

# Mock responses for Google Places API
MOCK_AUTOCOMPLETE_RESPONSE = {
    'status': 'OK',
    'predictions': [
        {
            'description': 'Nairobi, Kenya',
            'place_id': 'ChIJd8BlQ2BZwokRAFUEcm_qrcA',
            'types': ['locality', 'political', 'geocode'],
            'structured_formatting': {
                'main_text': 'Nairobi',
                'secondary_text': 'Kenya'
            }
        },
        {
            'description': 'Nairobi National Park, Nairobi, Kenya',
            'place_id': 'ChIJy8mG5jFZwokRHYi1lN2pBCU',
            'types': ['park', 'tourist_attraction', 'point_of_interest', 'establishment'],
            'structured_formatting': {
                'main_text': 'Nairobi National Park',
                'secondary_text': 'Nairobi, Kenya'
            }
        }
    ]
}

MOCK_PLACE_DETAILS_RESPONSE = {
    'status': 'OK',
    'result': {
        'formatted_address': 'Nairobi, Kenya',
        'geometry': {
            'location': {
                'lat': -1.2920659,
                'lng': 36.8219462
            },
            'viewport': {
                'northeast': {
                    'lat': -1.219766870107278,
                    'lng': 36.91522587989272
                },
                'southwest': {
                    'lat': -1.352083129892722,
                    'lng': 36.65066852010728
                }
            }
        },
        'place_id': 'ChIJd8BlQ2BZwokRAFUEcm_qrcA',
        'types': ['locality', 'political']
    }
}

class TestPlacesAPI(unittest.TestCase):    
    def setUp(self):
        """Set up test client and configure app for testing"""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        
        # Create a test user and get auth token
        self.test_email = "test_places@example.com"
        self.test_password = "testpass123"
        self.auth_token = self._get_auth_token()
        
        # Common headers with auth token
        self.headers = {
            'Authorization': f'Bearer {self.auth_token}',
            'Content-Type': 'application/json'
        }
    
    def tearDown(self):
        """Clean up after each test"""
        with app.app_context():
            db.session.remove()
    
    def _get_auth_token(self):
        """Helper to get auth token for test user"""
        # Create test user if not exists
        from models import User, UserRole
        from flask_bcrypt import generate_password_hash
        
        with app.app_context():
            user = User.query.filter_by(email=self.test_email).first()
            if not user:
                # Create user with hashed password
                user = User(
                    email=self.test_email,
                    password_hash=generate_password_hash(self.test_password).decode('utf-8'),
                    role=UserRole.CUSTOMER,
                    name="Test User",
                    location="Nairobi, Kenya"
                )
                db.session.add(user)
                db.session.commit()
            
            # Get auth token
            response = self.app.post('/api/login', json={
                'email': self.test_email,
                'password': self.test_password
            })
            
            if response.status_code == 200:
                return response.get_json()['data']['access_token']
            else:
                raise Exception(f"Failed to get auth token: {response.status_code} - {response.data}")
    
    @mock.patch('requests.get')
    def test_autocomplete_endpoint(self, mock_get):
        """Test the places autocomplete endpoint"""
        # Setup mock response
        mock_response = mock.Mock()
        mock_response.json.return_value = MOCK_AUTOCOMPLETE_RESPONSE
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        # Test with a known location
        response = self.app.get(
            '/api/places/autocomplete?query=Nairobi',
            headers=self.headers
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        # Check response structure
        self.assertIn('status', data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('predictions', data)
        self.assertGreater(len(data['predictions']), 0)
        
        # Check prediction structure
        prediction = data['predictions'][0]
        self.assertIn('description', prediction)
        self.assertIn('place_id', prediction)
        self.assertIn('types', prediction)
        
        # Verify the API was called with correct parameters
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        self.assertEqual(args[0], 'https://maps.googleapis.com/maps/api/place/autocomplete/json')
        self.assertEqual(kwargs['params']['input'], 'Nairobi')
        self.assertIn('key', kwargs['params'])
        
        # Return the first prediction for use in details test
        return prediction['place_id']
    
    @mock.patch('requests.get')
    def test_place_details_endpoint(self, mock_get):
        """Test the place details endpoint"""
        # Setup mock response for place details
        mock_response = mock.Mock()
        mock_response.json.return_value = MOCK_PLACE_DETAILS_RESPONSE
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        # Use a known place ID for testing
        test_place_id = 'ChIJd8BlQ2BZwokRAFUEcm_qrcA'
        
        # Test getting place details
        response = self.app.get(
            f'/api/places/details/{test_place_id}',
            headers=self.headers
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        # Check response structure
        self.assertIn('status', data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('result', data)
        
        # Check some common fields in the result
        result = data['result']
        self.assertIn('formatted_address', result)
        self.assertIn('geometry', result)
        self.assertIn('location', result['geometry'])
        
        # Verify the API was called with correct parameters
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        self.assertEqual(args[0], 'https://maps.googleapis.com/maps/api/place/details/json')
        self.assertEqual(kwargs['params']['place_id'], test_place_id)
        self.assertIn('key', kwargs['params'])
    
    @mock.patch('requests.get')
    def test_autocomplete_with_location_bias(self, mock_get):
        """Test autocomplete with location biasing"""
        # Setup mock response
        mock_response = mock.Mock()
        mock_response.json.return_value = MOCK_AUTOCOMPLETE_RESPONSE
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        # Coordinates for Nairobi
        nairobi_location = "-1.2921,36.8219"
        
        response = self.app.get(
            f'/api/places/autocomplete?query=West&location={nairobi_location}&radius=50000',
            headers=self.headers
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        # Check response structure
        self.assertEqual(data['status'], 'success')
        self.assertIn('predictions', data)
        self.assertGreater(len(data['predictions']), 0)
        
        # Verify the API was called with correct parameters
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        self.assertEqual(args[0], 'https://maps.googleapis.com/maps/api/place/autocomplete/json')
        self.assertEqual(kwargs['params']['input'], 'West')
        self.assertEqual(kwargs['params']['location'], nairobi_location)
        self.assertEqual(kwargs['params']['radius'], 50000)  # Should be an integer, not a string
        self.assertIn('key', kwargs['params'])
    
    def test_invalid_place_id(self):
        """Test with an invalid place ID"""
        response = self.app.get(
            '/api/places/details/invalid_place_id_123',
            headers=self.headers
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertEqual(data['status'], 'error')
        self.assertIn('message', data)

if __name__ == '__main__':
    unittest.main()
