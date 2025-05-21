from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import os
from datetime import datetime

from ..models import db, Job, User, Category, ProjectStatusHistory, JobStatus, UserRole
from ..utils.decorators import role_required
from ..utils.helpers import allowed_file, save_uploaded_file

# Create project blueprint
project_bp = Blueprint('project', __name__)

@project_bp.route('', methods=['POST'])
@jwt_required()
@role_required([UserRole.CUSTOMER, UserRole.ADMIN])
def create_project():
    """Create a new project."""
    current_user_id = get_jwt_identity()
    data = request.form
    
    # Validate required fields
    required_fields = ['title', 'description', 'category_id', 'location', 'budget']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({
                'success': False,
                'error': f'{field.replace("_", " ").title()} is required.'
            }), 400
    
    try:
        # Convert budget to float
        budget = float(data['budget'])
        if budget <= 0:
            return jsonify({
                'success': False,
                'error': 'Budget must be greater than 0.'
            }), 400
            
        # Check if category exists
        category = db.session.get(Category, data['category_id'])
        if not category:
            return jsonify({
                'success': False,
                'error': 'Invalid category.'
            }), 400
        
        # Create new project
        project = Job(
            title=data['title'],
            description=data['description'],
            category_id=category.id,
            customer_id=current_user_id,
            location=data['location'],
            budget=budget,
            status=JobStatus.OPEN
        )
        
        db.session.add(project)
        db.session.flush()  # Get the project ID for file uploads
        
        # Handle file uploads if any
        if 'documents' in request.files:
            files = request.files.getlist('documents')
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_url = save_uploaded_file(file, 'project_documents', f'project_{project.id}')
                    
                    if file_url:
                        attachment = Attachment(
                            file_url=file_url,
                            filename=filename,
                            uploaded_by=current_user_id,
                            job_id=project.id,
                            user_id=current_user_id
                        )
                        db.session.add(attachment)
        
        # Record status change
        status_history = ProjectStatusHistory(
            project_id=project.id,
            from_status=None,
            to_status=JobStatus.OPEN,
            changed_by=current_user_id,
            notes='Project created'
        )
        db.session.add(status_history)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Project created successfully',
            'project': project.to_dict()
        }), 201
        
    except ValueError:
        return jsonify({
            'success': False,
            'error': 'Invalid budget value. Must be a number.'
        }), 400
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Project creation error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to create project. Please try again.'
        }), 500

@project_bp.route('', methods=['GET'])
def get_projects():
    """Get all projects with optional filtering."""
    try:
        # Get query parameters
        status = request.args.get('status')
        category_id = request.args.get('category_id')
        location = request.args.get('location')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        
        # Base query
        query = Job.query.filter(Job.status != JobStatus.COMPLETED)
        
        # Apply filters
        if status:
            query = query.filter(Job.status == status)
        if category_id:
            query = query.filter(Job.category_id == category_id)
        if location:
            query = query.filter(Job.location.ilike(f'%{location}%'))
        
        # Pagination
        pagination = query.order_by(Job.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False)
        
        projects = [p.to_dict() for p in pagination.items]
        
        return jsonify({
            'success': True,
            'projects': projects,
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page
        })
        
    except Exception as e:
        current_app.logger.error(f'Get projects error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve projects. Please try again.'
        }), 500

@project_bp.route('/<int:project_id>', methods=['GET'])
def get_project(project_id):
    """Get project by ID."""
    try:
        project = Job.query.get_or_404(project_id)
        
        return jsonify({
            'success': True,
            'project': project.to_dict(include_details=True)
        })
        
    except Exception as e:
        current_app.logger.error(f'Get project error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve project. Please try again.'
        }), 500

@project_bp.route('/<int:project_id>', methods=['PUT'])
@jwt_required()
def update_project(project_id):
    """Update project details."""
    current_user_id = get_jwt_identity()
    data = request.form
    
    try:
        project = Job.query.get_or_404(project_id)
        
        # Check if user is the owner or admin
        if project.customer_id != current_user_id and User.query.get(current_user_id).role != UserRole.ADMIN:
            return jsonify({
                'success': False,
                'error': 'Unauthorized to update this project.'
            }), 403
        
        # Update allowed fields
        allowed_fields = ['title', 'description', 'category_id', 'location', 'budget', 'status']
        
        for field in allowed_fields:
            if field in data:
                if field == 'status' and data[field] != project.status:
                    # Record status change
                    status_history = ProjectStatusHistory(
                        project_id=project.id,
                        from_status=project.status,
                        to_status=data[field],
                        changed_by=current_user_id,
                        notes=data.get('status_notes', 'Status updated')
                    )
                    db.session.add(status_history)
                setattr(project, field, data[field])
        
        # Handle file uploads if any
        if 'documents' in request.files:
            files = request.files.getlist('documents')
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_url = save_uploaded_file(file, 'project_documents', f'project_{project.id}')
                    
                    if file_url:
                        attachment = Attachment(
                            file_url=file_url,
                            filename=filename,
                            uploaded_by=current_user_id,
                            job_id=project.id,
                            user_id=current_user_id
                        )
                        db.session.add(attachment)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Project updated successfully',
            'project': project.to_dict(include_details=True)
        })
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Project update error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to update project. Please try again.'
        }), 500

@project_bp.route('/<int:project_id>/bids', methods=['GET'])
@jwt_required()
def get_project_bids(project_id):
    """Get all bids for a project."""
    current_user_id = get_jwt_identity()
    
    try:
        project = Job.query.get_or_404(project_id)
        user = User.query.get(current_user_id)
        
        # Check if user is the project owner, an admin, or a bidder
        if project.customer_id != current_user_id and user.role != UserRole.ADMIN:
            # Check if user has a bid on this project
            user_bid = next((bid for bid in project.bids if bid.professional_id == current_user_id), None)
            if not user_bid:
                return jsonify({
                    'success': False,
                    'error': 'Unauthorized to view these bids.'
                }), 403
        
        # If user is the project owner or admin, return all bids
        # Otherwise, only return the user's bid
        if project.customer_id == current_user_id or user.role == UserRole.ADMIN:
            bids = [bid.to_dict(include_details=True) for bid in project.bids]
        else:
            user_bid = next((bid for bid in project.bids if bid.professional_id == current_user_id), None)
            bids = [user_bid.to_dict(include_details=True)] if user_bid else []
        
        return jsonify({
            'success': True,
            'bids': bids,
            'project': {
                'id': project.id,
                'title': project.title,
                'status': project.status.value if project.status else None,
                'customer_id': project.customer_id
            }
        })
        
    except Exception as e:
        current_app.logger.error(f'Get project bids error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve project bids. Please try again.'
        }), 500
