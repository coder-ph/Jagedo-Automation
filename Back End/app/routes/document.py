from flask import Blueprint, request, jsonify, send_from_directory, current_app, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime
from ..extensions import db

from ..models import Attachment, Job, Bid, User, UserRole
from ..utils.decorators import role_required
from ..utils.helpers import allowed_file
from ..services.cloudinary_storage import cloudinary_storage

# Create document blueprint
document_bp = Blueprint('document', __name__)

def check_document_permission(attachment, user):
    """Check if user has permission to access the document"""
    # Admin can access any document
    if user.role == UserRole.ADMIN:
        return True
    
    # User can access their own documents
    if attachment.uploaded_by == user.id:
        return True
    
    # Check if user is the owner of the job
    if attachment.job_id and attachment.job.client_id == user.id:
        return True
    
    # Check if user is a professional with access to the job
    if attachment.job_id and user.role == UserRole.PROFESSIONAL:
        # Check if user has a bid on this job
        bid = Bid.query.filter_by(
            job_id=attachment.job_id,
            professional_id=user.id
        ).first()
        if bid:
            return True
    
    return False

@document_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_document():
    """
    Upload a document and associate it with a job, bid, or user profile.
    
    Request format:
    - file: The file to upload (required)
    - document_type: Type of document (profile, bid, job, other) - defaults to 'other'
    - job_id: ID of the job this document is associated with (optional)
    - bid_id: ID of the bid this document is associated with (optional)
    - user_id: ID of the user this document is associated with (defaults to current user)
    - title: Optional title for the document
    - description: Optional description of the document
    """
    current_user_id = get_jwt_identity()
    
    # Check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({
            'success': False,
            'error': 'No file part in the request.'
        }), 400
        
    file = request.files['file']
    
    # If the user does not select a file, the browser submits an empty file without a filename
    if file.filename == '':
        return jsonify({
            'success': False,
            'error': 'No selected file.'
        }), 400
    
    # Get additional data from form
    document_type = request.form.get('document_type', 'other').lower()
    job_id = request.form.get('job_id', type=int)
    bid_id = request.form.get('bid_id', type=int)
    user_id = request.form.get('user_id', current_user_id, type=int)
    title = request.form.get('title', '')
    description = request.form.get('description', '')
    
    # Validate document type
    valid_document_types = ['profile', 'bid', 'job', 'other']
    if document_type not in valid_document_types:
        return jsonify({
            'success': False,
            'error': f'Invalid document type. Must be one of: {valid_document_types}.'
        }), 400
    
    # Set folder based on document type
    folder = f"{document_type}s"
    
    # Validate file extension and get file info
    filename = secure_filename(file.filename)
    file_ext = os.path.splitext(filename)[1].lower().lstrip('.')
    
    # Get allowed extensions from config
    allowed_extensions = set()
    for ext_group in current_app.config['ALLOWED_EXTENSIONS'].values():
        allowed_extensions.update(ext_group)
    
    if file_ext not in allowed_extensions:
        return jsonify({
            'success': False,
            'error': f'File type not allowed. Allowed types: {allowed_extensions}.'
        }), 400
    
    # Generate a unique filename with timestamp
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    unique_filename = f"{timestamp}_{uuid.uuid4().hex}{os.path.splitext(filename)[1]}"
    
    try:
        # Read file content to get actual size
        file_content = file.read()
        file_size = len(file_content)
        
        # Reset file pointer
        file.seek(0)
        
        # Check file size limit (16MB)
        max_size = current_app.config.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024)
        if file_size > max_size:
            return jsonify({
                'success': False,
                'error': f'File size exceeds maximum allowed size of {max_size / (1024 * 1024):.1f}MB.'
            }), 400
        
        # Determine MIME type
        mime_type = file.content_type or 'application/octet-stream'
        
        # Upload to Cloudinary or local storage based on configuration
        if current_app.config.get('STORAGE_PROVIDER') == 'cloudinary':
            # Set resource type based on file type
            resource_type = 'auto'  # Let Cloudinary auto-detect
            if mime_type.startswith('image/'):
                resource_type = 'image'
            elif mime_type.startswith('video/'):
                resource_type = 'video'
            elif mime_type.startswith('application/pdf'):
                resource_type = 'raw'
            
            # Prepare context and tags for better organization in Cloudinary
            context = {
                'user_id': str(user_id),
                'document_type': document_type,
                'uploaded_at': datetime.utcnow().isoformat(),
                'title': title,
                'description': description
            }
            
            # Upload to Cloudinary with error handling
            try:
                result = cloudinary_storage.upload_file(
                    file,
                    subfolder=folder,
                    resource_type=resource_type,
                    context=context,
                    tags=[f"user_{user_id}", f"type_{document_type}"]
                )
                
                # Create attachment record
                attachment = Attachment(
                    file_url=result['public_id'],
                    public_url=result['secure_url'],
                    filename=filename,
                    mime_type=mime_type,
                    file_size=file_size,
                    uploaded_by=current_user_id,
                    user_id=user_id,
                    job_id=job_id,
                    bid_id=bid_id
                )
                
            except Exception as upload_error:
                current_app.logger.error(f'Cloudinary upload error: {str(upload_error)}')
                return jsonify({
                    'success': False,
                    'error': 'Failed to upload file to cloud storage.',
                    'details': str(upload_error)
                }), 500
                
        else:
            # Fallback to local storage
            try:
                os.makedirs(os.path.join(current_app.config['UPLOAD_FOLDER'], folder), exist_ok=True)
                file_path = os.path.join(folder, unique_filename)
                full_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file_path)
                
                # Save file
                file.save(full_path)
                
                # Verify file was saved
                if not os.path.exists(full_path):
                    raise IOError('Failed to save file to disk')
                
                # Update file size with actual size
                file_size = os.path.getsize(full_path)
                
                # Create attachment record
                attachment = Attachment(
                    file_url=file_path,
                    filename=filename,
                    mime_type=mime_type,
                    file_size=file_size,
                    uploaded_by=current_user_id,
                    user_id=user_id,
                    job_id=job_id,
                    bid_id=bid_id
                )
                
            except Exception as local_error:
                current_app.logger.error(f'Local file save error: {str(local_error)}')
                # Clean up partially saved file if it exists
                if 'full_path' in locals() and os.path.exists(full_path):
                    try:
                        os.remove(full_path)
                    except Exception as cleanup_error:
                        current_app.logger.error(f'Error cleaning up file {full_path}: {str(cleanup_error)}')
                
                return jsonify({
                    'success': False,
                    'error': 'Failed to save file to local storage.',
                    'details': str(local_error)
                }), 500
        
        # Add metadata to attachment
        if title:
            attachment.title = title
        if description:
            attachment.description = description
        
        db.session.add(attachment)
        db.session.commit()
        
        # Log successful upload
        current_app.logger.info(f'Successfully uploaded file {attachment.id} for user {user_id}')
        
        return jsonify({
            'success': True,
            'message': 'File uploaded successfully',
            'attachment': attachment.to_dict(),
            'download_url': attachment.get_download_url()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'File upload error: {str(e)}', exc_info=True)
        return jsonify({
            'success': False,
            'error': 'An unexpected error occurred while processing your request.',
            'details': str(e)
        }), 500

@document_bp.route('/download/<int:attachment_id>', methods=['GET'])
@jwt_required()
def download_document(attachment_id):
    """Download a document by attachment ID."""
    current_user_id = get_jwt_identity()
    user = db.session.get(User, current_user_id)
    
    try:
        attachment = Attachment.query.get_or_404(attachment_id)
        
        # Check if user has permission to access this file
        if not check_document_permission(attachment, user):
            return jsonify({
                'success': False,
                'error': 'Unauthorized to access this file.'
            }), 403
        
        # If using Cloudinary, redirect to the public URL
        if current_app.config.get('STORAGE_PROVIDER') == 'cloudinary':
            if not attachment.public_url:
                return jsonify({
                    'success': False,
                    'error': 'File URL not found.'
                }), 404
            
            # Generate a signed URL that expires in 1 hour
            try:
                download_url = cloudinary_storage.get_file_url(
                    attachment.file_url,
                    secure=True,
                    sign_url=True,
                    expiration=3600  # 1 hour
                )
                return jsonify({
                    'success': True,
                    'download_url': download_url
                })
            except Exception as e:
                current_app.logger.error(f'Failed to generate download URL: {str(e)}')
                return jsonify({
                    'success': False,
                    'error': 'Failed to generate download URL. Please try again.'
                }), 500
        else:
            # Fallback to local file system
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], attachment.file_url)
            
            # Check if file exists
            if not os.path.exists(file_path):
                return jsonify({
                    'success': False,
                    'error': 'File not found.'
                }), 404
            
            # Send the file
            return send_from_directory(
                directory=os.path.dirname(file_path),
                path=os.path.basename(file_path),
                as_attachment=True,
                download_name=attachment.filename
            )
        
    except Exception as e:
        current_app.logger.error(f'Document download error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to download file. Please try again.'
        }), 500

@document_bp.route('/<int:attachment_id>', methods=['DELETE'])
@jwt_required()
def delete_document(attachment_id):
    """Delete a document."""
    current_user_id = get_jwt_identity()
    user = db.session.get(User, current_user_id)
    
    try:
        attachment = Attachment.query.get_or_404(attachment_id)
        
        # Check if user has permission to delete this file
        if not check_document_permission(attachment, user):
            return jsonify({
                'success': False,
                'error': 'Unauthorized to delete this file.'
            }), 403
        
        # Delete the file from storage
        if current_app.config.get('STORAGE_PROVIDER') == 'cloudinary':
            try:
                # Delete from Cloudinary
                cloudinary_storage.delete_file(attachment.file_url)
            except Exception as e:
                current_app.logger.error(f'Failed to delete file from Cloudinary: {str(e)}')
                # Continue with the deletion of the database record even if file deletion fails
        else:
            # Fallback to local file system
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], attachment.file_url)
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception as e:
                    current_app.logger.error(f'Failed to delete local file {file_path}: {str(e)}')
        
        # Delete the attachment record
        db.session.delete(attachment)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'File deleted successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Document deletion error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to delete file. Please try again.'
        }), 500
