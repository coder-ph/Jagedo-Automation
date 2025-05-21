from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime

from ..models import db, Bid, Job, User, BidTeamMember, Notification, JobStatus, UserRole, ProjectStatusHistory
from ..utils.decorators import role_required
from ..utils.helpers import allowed_file, save_uploaded_file

# Create bid blueprint
bid_bp = Blueprint('bid', __name__)

@bid_bp.route('', methods=['POST'])
@jwt_required()
@role_required([UserRole.PROFESSIONAL, UserRole.ADMIN])
def submit_bid():
    """Submit a bid for a project."""
    current_user_id = get_jwt_identity()
    data = request.form
    
    # Validate required fields
    required_fields = ['job_id', 'amount', 'proposal', 'timeline_weeks']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({
                'success': False,
                'error': f'{field.replace("_", " ").title()} is required.'
            }), 400
    
    try:
        # Get and validate job
        job = db.session.get(Job, int(data['job_id']))
        if not job:
            return jsonify({
                'success': False,
                'error': 'Project not found.'
            }), 404
            
        # Check if project is open for bidding
        if job.status != JobStatus.OPEN:
            return jsonify({
                'success': False,
                'error': 'This project is no longer accepting bids.'
            }), 400
            
        # Check if user has already submitted a bid
        existing_bid = Bid.query.filter_by(
            job_id=job.id,
            professional_id=current_user_id
        ).first()
        
        if existing_bid:
            return jsonify({
                'success': False,
                'error': 'You have already submitted a bid for this project.'
            }), 400
            
        # Validate amount
        try:
            amount = float(data['amount'])
            if amount <= 0:
                return jsonify({
                    'success': False,
                    'error': 'Bid amount must be greater than 0.'
                }), 400
        except ValueError:
            return jsonify({
                'success': False,
                'error': 'Invalid bid amount.'
            }), 400
            
        # Validate timeline_weeks
        try:
            timeline_weeks = int(data['timeline_weeks'])
            if timeline_weeks <= 0:
                return jsonify({
                    'success': False,
                    'error': 'Timeline must be greater than 0 weeks.'
                }), 400
        except ValueError:
            return jsonify({
                'success': False,
                'error': 'Invalid timeline value.'
            }), 400
            
        # Create new bid
        bid = Bid(
            job_id=job.id,
            professional_id=current_user_id,
            amount=amount,
            proposal=data['proposal'],
            timeline_weeks=timeline_weeks,
            status='pending'
        )
        
        db.session.add(bid)
        db.session.flush()  # Get the bid ID for team members and attachments
        
        # Handle team members if provided
        if 'team_members' in data:
            try:
                team_members = eval(data['team_members'])  # Convert string to list of dicts
                if isinstance(team_members, list):
                    for member in team_members:
                        team_member = BidTeamMember(
                            bid_id=bid.id,
                            email=member.get('email'),
                            name=member.get('name'),
                            role=member.get('role'),
                            hourly_rate=float(member.get('hourly_rate', 0)),
                            hours=float(member.get('hours', 0)),
                            total_cost=float(member.get('total_cost', 0))
                        )
                        db.session.add(team_member)
            except Exception as e:
                db.session.rollback()
                current_app.logger.error(f'Error processing team members: {str(e)}')
                return jsonify({
                    'success': False,
                    'error': 'Invalid team members data.'
                }), 400
        
        # Handle file uploads if any
        if 'attachments' in request.files:
            files = request.files.getlist('attachments')
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_url = save_uploaded_file(file, 'bid_attachments', f'bid_{bid.id}')
                    
                    if file_url:
                        attachment = Attachment(
                            file_url=file_url,
                            filename=filename,
                            uploaded_by=current_user_id,
                            bid_id=bid.id,
                            user_id=current_user_id
                        )
                        db.session.add(attachment)
        
        # Create notification for project owner
        notification = Notification(
            user_id=job.customer_id,
            title='New Bid Received',
            message=f'You have received a new bid for your project: {job.title}',
            notification_type='bid_received',
            content=json.dumps({
                'project_id': job.id,
                'project_title': job.title,
                'bid_id': bid.id,
                'bid_amount': float(amount)
            })
        )
        db.session.add(notification)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Bid submitted successfully',
            'bid': bid.to_dict(include_details=True)
        }), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Bid submission error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to submit bid. Please try again.'
        }), 500

@bid_bp.route('/<int:bid_id>', methods=['GET'])
@jwt_required()
def get_bid(bid_id):
    """Get bid details by ID."""
    current_user_id = get_jwt_identity()
    
    try:
        bid = Bid.query.get_or_404(bid_id)
        
        # Check if user is authorized to view this bid
        if (bid.professional_id != current_user_id and 
            bid.job.customer_id != current_user_id and
            User.query.get(current_user_id).role != UserRole.ADMIN):
            return jsonify({
                'success': False,
                'error': 'Unauthorized to view this bid.'
            }), 403
            
        return jsonify({
            'success': True,
            'bid': bid.to_dict(include_details=True)
        })
        
    except Exception as e:
        current_app.logger.error(f'Get bid error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve bid. Please try again.'
        }), 500

