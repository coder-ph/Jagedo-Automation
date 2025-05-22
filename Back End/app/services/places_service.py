import os
import requests
from flask import current_app, session
from .google_oauth import GoogleOAuthService

class PlacesService:
    """Service for handling Google Places API requests"""
    
    BASE_URL = "https://places.googleapis.com/v1/places"
    
    def __init__(self):
        self.api_key = current_app.config.get('GOOGLE_PLACES_API_KEY')
    
    def get_auth_headers(self):
        """Get authentication headers for API requests"""
        if 'google_token' in session:
            # Check if token needs refresh
            token_info = GoogleOAuthService.refresh_token_if_needed(session['google_token'])
            if token_info != session['google_token']:
                session['google_token'] = token_info
                session.modified = True
                
            return {
                'Authorization': f'Bearer {token_info["token"]}',
                'Content-Type': 'application/json',
                'X-Goog-FieldMask': 'places.displayName,places.formattedAddress,places.id,places.types,places.location',
                'X-Goog-User-Project': current_app.config.get('GOOGLE_PROJECT_ID', '')
            }
        
        # Fallback to API key if OAuth not available
        return {
            'Content-Type': 'application/json',
            'X-Goog-Api-Key': self.api_key,
            'X-Goog-FieldMask': 'places.displayName,places.formattedAddress,places.id,places.types,places.location',
            'X-Goog-User-Project': current_app.config.get('GOOGLE_PROJECT_ID', '')
        }
    
    def autocomplete(self, query, location_bias=None):
        """
        Get place predictions based on input text
        
        Args:
            query (str): The text input for autocomplete
            location_bias (dict, optional): Location bias parameters (lat, lng, radius)
            
        Returns:
            dict: Autocomplete predictions
        """
        url = f"{self.BASE_URL}:autocomplete"
        
        # Build request body
        data = {
            "input": query,
            "languageCode": "en",
            "regionCode": "ke"  # Default to Kenya, can be made configurable
        }
        
        # Add location bias if provided
        if location_bias:
            data["locationBias"] = {
                "rectangle": {
                    "low": {
                        "latitude": location_bias['lat'] - 0.1,
                        "longitude": location_bias['lng'] - 0.1
                    },
                    "high": {
                        "latitude": location_bias['lat'] + 0.1,
                        "longitude": location_bias['lng'] + 0.1
                    }
                }
            }
        
        try:
            response = requests.post(
                url,
                headers=self.get_auth_headers(),
                json=data
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"Error in Places API autocomplete: {str(e)}")
            return {"error": str(e), "status_code": getattr(e.response, 'status_code', 500)}
    
    def get_place_details(self, place_id):
        """
        Get detailed information about a place
        
        Args:
            place_id (str): The Google Place ID
            
        Returns:
            dict: Place details
        """
        url = f"{self.BASE_URL}/{place_id}"
        params = {
            "fields": "displayName,formattedAddress,location,types,addressComponents",
            "languageCode": "en"
        }
        
        try:
            response = requests.get(
                url,
                headers=self.get_auth_headers(),
                params=params
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"Error in Places API get_place_details: {str(e)}")
            return {"error": str(e), "status_code": getattr(e.response, 'status_code', 500)}
