"""
Background tasks for file processing.
"""
import os
import logging
import magic
from datetime import datetime
from typing import Dict, Any, Optional, Tuple
from pathlib import Path

from PIL import Image, UnidentifiedImageError
import PyPDF2
from werkzeug.utils import secure_filename

from ..extensions import db
from ..models import File, User
from ..utils.storage import storage
from .celery import celery_app

logger = logging.getLogger(__name__)

class FileProcessingError(Exception):
    """Base exception for file processing errors."""
    pass

def process_file_upload(
    file_storage,
    user_id: int,
    category: str = 'user_uploads',
    metadata: Dict[str, Any] = None,
    max_size: int = None
) -> File:
    """
    Process an uploaded file in the background.
    
    Args:
        file_storage: FileStorage object from request.files
        user_id: ID of the user uploading the file
        category: Category for the file (e.g., 'profile_image', 'document')
        metadata: Additional metadata to store with the file
        max_size: Maximum file size in bytes (overrides default)
        
    Returns:
        File: The created file record
    """
    try:
        # Validate user
        user = User.query.get(user_id)
        if not user:
            raise FileProcessingError(f"User {user_id} not found")
        
        # Get file info
        original_filename = secure_filename(file_storage.filename)
        file_ext = os.path.splitext(original_filename)[1].lower()
        content_type = file_storage.content_type
        
        # Read file content to get size and hash
        file_content = file_storage.read()
        file_size = len(file_content)
        
        # Check file size
        max_size = max_size or current_app.config.get('MAX_FILE_SIZE', 10 * 1024 * 1024)  # 10MB default
        if file_size > max_size:
            raise FileProcessingError(f"File size exceeds maximum allowed size of {max_size} bytes")
        
        # Detect MIME type
        mime = magic.Magic(mime=True)
        detected_type = mime.from_buffer(file_content)
        
        # Validate file type based on category
        if not is_file_type_allowed(detected_type, file_ext, category):
            raise FileProcessingError(f"File type not allowed for category '{category}'")
        
        # Generate a unique filename
        unique_id = str(uuid.uuid4().hex[:8])
        safe_filename = f"{unique_id}_{original_filename}"
        
        # Save file to storage
        file_path = storage.save_file(
            file_content,
            filename=safe_filename,
            folder=category,
            content_type=detected_type
        )
        
        # Create file record
        file_record = File(
            user_id=user_id,
            original_filename=original_filename,
            stored_filename=safe_filename,
            file_path=file_path,
            file_size=file_size,
            mime_type=detected_type,
            category=category,
            metadata=metadata or {}
        )
        
        db.session.add(file_record)
        db.session.commit()
        
        # Trigger additional processing based on file type
        if detected_type.startswith('image/'):
            process_image.delay(file_record.id)
        elif detected_type == 'application/pdf':
            process_pdf.delay(file_record.id)
        
        return file_record
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error processing file upload: {str(e)}")
        raise FileProcessingError(f"Failed to process file: {str(e)}")

def is_file_type_allowed(mime_type: str, file_ext: str, category: str) -> bool:
    """
    Check if a file type is allowed for a given category.
    
    Args:
        mime_type: Detected MIME type
        file_ext: File extension (with dot)
        category: File category
        
    Returns:
        bool: True if the file type is allowed
    """
    # Define allowed types per category
    allowed_types = {
        'profile_image': {
            'mime_types': {'image/jpeg', 'image/png', 'image/gif'},
            'extensions': {'.jpg', '.jpeg', '.png', '.gif'}
        },
        'document': {
            'mime_types': {
                'application/pdf',
                'application/msword',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'application/vnd.ms-excel',
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                'text/plain',
                'text/csv'
            },
            'extensions': {
                '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.txt', '.csv'
            }
        },
        'user_uploads': {
            'mime_types': None,  # All types allowed
            'extensions': None
        }
    }
    
    # Default to user_uploads if category not found
    category_rules = allowed_types.get(category, allowed_types['user_uploads'])
    
    # Check MIME type if rules exist
    if category_rules['mime_types'] and mime_type not in category_rules['mime_types']:
        return False
    
    # Check file extension if rules exist
    if category_rules['extensions'] and file_ext.lower() not in category_rules['extensions']:
        return False
    
    return True

