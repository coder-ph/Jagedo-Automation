import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from flask import session, redirect, url_for, current_app
import json
from datetime import datetime, timedelta

class GoogleOAuthService:
    """Service for handling Google OAuth 2.0 authentication"""
    
    @staticmethod
    def get_google_auth_flow():
        """Create and return a Flow instance for Google OAuth"""
        return Flow.from_client_config(
            client_config={
                "web": {
                    "client_id": current_app.config['GOOGLE_CLIENT_ID'],
                    "client_secret": current_app.config['GOOGLE_CLIENT_SECRET'],
                    "auth_uri": current_app.config['GOOGLE_AUTH_URI'],
                    "token_uri": current_app.config['GOOGLE_TOKEN_URI'],
                    "redirect_uris": [current_app.config['GOOGLE_REDIRECT_URI']],
                    "javascript_origins": [current_app.config['BASE_URL']]
                }
            },
            scopes=current_app.config['GOOGLE_SCOPES'].split(),
            redirect_uri=current_app.config['GOOGLE_REDIRECT_URI']
        )
    
    @staticmethod
    def get_auth_url():
        """Generate authorization URL for Google OAuth"""
        flow = GoogleOAuthService.get_google_auth_flow()
        auth_url, _ = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent'
        )
        return auth_url
    
    @staticmethod
    def get_tokens(auth_code):
        """Exchange authorization code for tokens"""
        flow = GoogleOAuthService.get_google_auth_flow()
        flow.fetch_token(code=auth_code)
        
        credentials = flow.credentials
        
        return {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes,
            'expires_at': credentials.expiry.isoformat() if credentials.expiry else None
        }
    
    @staticmethod
    def is_token_expired(token_info):
        """Check if the access token is expired"""
        if not token_info or 'expires_at' not in token_info or not token_info['expires_at']:
            return True
            
        expires_at = datetime.fromisoformat(token_info['expires_at'])
        return datetime.utcnow() >= expires_at
    
    @staticmethod
    def refresh_token_if_needed(token_info):
        """Refresh the access token if it's expired"""
        if not GoogleOAuthService.is_token_expired(token_info):
            return token_info
            
        credentials = Credentials(
            token=token_info.get('token'),
            refresh_token=token_info.get('refresh_token'),
            token_uri=token_info.get('token_uri'),
            client_id=token_info.get('client_id'),
            client_secret=token_info.get('client_secret'),
            scopes=token_info.get('scopes')
        )
        
        if not credentials.valid:
            credentials.refresh(Request())
            
            return {
                'token': credentials.token,
                'refresh_token': credentials.refresh_token or token_info.get('refresh_token'),
                'token_uri': credentials.token_uri,
                'client_id': credentials.client_id,
                'client_secret': credentials.client_secret,
                'scopes': credentials.scopes,
                'expires_at': credentials.expiry.isoformat() if credentials.expiry else None
            }
            
        return token_info
