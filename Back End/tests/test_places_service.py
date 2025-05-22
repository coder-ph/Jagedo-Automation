import os
import unittest
from unittest.mock import patch, MagicMock
from app.services.simple_places_service import SimplePlacesService

class TestSimplePlacesService(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.api_key = os.getenv('GOOGLE_PLACES_API_KEY')
        if not self.api_key:
            self.skipTest("GOOGLE_PLACES_API_KEY environment variable not set")
        
        self.places_service = SimplePlacesService(self.api_key)
    
    def test_autocomplete_success(self):
        """Test successful place autocomplete request."""
        # Test with a known location in Kenya
        query = "Nairobi"
        result = self.places_service.autocomplete(query)
        
        # Check if we got a successful response
        self.assertIn('predictions', result)
        self.assertIsInstance(result['predictions'], list)
        
        # If we have predictions, check their structure
        if result['predictions']:
            prediction = result['predictions'][0]
            self.assertIn('description', prediction)
            self.assertIn('place_id', prediction)
    
    def test_autocomplete_with_location(self):
        """Test autocomplete with location bias."""
        # Coordinates for Nairobi, Kenya
        location = {'lat': -1.2921, 'lng': 36.8219}
        result = self.places_service.autocomplete(
            query="restaurant",
            location=location,
            radius=5000  # 5km radius
        )
        
        self.assertIn('predictions', result)
        self.assertIsInstance(result['predictions'], list)
    
    def test_get_place_details(self):
        """Test getting place details by place ID."""
        # This is a known place ID for The Hub Karen in Nairobi
        place_id = "ChIJK3Y-LYVNLxgR_qK6Syz24SM"
        result = self.places_service.get_place_details(place_id)
        
        # Check if we got a successful response
        self.assertIn('result', result)
        self.assertIsInstance(result['result'], dict)
        
        # Check for expected fields in the result
        if 'result' in result:
            place = result['result']
            self.assertIn('name', place)
            self.assertIn('formatted_address', place)
            self.assertIn('geometry', place)
    
    @patch('requests.get')
    def test_autocomplete_api_error(self, mock_get):
        """Test handling of API errors in autocomplete."""
        # Mock a failed API response
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = Exception("API Error")
        mock_get.return_value = mock_response
        
        # Create a new instance to use the mocked requests
        service = SimplePlacesService("dummy_key")
        result = service.autocomplete("test")
        
        self.assertIn('error', result)
        self.assertEqual(result['status'], 'ERROR')

if __name__ == '__main__':
    unittest.main()
