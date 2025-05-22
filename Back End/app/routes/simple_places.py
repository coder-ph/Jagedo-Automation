from flask import Blueprint, request, jsonify, current_app
from ..services.simple_places_service import SimplePlacesService
import uuid

# Create a Blueprint
simple_places_bp = Blueprint('simple_places', __name__)

# Initialize the Places service
places_service = SimplePlacesService()

@simple_places_bp.route('/api/places/autocomplete', methods=['GET'])
def autocomplete():
    """
    Endpoint for place autocomplete suggestions.
    
    Query Parameters:
        q (str): The search query
        lat (float, optional): Latitude for location biasing
        lng (float, optional): Longitude for location biasing
        radius (int, optional): Radius in meters for location biasing (default: 50000)
    """
    query = request.args.get('q')
    lat = request.args.get('lat', type=float)
    lng = request.args.get('lng', type=float)
    radius = request.args.get('radius', 50000, type=int)
    
    if not query:
        return jsonify({"error": "Query parameter 'q' is required"}), 400
    
    # Create a session token for this search session
    session_token = str(uuid.uuid4())
    
    # Prepare location if provided
    location = None
    if lat is not None and lng is not None:
        location = {'lat': lat, 'lng': lng}
    
    # Get autocomplete results
    result = places_service.autocomplete(
        query=query,
        session_token=session_token,
        location=location,
        radius=radius
    )
    
    if 'error' in result:
        return jsonify({"error": result['error']}), 500
        
    return jsonify({
        "status": "success",
        "session_token": session_token,
        "predictions": result.get('predictions', [])
    })

@simple_places_bp.route('/api/places/details/<place_id>', methods=['GET'])
def place_details(place_id):
    """
    Get detailed information about a place.
    
    Path Parameters:
        place_id (str): The Google Place ID
        
    Query Parameters:
        session_token (str, optional): Session token from the autocomplete request
    """
    session_token = request.args.get('session_token')
    
    if not place_id:
        return jsonify({"error": "Place ID is required"}), 400
    
    # Get place details
    result = places_service.get_place_details(
        place_id=place_id,
        session_token=session_token
    )
    
    if 'error' in result:
        return jsonify({"error": result['error']}), 500
        
    return jsonify({
        "status": "success",
        "result": result.get('result', {})
    })
