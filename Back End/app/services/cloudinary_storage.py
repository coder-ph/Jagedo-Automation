import cloudinary
import cloudinary.uploader
import cloudinary.api
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime
from typing import Dict, Optional, Tuple, BinaryIO, Union, Any
import logging
from urllib.parse import urljoin

logger = logging.getLogger(__name__)

class StorageError(Exception):
    """Base exception for storage-related errors."""
    pass

class FileTooLargeError(StorageError):
    """Raised when a file exceeds the maximum allowed size."""
    pass

class InvalidFileTypeError(StorageError):
    """Raised when a file type is not allowed."""
    pass

class CloudinaryStorage:
    """Service for handling file uploads and storage with Cloudinary."""
    
    def __init__(self, app=None):
        """Initialize the Cloudinary storage service."""
        self.app = None
        self.allowed_extensions = {
            'images': {'jpg', 'jpeg', 'png', 'gif', 'webp'},
            'documents': {'pdf', 'doc', 'docx', 'txt', 'rtf'},
            'archives': {'zip', 'rar', '7z'},
            'spreadsheets': {'xls', 'xlsx', 'csv'},
            'presentations': {'ppt', 'pptx'},
            'code': {'py', 'js', 'html', 'css', 'json', 'xml'},
        }
        self.max_content_length = 16 * 1024 * 1024  # 16MB default
        
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize the storage service with the Flask app."""
        self.app = app
        
        # Configure Cloudinary
        cloudinary.config(
            cloud_name=app.config.get('CLOUDINARY_CLOUD_NAME'),
            api_key=app.config.get('CLOUDINARY_API_KEY'),
            api_secret=app.config.get('CLOUDINARY_API_SECRET')
        )
        
        # Update allowed extensions from app config if provided
        if 'ALLOWED_EXTENSIONS' in app.config:
            self.allowed_extensions = app.config['ALLOWED_EXTENSIONS']
        
        # Set max content length
        self.max_content_length = app.config.get('MAX_CONTENT_LENGTH', self.max_content_length)
    
    def get_allowed_extensions(self, category: str = None) -> set:
        """
        Get allowed file extensions.
        
        Args:
            category: Optional category to filter extensions
            
        Returns:
            set: Set of allowed file extensions
        """
        if category and category in self.allowed_extensions:
            return self.allowed_extensions[category]
        
        # Return all extensions if no category specified
        all_extensions = set()
        for ext_set in self.allowed_extensions.values():
            all_extensions.update(ext_set)
        return all_extensions
    
    def is_allowed_file(self, filename: str, category: str = None) -> bool:
        """
        Check if a file has an allowed extension.
        
        Args:
            filename: Name of the file to check
            category: Optional category to check against
            
        Returns:
            bool: True if the file extension is allowed, False otherwise
        """
        if '.' not in filename:
            return False
            
        ext = filename.rsplit('.', 1)[1].lower()
        return ext in self.get_allowed_extensions(category)
    
    def upload_file(self, file_storage, subfolder: str = 'uploads', **options) -> Dict[str, Any]:
        """
        Upload a file to Cloudinary.
        
        Args:
            file_storage: FileStorage object from request.files
            subfolder: Subfolder to store the file in
            **options: Additional options to pass to Cloudinary
            
        Returns:
            dict: Dictionary containing file information
            
        Raises:
            InvalidFileTypeError: If the file type is not allowed
            FileTooLargeError: If the file is too large
            StorageError: If the upload fails
        """
        if not file_storage or file_storage.filename == '':
            raise StorageError("No file provided")
            
        filename = secure_filename(file_storage.filename)
        
        # Check file extension
        if not self.is_allowed_file(filename):
            raise InvalidFileTypeError(f"File type not allowed: {filename}")
            
        # Check file size
        file_storage.seek(0, os.SEEK_END)
        file_size = file_storage.tell()
        file_storage.seek(0)
        
        if file_size > self.max_content_length:
            raise FileTooLargeError(f"File size exceeds maximum allowed size of {self.max_content_length} bytes")
        
        try:
            # Generate a unique public ID
            file_ext = filename.rsplit('.', 1)[1].lower()
            public_id = f"{subfolder}/{str(uuid.uuid4())}.{file_ext}"
            
            # Upload to Cloudinary
            result = cloudinary.uploader.upload(
                file_storage,
                public_id=public_id,
                **options
            )
            
            return {
                'public_id': result['public_id'],
                'secure_url': result['secure_url'],
                'url': result['url'],
                'format': result.get('format'),
                'resource_type': result.get('resource_type'),
                'bytes': result.get('bytes'),
                'created_at': result.get('created_at'),
                'original_filename': filename
            }
            
        except Exception as e:
            logger.error(f"Failed to upload file to Cloudinary: {str(e)}")
            raise StorageError(f"Failed to upload file: {str(e)}")
    
    def get_file_url(self, public_id: str, **options) -> str:
        """
        Get the URL for a file.
        
        Args:
            public_id: The public ID of the file
            **options: Additional options to pass to Cloudinary
            
        Returns:
            str: The URL of the file
        """
        try:
            return cloudinary.utils.cloudinary_url(public_id, **options)[0]
        except Exception as e:
            logger.error(f"Failed to generate URL for {public_id}: {str(e)}")
            raise StorageError(f"Failed to generate URL: {str(e)}")
    
    def delete_file(self, public_id: str, **options) -> bool:
        """
        Delete a file from Cloudinary.
        
        Args:
            public_id: The public ID of the file to delete
            **options: Additional options to pass to Cloudinary
            
        Returns:
            bool: True if the file was deleted successfully, False otherwise
        """
        try:
            result = cloudinary.uploader.destroy(public_id, **options)
            return result.get('result') == 'ok'
        except Exception as e:
            logger.error(f"Failed to delete file {public_id}: {str(e)}")
            raise StorageError(f"Failed to delete file: {str(e)}")

# Create a default instance
cloudinary_storage = CloudinaryStorage()
