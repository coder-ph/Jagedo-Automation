from flask import Blueprint, request, jsonify
from models import db, Bid, BidTeamMember, User, Job, Notification
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
import json

bp = Blueprint('bid_routes', __name__)

@bp.route('/api/bids/<int:bid_id>/team-members', methods=['POST'])
@jwt_required()
def add_team_member(bid_id):
    """
    Add a team member to a bid
    """
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['email', 'name', 'role', 'hourly_rate', 'hours']
    missing = [field for field in required_fields if field not in data]
    if missing:
        return jsonify({
            'success': False,
            'message': f'Missing required fields: {", ".join(missing)}'
        }), 400
    
    try:
        # Get the bid and verify ownership
        bid = Bid.query.get_or_404(bid_id)
        if bid.professional_id != current_user_id:
            return jsonify({
                'success': False,
                'message': 'Unauthorized: You can only add team members to your own bids'
            }), 403
        
        # Calculate total cost
        total_cost = float(data['hourly_rate']) * float(data['hours'])
        
        # Create the team member
        team_member = BidTeamMember(
            bid_id=bid_id,
            email=data['email'].lower().strip(),
            name=data['name'],
            role=data['role'],
            hourly_rate=data['hourly_rate'],
            hours=data['hours'],
            total_cost=total_cost
        )
        
        db.session.add(team_member)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Team member added successfully',
            'data': team_member.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error adding team member: {str(e)}'
        }), 500

@bp.route('/api/bids/<int:bid_id>/team-members', methods=['GET'])
@jwt_required()
def get_team_members(bid_id):
    """
    Get all team members for a bid
    """
    current_user_id = get_jwt_identity()
    
    try:
        # Get the bid and verify access
        bid = Bid.query.get_or_404(bid_id)
        if bid.professional_id != current_user_id and bid.job.customer_id != current_user_id:
            return jsonify({
                'success': False,
                'message': 'Unauthorized: You can only view team members for your own bids or projects'
            }), 403
        
        team_members = BidTeamMember.query.filter_by(bid_id=bid_id).all()
        
        return jsonify({
            'success': True,
            'data': [member.to_dict() for member in team_members]
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error retrieving team members: {str(e)}'
        }), 500

@bp.route('/api/bids/team-members/lookup', methods=['GET'])
@jwt_required()
def lookup_professional():
    """
    Look up a professional by email to auto-populate their details
    """
    email = request.args.get('email')
    if not email:
        return jsonify({
            'success': False,
            'message': 'Email parameter is required'
        }), 400
    
    try:
        # Look up the user by email
        user = User.query.filter(
            db.func.lower(User.email) == email.lower().strip(),
            User.role == 'professional'
        ).first()
        
        if not user:
            return jsonify({
                'success': True,
                'found': False,
                'message': 'No professional found with this email'
            })
        
        # Get the user's primary role/skill
        primary_skill = None
        if user.skills:
            primary_skill = user.skills[0].skill.name if user.skills[0].skill else None
        
        return jsonify({
            'success': True,
            'found': True,
            'data': {
                'email': user.email,
                'name': user.name,
                'role': primary_skill or 'Professional',
                'hourly_rate': user.hourly_rate if hasattr(user, 'hourly_rate') else None,
                'phone': user.phone if hasattr(user, 'phone') else None,
                'nca_level': user.nca_level,
                'average_rating': user.average_rating
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error looking up professional: {str(e)}'
        }), 500