@bid_bp.route('/<int:bid_id>', methods=['PUT'])
@jwt_required()
def update_bid(bid_id):
    """Update bid details."""
    current_user_id = get_jwt_identity()
    data = request.form
    
    try:
        bid = Bid.query.get_or_404(bid_id)
        
        # Check if user is the bid owner
        if bid.professional_id != current_user_id:
            return jsonify({
                'success': False,
                'error': 'Unauthorized to update this bid.'
            }), 403
            
        # Check if bid can be updated
        if bid.status != 'pending':
            return jsonify({
                'success': False,
                'error': 'Only pending bids can be updated.'
            }), 400
            
        # Update allowed fields
        if 'amount' in data:
            try:
                amount = float(data['amount'])
                if amount <= 0:
                    return jsonify({
                        'success': False,
                        'error': 'Bid amount must be greater than 0.'
                    }), 400
                bid.amount = amount
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': 'Invalid bid amount.'
                }), 400
                
        if 'proposal' in data:
            bid.proposal = data['proposal']
            
        if 'timeline_weeks' in data:
            try:
                timeline_weeks = int(data['timeline_weeks'])
                if timeline_weeks <= 0:
                    return jsonify({
                        'success': False,
                        'error': 'Timeline must be greater than 0 weeks.'
                    }), 400
                bid.timeline_weeks = timeline_weeks
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': 'Invalid timeline value.'
                }), 400
        
        # Handle file uploads if any
        if 'attachments' in request.files:
            files = request.files.getlist('attachments')
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_url = save_uploaded_file(file, 'bid_attachments', f'bid_{bid.id}')
                    
                    if file_url:
                        attachment = Attachment(
                            file_url=file_url,
                            filename=filename,
                            uploaded_by=current_user_id,
                            bid_id=bid.id,
                            user_id=current_user_id
                        )
                        db.session.add(attachment)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Bid updated successfully',
            'bid': bid.to_dict(include_details=True)
        })
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Bid update error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to update bid. Please try again.'
        }), 500

@bid_bp.route('/<int:bid_id>', methods=['DELETE'])
@jwt_required()
def delete_bid(bid_id):
    """Delete a bid."""
    current_user_id = get_jwt_identity()
    
    try:
        bid = Bid.query.get_or_404(bid_id)
        
        # Check if user is the bid owner or an admin
        if bid.professional_id != current_user_id and User.query.get(current_user_id).role != UserRole.ADMIN:
            return jsonify({
                'success': False,
                'error': 'Unauthorized to delete this bid.'
            }), 403
            
        # Check if bid can be deleted
        if bid.status != 'pending':
            return jsonify({
                'success': False,
                'error': 'Only pending bids can be deleted.'
            }), 400
            
        # Delete the bid
        db.session.delete(bid)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Bid deleted successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Bid deletion error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to delete bid. Please try again.'
        }), 500

@bid_bp.route('/<int:bid_id>/accept', methods=['POST'])
@jwt_required()
def accept_bid(bid_id):
    """Accept a bid and award the project to the bidder."""
    current_user_id = get_jwt_identity()
    
    try:
        bid = Bid.query.get_or_404(bid_id)
        job = bid.job
        
        # Check if user is the project owner
        if job.customer_id != current_user_id:
            return jsonify({
                'success': False,
                'error': 'Only the project owner can accept bids.'
            }), 403
            
        # Check if project is still open
        if job.status != JobStatus.OPEN:
            return jsonify({
                'success': False,
                'error': 'This project is no longer open for bidding.'
            }), 400
            
        # Check if bid is pending
        if bid.status != 'pending':
            return jsonify({
                'success': False,
                'error': 'This bid is no longer pending.'
            }), 400
            
        # Start transaction
        with db.session.begin_nested():
            # Update bid status to accepted
            bid.status = 'accepted'
            
            # Update project status to awarded and assign contractor
            job.status = JobStatus.AWARDED
            job.assigned_contractor_id = bid.professional_id
            
            # Reject all other bids for this project
            Bid.query.filter(
                Bid.job_id == job.id,
                Bid.id != bid.id,
                Bid.status == 'pending'
            ).update({'status': 'rejected'})
            
            # Create notification for the winning bidder
            notification = Notification(
                user_id=bid.professional_id,
                title='Bid Accepted',
                message=f'Your bid for project "{job.title}" has been accepted!',
                notification_type='bid_accepted',
                content=json.dumps({
                    'project_id': job.id,
                    'project_title': job.title,
                    'bid_id': bid.id
                })
            )
            db.session.add(notification)
            
            # Create notifications for rejected bidders
            rejected_bids = Bid.query.filter(
                Bid.job_id == job.id,
                Bid.id != bid.id,
                Bid.status == 'rejected'
            ).all()
            
            for rejected_bid in rejected_bids:
                notification = Notification(
                    user_id=rejected_bid.professional_id,
                    title='Bid Not Selected',
                    message=f'Your bid for project "{job.title}" was not selected.',
                    notification_type='bid_rejected',
                    content=json.dumps({
                        'project_id': job.id,
                        'project_title': job.title,
                        'bid_id': rejected_bid.id
                    })
                )
                db.session.add(notification)
            
            # Record status change
            status_history = ProjectStatusHistory(
                project_id=job.id,
                from_status=job.status,
                to_status=JobStatus.AWARDED,
                changed_by=current_user_id,
                notes=f'Project awarded to {bid.professional.name}'
            )
            db.session.add(status_history)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Bid accepted successfully',
            'project': job.to_dict(),
            'bid': bid.to_dict(include_details=True)
        })
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Bid acceptance error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to accept bid. Please try again.'
        }), 500
