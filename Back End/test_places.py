import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_google_oauth2_token():
    """Test OAuth 2.0 token retrieval"""
    token_url = os.getenv('GOOGLE_TOKEN_URI')
    client_id = os.getenv('GOOGLE_CLIENT_ID')
    client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
    
    print("Testing OAuth 2.0 token retrieval...")
    print(f"Token URL: {token_url}")
    print(f"Client ID: {client_id[:10]}..." if client_id else "No client ID found")
    print(f"Client Secret: {'*' * 10}..." if client_secret else "No client secret found")
    
    try:
        response = requests.post(
            token_url,
            data={
                'grant_type': 'client_credentials',
                'client_id': client_id,
                'client_secret': client_secret,
                'scope': 'https://www.googleapis.com/auth/places'
            }
        )
        response.raise_for_status()
        token_data = response.json()
        print("✅ Successfully obtained OAuth 2.0 token")
        print(f"Token type: {token_data.get('token_type')}")
        print(f"Expires in: {token_data.get('expires_in')} seconds")
        return token_data.get('access_token')
    except Exception as e:
        print(f"❌ Failed to get OAuth 2.0 token: {str(e)}")
        if hasattr(e, 'response') and e.response:
            print(f"Response status: {e.response.status_code}")
            print(f"Response body: {e.response.text}")
        return None

def test_places_autocomplete(api_key=None, access_token=None):
    """Test Places Autocomplete API"""
    query = "Nairobi"
    
    if access_token:
        print("\nTesting Places Autocomplete with OAuth 2.0...")
        url = 'https://places.googleapis.com/v1/places:autocomplete'
        headers = {
            'Content-Type': 'application/json',
            'X-Goog-FieldMask': 'places.displayName,places.formattedAddress,places.id,places.types',
            'Authorization': f'Bearer {access_token}'
        }
        payload = {
            'input': query,
            'languageCode': 'en'
        }
    elif api_key:
        print("\nTesting Places Autocomplete with API Key...")
        url = 'https://maps.googleapis.com/maps/api/place/autocomplete/json'
        params = {
            'input': query,
            'key': api_key,
            'types': 'geocode',
            'language': 'en'
        }
        headers = {}
        payload = None
    else:
        print("❌ No authentication method provided")
        return
    
    try:
        if access_token:
            response = requests.post(url, headers=headers, json=payload)
        else:
            response = requests.get(url, headers=headers, params=params)
            
        response.raise_for_status()
        data = response.json()
        print("✅ Places Autocomplete API call successful")
        print(f"Response: {data}")
        return data
    except Exception as e:
        print(f"❌ Places Autocomplete API call failed: {str(e)}")
        if hasattr(e, 'response') and e.response:
            print(f"Response status: {e.response.status_code}")
            print(f"Response body: {e.response.text}")
        return None

if __name__ == "__main__":
    print("=== Testing Google Places API Integration ===\n")
    
    # First try OAuth 2.0
    access_token = test_google_oauth2_token()
    if access_token:
        test_places_autocomplete(access_token=access_token)
    
    # Fall back to API key if OAuth 2.0 fails
    api_key = os.getenv('GOOGLE_PLACES_API_KEY')
    if api_key and (not access_token or input("\nTest with API key as well? (y/n): ").lower() == 'y'):
        test_places_autocomplete(api_key=api_key)
