import os
import uuid
import mimetypes
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import current_app, request, abort
from pathlib import Path
from typing import Dict, Optional, Tuple, BinaryIO, Union
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

class StorageService:
    """Service for handling file uploads and storage."""
    
    def __init__(self, app=None):
        """Initialize the storage service."""
        self.app = None
        self.upload_folder = None
        self.max_content_length = None
        self.allowed_extensions = None
        self.base_url = None
        
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize the storage service with the Flask app."""
        self.app = app
        
        # Configure storage
        self.upload_folder = app.config.get('UPLOAD_FOLDER', 'uploads')
        self.max_content_length = app.config.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024)  # 16MB default
        self.allowed_extensions = app.config.get('ALLOWED_EXTENSIONS', {
            'images': {'jpg', 'jpeg', 'png', 'gif', 'webp'},
            'documents': {'pdf', 'doc', 'docx', 'txt', 'rtf'},
            'archives': {'zip', 'rar', '7z'},
            'spreadsheets': {'xls', 'xlsx', 'csv'},
            'presentations': {'ppt', 'pptx'},
            'code': {'py', 'js', 'html', 'css', 'json', 'xml'},
        })
        
        # Ensure upload directory exists
        os.makedirs(self.upload_folder, exist_ok=True)
        
        # Set base URL for file access
        self.base_url = app.config.get('FILE_SERVE_URL', '/files/')
        
        # Add to app.extensions
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['storage'] = self
    
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
    
    def get_secure_filename(self, filename: str) -> str:
        """
        Generate a secure filename.
        
        Args:
            filename: Original filename
            
        Returns:
            str: Secure filename
        """
        # Generate a unique filename to prevent collisions
        ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        unique_id = uuid.uuid4().hex[:8]
        secure_name = secure_filename(filename)
        
        if ext:
            return f"{os.path.splitext(secure_name)[0]}_{unique_id}.{ext}"
        return f"{secure_name}_{unique_id}"
    
    def get_file_path(self, filename: str, subfolder: str = '') -> str:
        """
        Get the full filesystem path for a file.
        
        Args:
            filename: Name of the file
            subfolder: Optional subfolder within the upload directory
            
        Returns:
            str: Full filesystem path
        """
        if subfolder:
            return os.path.join(self.upload_folder, subfolder, filename)
        return os.path.join(self.upload_folder, filename)
    
    def get_file_url(self, filename: str, subfolder: str = '') -> str:
        """
        Get the URL to access a file.
        
        Args:
            filename: Name of the file
            subfolder: Optional subfolder within the upload directory
            
        Returns:
            str: URL to access the file
        """
        if subfolder:
            return urljoin(self.base_url, f"{subfolder}/{filename}")
        return urljoin(self.base_url, filename)
    
    def save_file(
        self, 
        file_storage, 
        subfolder: str = '', 
        category: str = None,
        max_size: int = None
    ) -> Dict[str, str]:
        """
        Save an uploaded file.
        
        Args:
            file_storage: FileStorage object from request.files
            subfolder: Optional subfolder to save the file in
            category: Optional category to validate file type
            max_size: Maximum file size in bytes (overrides default)
            
        Returns:
            dict: Dictionary containing file information
            
        Raises:
            FileTooLargeError: If the file exceeds the maximum size
            InvalidFileTypeError: If the file type is not allowed
        """
        if not file_storage or file_storage.filename == '':
            raise ValueError("No file provided")
        
        # Check file size
        max_size = max_size or self.max_content_length
        file_storage.seek(0, os.SEEK_END)
        file_size = file_storage.tell()
        file_storage.seek(0)
        
        if file_size > max_size:
            raise FileTooLargeError(f"File size exceeds maximum allowed size of {max_size} bytes")
        
        # Check file extension
        if not self.is_allowed_file(file_storage.filename, category):
            raise InvalidFileTypeError("File type not allowed")
        
        # Generate secure filename
        filename = self.get_secure_filename(file_storage.filename)
        
        # Create subfolder if it doesn't exist
        if subfolder:
            subfolder_path = os.path.join(self.upload_folder, subfolder)
            os.makedirs(subfolder_path, exist_ok=True)
            file_path = os.path.join(subfolder_path, filename)
        else:
            file_path = os.path.join(self.upload_folder, filename)
        
        try:
            # Save the file
            file_storage.save(file_path)
            
            # Get file info
            file_info = {
                'filename': filename,
                'original_filename': file_storage.filename,
                'content_type': file_storage.content_type or mimetypes.guess_type(filename)[0] or 'application/octet-stream',
                'size': file_size,
                'path': file_path,
                'url': self.get_file_url(filename, subfolder),
                'uploaded_at': datetime.utcnow().isoformat(),
                'subfolder': subfolder
            }
            
            return file_info
            
        except Exception as e:
            logger.error(f"Error saving file: {str(e)}")
            # Clean up if file was partially saved
            if os.path.exists(file_path):
                os.remove(file_path)
            raise StorageError(f"Failed to save file: {str(e)}")
    
    def delete_file(self, filename: str, subfolder: str = '') -> bool:
        """
        Delete a file.
        
        Args:
            filename: Name of the file to delete
            subfolder: Optional subfolder where the file is located
            
        Returns:
            bool: True if the file was deleted, False otherwise
        """
        try:
            file_path = self.get_file_path(filename, subfolder)
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting file {filename}: {str(e)}")
            return False
    
    def get_file_info(self, filename: str, subfolder: str = '') -> Optional[Dict]:
        """
        Get information about a file.
        
        Args:
            filename: Name of the file
            subfolder: Optional subfolder where the file is located
            
        Returns:
            dict: File information or None if file doesn't exist
        """
        file_path = self.get_file_path(filename, subfolder)
        
        if not os.path.exists(file_path):
            return None
        
        return {
            'filename': filename,
            'path': file_path,
            'url': self.get_file_url(filename, subfolder),
            'size': os.path.getsize(file_path),
            'last_modified': datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat(),
            'content_type': mimetypes.guess_type(filename)[0] or 'application/octet-stream',
            'subfolder': subfolder
        }
    
    def serve_file(self, filename: str, subfolder: str = ''):
        """
        Serve a file for download.
        
        Args:
            filename: Name of the file to serve
            subfolder: Optional subfolder where the file is located
            
        Returns:
            File response for Flask to serve
            
        Raises:
            FileNotFoundError: If the file doesn't exist
        """
        from flask import send_from_directory, safe_join, abort
        
        try:
            if subfolder:
                directory = os.path.join(self.upload_folder, subfolder)
                return send_from_directory(directory, filename, as_attachment=True)
            else:
                return send_from_directory(self.upload_folder, filename, as_attachment=True)
        except Exception as e:
            logger.error(f"Error serving file {filename}: {str(e)}")
            abort(404)

# Create a default instance
storage = StorageService()

def init_storage(app):
    """Initialize the storage service with the Flask app."""
    storage.init_app(app)
    return storage
