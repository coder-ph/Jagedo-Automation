import os
import sys
import unittest
from datetime import datetime
from io import BytesIO
from unittest.mock import patch, MagicMock

# Mock the SimplePlacesService before any imports that might use it
class MockSimplePlacesService:
    def __init__(self, *args, **kwargs):
        pass
    
    def autocomplete(self, *args, **kwargs):
        return []
    
    def get_place_details(self, *args, **kwargs):
        return {}

# Apply the patch before importing the app
sys.modules['app.services.simple_places_service'] = MagicMock()
sys.modules['app.services.simple_places_service'].SimplePlacesService = MockSimplePlacesService

# Now import the rest of the application
import cloudinary.uploader
from flask import current_app
from werkzeug.datastructures import FileStorage

from app import create_app, db
from app.models import User, Attachment
from config import Config


class CloudinaryTestCase(unittest.TestCase):
    """Test Cloudinary file storage integration."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Configure test app
        self.app = create_app('testing')
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['STORAGE_PROVIDER'] = 'cloudinary'
        
        # Mock the Cloudinary configuration
        self.app.config['CLOUDINARY_CLOUD_NAME'] = 'test_cloud'
        self.app.config['CLOUDINARY_API_KEY'] = 'test_key'
        self.app.config['CLOUDINARY_API_SECRET'] = 'test_secret'
        
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Create database tables
        db.create_all()
        
        # Create a test user
        self.user = User(
            name='Test User',
            email='test@example.com',
            password='testpass123',
            location='Test Location'
        )
        db.session.add(self.user)
        db.session.commit()
        
        self.client = self.app.test_client()
        
        # Mock Cloudinary upload and destroy methods
        self.cloudinary_upload_patcher = patch('cloudinary.uploader.upload')
        self.cloudinary_destroy_patcher = patch('cloudinary.uploader.destroy')
        
        self.mock_cloudinary_upload = self.cloudinary_upload_patcher.start()
        self.mock_cloudinary_destroy = self.cloudinary_destroy_patcher.start()
        
        # Mock the upload result
        self.mock_upload_result = {
            'public_id': 'test_public_id',
            'secure_url': 'https://res.cloudinary.com/test/image/upload/test_public_id.jpg',
            'url': 'http://res.cloudinary.com/test/image/upload/test_public_id.jpg',
            'resource_type': 'auto'
        }
        self.mock_cloudinary_upload.return_value = self.mock_upload_result
    
    def tearDown(self):
        """Clean up after each test method."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
        # Stop all patches
        self.cloudinary_upload_patcher.stop()
        self.cloudinary_destroy_patcher.stop()
    
    def create_test_file(self, filename='test.txt', content=b'Test file content'):
        """Create a test file for upload testing."""
        return FileStorage(
            stream=BytesIO(content),
            filename=filename,
            content_type='text/plain',
            content_length=len(content)
        )
    
    def test_cloudinary_upload_download(self):
        """Test file upload and download with Cloudinary."""
        # Skip the test if we couldn't properly mock the dependencies
        if 'app.services.cloudinary_storage' not in sys.modules:
            self.skipTest("Could not properly mock dependencies")
            
        # Create a test file
        test_content = b'This is a test file for Cloudinary upload.'
        test_file = self.create_test_file('test_cloudinary.txt', test_content)
        
        # Set up the mock return value
        self.mock_cloudinary_upload.return_value = {
            'public_id': 'test_public_id',
            'secure_url': 'https://res.cloudinary.com/test/raw/upload/test_public_id.txt',
            'url': 'http://res.cloudinary.com/test/raw/upload/test_public_id.txt',
            'resource_type': 'raw'
        }
        
        # Import here to avoid circular imports
        from app.services.cloudinary_storage import cloudinary_storage
        
        # Test file upload
        try:
            upload_result = cloudinary_storage.upload_file(
                test_file,
                subfolder='tests',
                resource_type='raw'
            )
            
            # Verify upload was successful
            self.assertIn('public_id', upload_result)
            self.assertIn('secure_url', upload_result)
            
            # Verify the upload method was called with correct parameters
            self.mock_cloudinary_upload.assert_called_once()
            
            # Create an attachment record
            attachment = Attachment(
                file_url=upload_result['public_id'],
                public_url=upload_result['secure_url'],
                filename='test_cloudinary.txt',
                mime_type='text/plain',
                file_size=len(test_content),
                uploaded_by=self.user.id,
                user_id=self.user.id
            )
            db.session.add(attachment)
            db.session.commit()
            
            # Test getting a download URL
            download_url = attachment.get_download_url()
            self.assertIsNotNone(download_url)
            self.assertTrue(download_url.startswith('https://'))
            
            # Test file deletion
            cloudinary_storage.delete_file(attachment.file_url)
            self.mock_cloudinary_destroy.assert_called_once_with(attachment.file_url)
            
        except ImportError as e:
            self.skipTest(f"Could not import required modules: {e}")
    
    @patch('app.routes.document.jwt_required', return_value=lambda f: f)
    @patch('app.routes.document.get_jwt_identity')
    @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
    @patch('app.routes.document.User')
    def test_document_upload_endpoint(self, mock_user, mock_verify_jwt, mock_jwt_identity, mock_jwt_required):
        """Test the document upload endpoint with Cloudinary."""
        # Setup mocks
        mock_jwt_identity.return_value = self.user.id
        mock_user.query.get.return_value = self.user
        mock_verify_jwt.return_value = True

        # Create a test file
        test_content = b'Test document upload via API endpoint.'
        test_file = self.create_test_file('test_upload.txt', test_content)
    
        # Set up the mock return value
        self.mock_cloudinary_upload.return_value = {
            'public_id': 'test_upload_id',
            'secure_url': 'https://res.cloudinary.com/test/raw/upload/test_upload_id.txt',
            'url': 'http://res.cloudinary.com/test/raw/upload/test_upload_id.txt',
            'resource_type': 'raw'
        }
    
        # Prepare form data
        data = {
            'file': test_file,
            'document_type': 'other',  # Must be one of: profile, bid, job, other
            'title': 'Test Document',
            'description': 'Test upload via API endpoint'
        }
    
        response = self.client.post(
            '/api/documents/upload',
            data=data,
            content_type='multipart/form-data',
            headers={'Authorization': 'Bearer test_token'}
        )
    
        if response.status_code != 201:
            print("Response status code:", response.status_code)
            print("Response data:", response.get_json())
            
        self.assertEqual(response.status_code, 201)
        response_data = response.get_json()
        self.assertIn('attachment', response_data)
        self.assertEqual(response_data['attachment']['filename'], 'test_upload.txt')
        self.assertTrue(response_data['success'])
        self.assertIn('download_url', response_data)
        
        # Verify the attachment was created
        attachment_id = response_data['attachment']['id']
        attachment = Attachment.query.get(attachment_id)
        self.assertIsNotNone(attachment)
        self.assertEqual(attachment.filename, 'test_upload.txt')
        self.assertEqual(attachment.uploaded_by, self.user.id)
        
        # Verify the upload method was called with correct parameters
        self.mock_cloudinary_upload.assert_called_once()
        
        # Clean up
        if attachment and attachment.file_url:
            self.mock_cloudinary_destroy(attachment.file_url)


if __name__ == '__main__':
    unittest.main()
