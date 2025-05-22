import os
import json
from app.services.simple_places_service import SimplePlacesService

def print_place_details(place):
    """Helper function to print place details in a readable format."""
    print(f"\n📌 {place.get('name', 'N/A')}")
    print(f"📍 {place.get('formatted_address', 'No address')}")
    
    if 'formatted_phone_number' in place:
        print(f"📞 {place['formatted_phone_number']}")
    
    if 'website' in place:
        print(f"🌐 {place['website']}")
    
    if 'rating' in place:
        print(f"⭐ {place['rating']}/5.0 ({place.get('user_ratings_total', 0)} reviews)")
    
    if 'opening_hours' in place and 'weekday_text' in place['opening_hours']:
        print("\n🕒 Opening Hours:")
        for day in place['opening_hours']['weekday_text']:
            print(f"   {day}")
    
    if 'photos' in place and place['photos']:
        print(f"\n📸 {len(place['photos'])} photos available")
    
    print("\n" + "="*80)

def test_kenya_restricted_search():
    """Test the Google Places Autocomplete with Kenya restriction."""
    # Get the API key from environment variables
    api_key = os.getenv('GOOGLE_PLACES_API_KEY')
    
    if not api_key:
        print("❌ Error: GOOGLE_PLACES_API_KEY environment variable is not set")
        return
    
    print("🔍 Testing Google Places Autocomplete with Kenya restriction...\n")
    
    # Initialize the service
    places_service = SimplePlacesService(api_key)
    
    # Test 1: Search for a place in Kenya
    print("1. Searching for 'Sarit Centre' in Kenya...")
    result = places_service.autocomplete("Sarit Centre")
    
    if 'error' in result:
        print(f"❌ Error: {result['error']}")
        return
        
    if 'predictions' in result and result['predictions']:
        print("✅ Found results in Kenya:")
        for i, pred in enumerate(result['predictions'][:3], 1):  # Show first 3 results
            print(f"   {i}. {pred.get('description', 'No description')}")
            
            # Get and show details for the first result
            if i == 1 and 'place_id' in pred:
                print("\n🔍 Getting details for the first result...")
                details = places_service.get_place_details(pred['place_id'])
                if 'result' in details:
                    print_place_details(details['result'])
    else:
        print("❌ No predictions found")
    
    # Test 2: Try a location outside Kenya (should be restricted)
    print("\n2. Searching for 'Eiffel Tower' (should be restricted to Kenya)...")
    result = places_service.autocomplete("Eiffel Tower")
    
    if 'error' in result:
        print(f"❌ Error: {result['error']}")
    elif 'predictions' in result and result['predictions']:
        print("❌ Found results outside Kenya (restriction not working):")
        for i, pred in enumerate(result['predictions'][:3], 1):
            print(f"   {i}. {pred.get('description', 'No description')}")
    else:
        print("✅ No results found (expected when searching for non-Kenyan locations)")
    
    # Test 3: Search with location bias in Kenya
    print("\n3. Searching for 'restaurant' near Nairobi...")
    result = places_service.autocomplete(
        "restaurant",
        location={"lat": -1.2921, "lng": 36.8219},  # Nairobi coordinates
        radius=5000  # 5km radius
    )
    
    if 'error' in result:
        print(f"❌ Error: {result['error']}")
    elif 'predictions' in result and result['predictions']:
        print("✅ Found restaurants in Nairobi:")
        for i, pred in enumerate(result['predictions'][:3], 1):
            print(f"   {i}. {pred.get('description', 'No description')}")
    else:
        print("❌ No restaurants found in the specified area")

if __name__ == "__main__":
    test_kenya_restricted_search()