@celery_app.task(bind=True, max_retries=3)
def process_image(self, file_id: int) -> Dict[str, Any]:
    """
    Process an uploaded image (resize, create thumbnails, etc.).
    
    Args:
        file_id: ID of the file to process
        
    Returns:
        dict: Processing results
    """
    try:
        file_record = File.query.get(file_id)
        if not file_record:
            raise FileProcessingError(f"File {file_id} not found")
        
        if not file_record.mime_type.startswith('image/'):
            raise FileProcessingError(f"File {file_id} is not an image")
        
        # Load the image
        try:
            image_path = storage.get_file_path(file_record.stored_filename, file_record.category)
            with Image.open(image_path) as img:
                # Get image info
                width, height = img.size
                format = img.format
                mode = img.mode
                
                # Update file metadata
                file_record.metadata.update({
                    'width': width,
                    'height': height,
                    'format': format,
                    'mode': mode,
                    'processed': True,
                    'processed_at': datetime.utcnow().isoformat()
                })
                
                # Create thumbnail if it's a profile image
                if file_record.category == 'profile_image':
                    # Create thumbnail (200x200)
                    img.thumbnail((200, 200))
                    thumb_filename = f"thumb_{file_record.stored_filename}"
                    thumb_path = storage.get_file_path(thumb_filename, file_record.category)
                    
                    # Save thumbnail
                    img.save(thumb_path, format=format or 'JPEG')
                    
                    # Update metadata with thumbnail info
                    file_record.metadata['thumbnail'] = thumb_filename
                
                db.session.commit()
                
                return {
                    'success': True,
                    'file_id': file_id,
                    'dimensions': f"{width}x{height}",
                    'format': format,
                    'thumbnail_created': file_record.category == 'profile_image'
                }
                
        except (IOError, UnidentifiedImageError) as e:
            raise FileProcessingError(f"Invalid image file: {str(e)}")
            
    except Exception as e:
        logger.error(f"Error processing image {file_id}: {str(e)}")
        try:
            raise self.retry(exc=e, countdown=60 * (2 ** (self.request.retries - 1)))
        except self.MaxRetriesExceededError:
            logger.error(f"Max retries exceeded for image processing {file_id}")
            return {
                'success': False,
                'file_id': file_id,
                'error': str(e)
            }

@celery_app.task(bind=True, max_retries=3)
def process_pdf(self, file_id: int) -> Dict[str, Any]:
    """
    Process an uploaded PDF file (extract text, page count, etc.).
    
    Args:
        file_id: ID of the file to process
        
    Returns:
        dict: Processing results
    """
    try:
        file_record = File.query.get(file_id)
        if not file_record:
            raise FileProcessingError(f"File {file_id} not found")
            
        if file_record.mime_type != 'application/pdf':
            raise FileProcessingError(f"File {file_id} is not a PDF")
            
        # Process the PDF
        file_path = storage.get_file_path(file_record.stored_filename, file_record.category)
        
        with open(file_path, 'rb') as f:
            pdf = PyPDF2.PdfReader(f)
            
            # Extract basic info
            num_pages = len(pdf.pages)
            
            # Extract text from first page for preview
            preview_text = ""
            if num_pages > 0:
                first_page = pdf.pages[0]
                preview_text = first_page.extract_text()[:500]  # First 500 chars
            
            # Update file metadata
            file_record.metadata.update({
                'page_count': num_pages,
                'preview_text': preview_text,
                'processed': True,
                'processed_at': datetime.utcnow().isoformat()
            })
            
            db.session.commit()
            
            return {
                'success': True,
                'file_id': file_id,
                'page_count': num_pages,
                'preview_text_length': len(preview_text)
            }
            
    except Exception as e:
        logger.error(f"Error processing PDF {file_id}: {str(e)}")
        try:
            raise self.retry(exc=e, countdown=60 * (2 ** (self.request.retries - 1)))
        except self.MaxRetriesExceededError:
            logger.error(f"Max retries exceeded for PDF processing {file_id}")
            return {
                'success': False,
                'file_id': file_id,
                'error': str(e)
            }

@celery_app.task
def cleanup_orphaned_files() -> Dict[str, Any]:
    """
    Clean up files that don't have corresponding database records.
    
    Returns:
        dict: Cleanup results
    """
    try:
        # Get all files in storage
        all_files = set()
        for category in storage.list_folders():
            for file in storage.list_files(category):
                all_files.add((category, file))
        
        # Get all files referenced in the database
        db_files = set()
        for file in File.query.with_entities(File.category, File.stored_filename).all():
            db_files.add((file.category, file.stored_filename))
        
        # Find orphaned files (in storage but not in DB)
        orphaned = all_files - db_files
        
        # Delete orphaned files
        deleted = 0
        for category, filename in orphaned:
            try:
                if storage.delete_file(filename, category):
                    deleted += 1
            except Exception as e:
                logger.error(f"Error deleting orphaned file {category}/{filename}: {str(e)}")
        
        return {
            'success': True,
            'total_files': len(all_files),
            'orphaned_files': len(orphaned),
            'deleted': deleted
        }
        
    except Exception as e:
        logger.error(f"Error in cleanup_orphaned_files: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }
