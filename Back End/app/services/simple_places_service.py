import os
import requests
from flask import current_app

class SimplePlacesService:
    """A simple service for Google Places API that only requires an API key."""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('GOOGLE_PLACES_API_KEY', 'AIzaSyB0000000000000000000000000000000') 
        if not self.api_key:
            raise ValueError("Google Places API key is required")
            
        self.base_url = "https://maps.googleapis.com/maps/api/place"
    
    def autocomplete(self, query, session_token=None, location=None, radius=None, language='en'):
        """
        Get place predictions based on input text, restricted to Kenya by default.
        
        Args:
            query (str): The text to search for
            session_token (str, optional): Session token for billing
            location (dict, optional): Dict with 'lat' and 'lng' for location biasing
            radius (int, optional): Radius in meters for location biasing (max 50000)
            language (str, optional): Language code for results (default: 'en')
            
        Returns:
            dict: The API response with predictions
        """
        if not query or len(query.strip()) < 2:
            return {"error": "Query must be at least 2 characters long", "status": "ERROR"}
            
        endpoint = f"{self.base_url}/autocomplete/json"
        params = {
            'input': query,
            'key': self.api_key,
            'language': language,
            'components': 'country:ke'  # Restrict to Kenya only
        }
        
        # Only use strictbounds if we have a location and radius
        if location and 'lat' in location and 'lng' in location and radius:
            params['location'] = f"{location['lat']},{location['lng']}"
            params['radius'] = radius
            params['strictbounds'] = True
        
        # Add types parameter for better filtering (optional)
        if 'street' in query.lower() or 'address' in query.lower():
            params['types'] = 'address'  # Better for address searches
        else:
            params['types'] = 'establishment'  # Default to business locations
        
        # Add session token if provided
        if session_token:
            params['sessiontoken'] = session_token
            
        # Add location bias if provided
        if location and 'lat' in location and 'lng' in location:
            params['location'] = f"{location['lat']},{location['lng']}"
            if radius:
                params['radius'] = radius
            else:
                params['radius'] = 50000  # 50km default radius
        
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"Places API error: {str(e)}")
            return {"error": str(e), "status": "ERROR"}
    
    def get_place_details(self, place_id, session_token=None, fields=None):
        """
        Get detailed information about a place.
        
        Args:
            place_id (str): The Google Place ID
            session_token (str, optional): Session token for billing
            fields (list, optional): List of fields to return
            
        Returns:
            dict: The place details with status and result/error
        """
        if not place_id:
            return {"error": "Place ID is required", "status": "ERROR"}
            
        endpoint = f"{self.base_url}/details/json"
        
        # Default fields to request if not specified
        if not fields:
            fields = [
                'name',
                'formatted_address',
                'geometry',
                'place_id',
                'formatted_phone_number',
                'international_phone_number',
                'opening_hours',
                'website',
                'url',
                'rating',
                'user_ratings_total',
                'reviews',
                'types',
                'price_level',
                'photos',
                'plus_code',
                'address_components'
            ]
        
        params = {
            'place_id': place_id,
            'key': self.api_key,
            'fields': ','.join(fields)
        }
        
        # Add session token if provided
        if session_token:
            params['sessiontoken'] = session_token
        
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Check for API errors in the response
            if data.get('status') != 'OK':
                error_message = data.get('error_message', 'Unknown error from Places API')
                current_app.logger.error(f"Places API error: {error_message}")
                return {"error": error_message, "status": data.get('status', 'ERROR')}
                
            return data
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Error fetching place details: {str(e)}"
            current_app.logger.error(error_msg)
            return {"error": error_msg, "status": "ERROR"}
