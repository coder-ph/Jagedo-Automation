# Google Places Autocomplete Integration

This document provides an overview of the Google Places Autocomplete integration in the Jagedo Backend.

## Features

- Search for places using Google Places Autocomplete API
- Get detailed place information
- Location biasing for more relevant results
- OAuth 2.0 authentication with Google
- Example frontend implementation

## Prerequisites

1. Google Cloud Project with the following APIs enabled:
   - Places API
   - Geocoding API

2. OAuth 2.0 Client ID credentials
   - Configure the authorized JavaScript origins and redirect URIs in the Google Cloud Console

3. API Key for Places API

## Environment Variables

Add the following to your `.env` file:

```
# Google OAuth 2.0 Configuration
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
GOOGLE_PROJECT_ID=your-project-id
GOOGLE_REDIRECT_URI=http://localhost:5000/api/auth/google/callback
GOOGLE_AUTH_URI=https://accounts.google.com/o/oauth2/auth
GOOGLE_TOKEN_URI=https://oauth2.googleapis.com/token
GOOGLE_USER_INFO_URI=https://www.googleapis.com/oauth2/v1/userinfo
GOOGLE_SCOPES=email profile https://www.googleapis.com/auth/places

# Google Places API
GOOGLE_PLACES_API_KEY=your-places-api-key

# Base URL for OAuth callbacks
BASE_URL=http://localhost:5000
```

## API Endpoints

### 1. Get OAuth URL

```
GET /api/places/auth/url
```

Returns the Google OAuth URL to initiate the authentication flow.

### 2. OAuth Callback

```
GET /api/places/auth/callback?code={auth_code}
```

Handles the OAuth callback from Google and stores the access token in the session.

### 3. Search for Places

```
GET /api/places/autocomplete?query={search_term}[&lat={latitude}&lng={longitude}]
```

Parameters:
- `query`: The search term (required)
- `lat`: Latitude for location biasing (optional)
- `lng`: Longitude for location biasing (optional)

### 4. Get Place Details

```
GET /api/places/details/{place_id}
```

## Example Frontend

An example frontend implementation is available at `/examples/places`. This demonstrates:

1. Google OAuth 2.0 authentication
2. Location-based place search
3. Displaying search results
4. Viewing place details

To access the example:

1. Start the Flask development server
2. Open `http://localhost:5000/examples/places` in your browser
3. Click "Sign in with Google" to authenticate
4. Start searching for places

## Implementation Notes

- The implementation uses both API key and OAuth 2.0 for authentication
- OAuth 2.0 is required for certain Places API features
- The API falls back to using the API key if OAuth is not available
- Access tokens are automatically refreshed when they expire

## Security Considerations

1. Keep your API keys and OAuth credentials secure
2. Restrict API key usage in the Google Cloud Console
3. Use HTTPS in production
4. Implement proper CORS policies
5. Rate limit your API endpoints

## Testing

Run the test suite with:

```bash
pytest tests/integration/test_places_api.py -v
```

## Troubleshooting

1. **Authentication Errors**:
   - Verify your OAuth client ID and secret are correct
   - Ensure the redirect URI is whitelisted in the Google Cloud Console
   - Check that the required scopes are requested

2. **API Errors**:
   - Verify your API key has the correct permissions
   - Check your Google Cloud Project's quota usage
   - Ensure the required APIs are enabled

3. **CORS Issues**:
   - Make sure your frontend origin is allowed in the CORS configuration
   - Check the browser's console for CORS-related errors
