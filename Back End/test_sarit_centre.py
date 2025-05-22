import os
import json
from app.services.simple_places_service import SimplePlacesService

def test_sarit_centre_search():
    # Get the API key from environment variables
    api_key = os.getenv('GOOGLE_PLACES_API_KEY')
    
    if not api_key:
        print("Error: GOOGLE_PLACES_API_KEY environment variable is not set")
        return
    
    print("Testing Sarit Centre search...\n")
    
    # Initialize the service
    places_service = SimplePlacesService(api_key)
    
    # Test 1: Try different search variations
    queries = [
        "Sarit Centre",
        "Sarit Centre Nairobi",
        "Sarit Centre Westlands",
        "Sarit"
    ]
    
    for query in queries:
        print(f"\nSearching for: '{query}'")
        result = places_service.autocomplete(query)
        
        print("\nAPI Response:")
        print(json.dumps(result, indent=2))
        
        if 'predictions' in result and result['predictions']:
            print("\nResults:")
            for i, pred in enumerate(result['predictions'][:3], 1):
                print(f"{i}. {pred.get('description', 'No description')}")
        else:
            print("No results found")
            
        print("\n" + "-"*80)

if __name__ == "__main__":
    test_sarit_centre_search()
