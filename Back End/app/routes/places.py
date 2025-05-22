from flask import Blueprint, request, jsonify, session, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.places_service import PlacesService
from ..services.google_oauth import GoogleOAuthService

places_bp = Blueprint('places', __name__)

@places_bp.route('/api/places/autocomplete', methods=['GET'])
@jwt_required(optional=True)
def autocomplete():
    """
    Get place predictions based on input text
    ---
    tags:
      - Places
    parameters:
      - name: query
        in: query
        type: string
        required: true
        description: The text input for autocomplete
      - name: lat
        in: query
        type: number
        required: false
        description: Latitude for location bias
      - name: lng
        in: query
        type: number
        required: false
        description: Longitude for location bias
      - name: radius
        in: query
        type: number
        required: false
        description: Radius in meters for location bias
    responses:
      200:
        description: List of place predictions
        schema:
          type: object
          properties:
            predictions:
              type: array
              items:
                type: object
                properties:
                  place_id:
                    type: string
                  description:
                    type: string
                  types:
                    type: array
                    items:
                      type: string
                  structured_formatting:
                    type: object
                    properties:
                      main_text:
                        type: string
                      secondary_text:
                        type: string
      400:
        description: Missing required parameters
      500:
        description: Internal server error
    """
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400
    
    location_bias = None
    lat = request.args.get('lat', type=float)
    lng = request.args.get('lng', type=float)
    
    if lat is not None and lng is not None:
        location_bias = {
            'lat': lat,
            'lng': lng,
            'radius': request.args.get('radius', 50000, type=float)  # Default 50km radius
        }
    
    places_service = PlacesService()
    result = places_service.autocomplete(query, location_bias)
    
    if 'error' in result:
        return jsonify({"error": result['error']}), result.get('status_code', 500)
    
    # Transform the response to match the expected format
    predictions = []
    for place in result.get('places', []):
        predictions.append({
            'place_id': place.get('id'),
            'description': place.get('formattedAddress'),
            'types': place.get('types', []),
            'structured_formatting': {
                'main_text': place.get('displayName', {}).get('text', ''),
                'secondary_text': place.get('formattedAddress', '')
            },
            'location': place.get('location')
        })
    
    return jsonify({"predictions": predictions})

@places_bp.route('/api/places/details/<place_id>', methods=['GET'])
@jwt_required(optional=True)
def place_details(place_id):
    """
    Get detailed information about a place
    ---
    tags:
      - Places
    parameters:
      - name: place_id
        in: path
        type: string
        required: true
        description: Google Place ID
    responses:
      200:
        description: Place details
        schema:
          type: object
          properties:
            result:
              type: object
              properties:
                formatted_address:
                  type: string
                geometry:
                  type: object
                  properties:
                    location:
                      type: object
                      properties:
                        lat:
                          type: number
                        lng:
                          type: number
                name:
                  type: string
                place_id:
                  type: string
                types:
                  type: array
                  items:
                    type: string
      404:
        description: Place not found
      500:
        description: Internal server error
    """
    if not place_id:
        return jsonify({"error": "Place ID is required"}), 400
    
    places_service = PlacesService()
    result = places_service.get_place_details(place_id)
    
    if 'error' in result:
        return jsonify({"error": result['error']}), result.get('status_code', 500)
    
    if not result:
        return jsonify({"error": "Place not found"}), 404
    
    # Transform the response to match the expected format
    place_data = {
        'formatted_address': result.get('formattedAddress'),
        'geometry': {
            'location': {
                'lat': result.get('location', {}).get('latitude'),
                'lng': result.get('location', {}).get('longitude')
            }
        },
        'name': result.get('displayName', {}).get('text', ''),
        'place_id': place_id,
        'types': result.get('types', [])
    }
    
    return jsonify({"result": place_data})

@places_bp.route('/api/places/auth/url', methods=['GET'])
@jwt_required()
def get_auth_url():
    """
    Get Google OAuth URL for Places API
    ---
    tags:
      - Places
    responses:
      200:
        description: Google OAuth URL
        schema:
          type: object
          properties:
            url:
              type: string
      500:
        description: Error generating auth URL
    """
    try:
        auth_url = GoogleOAuthService.get_auth_url()
        return jsonify({"url": auth_url})
    except Exception as e:
        current_app.logger.error(f"Error generating auth URL: {str(e)}")
        return jsonify({"error": str(e)}), 500

@places_bp.route('/api/places/auth/callback', methods=['GET'])
@jwt_required()
def oauth_callback():
    """
    OAuth callback for Google Places API
    ---
    tags:
      - Places
    parameters:
      - name: code
        in: query
        type: string
        required: true
        description: Authorization code from Google
      - name: error
        in: query
        type: string
        required: false
        description: Error message if OAuth failed
    responses:
      200:
        description: Successfully authenticated
      400:
        description: Missing code parameter or OAuth error
      500:
        description: Internal server error
    """
    error = request.args.get('error')
    if error:
        return jsonify({"error": f"OAuth error: {error}"}), 400
    
    code = request.args.get('code')
    if not code:
        return jsonify({"error": "Missing authorization code"}), 400
    
    try:
        token_info = GoogleOAuthService.get_tokens(code)
        # Store token in session (in a real app, you'd want to store this in a database)
        session['google_token'] = token_info
        return jsonify({"message": "Successfully authenticated with Google Places API"})
    except Exception as e:
        current_app.logger.error(f"Error in OAuth callback: {str(e)}")
        return jsonify({"error": str(e)}), 500
