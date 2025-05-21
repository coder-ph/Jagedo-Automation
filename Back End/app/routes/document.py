from flask import Blueprint, request, jsonify, send_from_directory, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import os
import uuid
from ..extensions import db

from ..models import db, Attachment, Job, Bid, User, UserRole
from ..utils.decorators import role_required
from ..utils.helpers import allowed_file, save_uploaded_file

# Create document blueprint
document_bp = Blueprint('document', __name__)

@document_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_document():
    """Upload a document and associate it with a job, bid, or user profile."""
    current_user_id = get_jwt_identity()
    
    # Check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({
            'success': False,
            'error': 'No file part in the request.'
        }), 400
    
    file = request.files['file']
    
    # If user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return jsonify({
            'success': False,
            'error': 'No selected file.'
        }), 400
    
    if file and allowed_file(file.filename):
        try:
            # Get additional data from form
            document_type = request.form.get('document_type', 'other')
            job_id = request.form.get('job_id')
            bid_id = request.form.get('bid_id')
            
            # Determine the upload directory based on document type
            if document_type == 'profile':
                upload_dir = 'profile_documents'
                subfolder = f'user_{current_user_id}'
            elif document_type == 'bid' and bid_id:
                upload_dir = 'bid_documents'
                subfolder = f'bid_{bid_id}'
            else:  # Default to job documents
                upload_dir = 'job_documents'
                subfolder = f'job_{job_id}' if job_id else 'other'
            
            # Save the file
            filename = secure_filename(file.filename)
            file_url = save_uploaded_file(file, upload_dir, subfolder)
            
            if not file_url:
                return jsonify({
                    'success': False,
                    'error': 'Failed to save file.'
                }), 500
            
            # Create attachment record
            attachment = Attachment(
                file_url=file_url,
                filename=filename,
                uploaded_by=current_user_id,
                user_id=current_user_id,
                job_id=int(job_id) if job_id and job_id.isdigit() else None,
                bid_id=int(bid_id) if bid_id and bid_id.isdigit() else None
            )
            
            db.session.add(attachment)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'File uploaded successfully',
                'attachment': attachment.to_dict()
            }), 201
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Document upload error: {str(e)}')
            return jsonify({
                'success': False,
                'error': 'Failed to upload file. Please try again.'
            }), 500
    else:
        return jsonify({
            'success': False,
            'error': 'File type not allowed.'
        }), 400

@document_bp.route('/download/<int:attachment_id>', methods=['GET'])
@jwt_required()
def download_document(attachment_id):
    """Download a document by attachment ID."""
    current_user_id = get_jwt_identity()
    user = db.session.get(User, current_user_id)
    
    try:
        attachment = Attachment.query.get_or_404(attachment_id)
        
        # Debug logging
        current_app.logger.debug(f"Attachment details: {attachment.to_dict() if hasattr(attachment, 'to_dict') else 'No to_dict method'}")
        current_app.logger.debug(f"Current user ID: {current_user_id}, Role: {user.role}")
        
        # Check if user has permission to access this file
        has_permission = False
        
        # User is the uploader or the file is assigned to them
        if attachment.uploaded_by == current_user_id or attachment.user_id == current_user_id:
            current_app.logger.debug("Permission granted: User is the uploader or file is assigned to them")
            has_permission = True
        # User is an admin
        elif user.role == UserRole.ADMIN:
            current_app.logger.debug("Permission granted: User is an admin")
            has_permission = True
        # File is associated with a job the user owns
        elif attachment.job and attachment.job.customer_id == current_user_id:
            current_app.logger.debug("Permission granted: User owns the job")
            has_permission = True
        # File is associated with a bid the user made
        elif attachment.bid and attachment.bid.professional_id == current_user_id:
            current_app.logger.debug("Permission granted: User made the bid")
            has_permission = True
        # User is a professional who has placed a bid on the project
        elif attachment.job and user.role == UserRole.PROFESSIONAL:
            from app.models.bid import Bid
            from app.models.job import JobStatus
            
            # If project is awarded, only the winning professional has access
            if attachment.job.status == JobStatus.AWARDED:
                if attachment.job.assigned_contractor_id == current_user_id:
                    current_app.logger.debug("Permission granted: User is the winning professional")
                    has_permission = True
                else:
                    current_app.logger.debug("Permission denied: Project is awarded to another professional")
            # If project is still open, any professional with a bid has access
            elif attachment.job.status == JobStatus.OPEN:
                # Check if the user has any bids on this job
                has_bid = Bid.query.filter_by(
                    job_id=attachment.job.id,
                    professional_id=current_user_id,
                    status='pending'  # Only consider active/pending bids
                ).first() is not None
                current_app.logger.debug(f"Professional has active bid on job {attachment.job.id}: {has_bid}")
                if has_bid:
                    has_permission = True
        
        if not has_permission:
            return jsonify({
                'success': False,
                'error': 'Unauthorized to access this file.'
            }), 403
        
        # Get the file path
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
        has_permission = False
        
        # User is the uploader or the file is assigned to them
        if attachment.uploaded_by == current_user_id or attachment.user_id == current_user_id:
            has_permission = True
        # User is an admin
        elif user.role == UserRole.ADMIN:
            has_permission = True
        # File is associated with a job the user owns
        elif attachment.job and attachment.job.customer_id == current_user_id:
            has_permission = True
        # File is associated with a bid the user made
        elif attachment.bid and attachment.bid.professional_id == current_user_id:
            has_permission = True
        
        if not has_permission:
            return jsonify({
                'success': False,
                'error': 'Unauthorized to delete this file.'
            }), 403
        
        # Get the file path
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], attachment.file_url)
        
        # Delete the file from storage
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                current_app.logger.error(f'Failed to delete file {file_path}: {str(e)}')
        
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
