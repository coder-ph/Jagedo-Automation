import os
from app.services.simple_places_service import SimplePlacesService

def test_places_autocomplete():
    # Get the API key from environment variables
    api_key = os.getenv('GOOGLE_PLACES_API_KEY')
    
    if not api_key:
        print("Error: GOOGLE_PLACES_API_KEY environment variable is not set")
        print("Please set it with: export GOOGLE_PLACES_API_KEY='your_api_key'")
        return
    
    print("Testing Google Places Autocomplete...\n")
    
    # Initialize the service
    places_service = SimplePlacesService(api_key)
    
    # Test 1: Basic search
    print("Test 1: Basic search for 'Nairobi'") 
    result = places_service.autocomplete("Nairobi")
    
    if 'error' in result:
        print(f"Error: {result['error']}")
        return
        
    if 'predictions' in result:
        print(f"Found {len(result['predictions'])} results:")
        for i, pred in enumerate(result['predictions'][:5], 1):  # Show first 5 results
            print(f"{i}. {pred.get('description', 'No description')}")
    else:
        print("No predictions found in the response")
    
    print("\n" + "="*80 + "\n")
    
    # Test 2: Search with location bias (Nairobi coordinates)
    print("Test 2: Search for 'restaurant' near Nairobi")
    result = places_service.autocomplete(
        "restaurant",
        location={"lat": -1.2921, "lng": 36.8219},  # Nairobi coordinates
        radius=5000  # 5km radius
    )
    
    if 'error' in result:
        print(f"Error: {result['error']}")
        return
        
    if 'predictions' in result:
        print(f"Found {len(result['predictions'])} restaurants near Nairobi:")
        for i, pred in enumerate(result['predictions'][:5], 1):  # Show first 5 results
            print(f"{i}. {pred.get('description', 'No description')}")
    else:
        print("No restaurant predictions found in the response")
    
    print("\n" + "="*80 + "\n")
    
    # Test 3: Get place details (using a known place ID - The Hub Karen, Nairobi)
    print("Test 3: Get place details for 'The Hub Karen, Nairobi'")
    place_id = "ChIJK3Y-LYVNLxgR_qK6Syz24SM"  # The Hub Karen, Nairobi
    details = places_service.get_place_details(place_id)
    
    if 'error' in details:
        print(f"Error: {details['error']}")
        return
        
    if 'result' in details:
        place = details['result']
        print(f"Name: {place.get('name', 'N/A')}")
        print(f"Address: {place.get('formatted_address', 'N/A')}")
        if 'formatted_phone_number' in place:
            print(f"Phone: {place['formatted_phone_number']}")
        if 'website' in place:
            print(f"Website: {place['website']}")
        if 'rating' in place:
            print(f"Rating: {place['rating']} ({place.get('user_ratings_total', 0)} reviews)")
    else:
        print("No place details found in the response")

if __name__ == "__main__":
    test_places_autocomplete()
