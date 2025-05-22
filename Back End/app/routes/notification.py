from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from ..models import db, Notification, User, UserRole
from ..utils.decorators import role_required

# Create notification blueprint
notification_bp = Blueprint('notification', __name__)

@notification_bp.route('', methods=['GET'])
@jwt_required()
def get_notifications():
    """Get all notifications for the current user."""
    current_user_id = get_jwt_identity()
    
    try:
        # Get query parameters
        unread_only = request.args.get('unread_only', 'false').lower() == 'true'
        limit = int(request.args.get('limit', 20))
        offset = int(request.args.get('offset', 0))
        
        # Base query
        query = Notification.query.filter_by(user_id=current_user_id)
        
        # Filter by read status if needed
        if unread_only:
            query = query.filter_by(read=False)
        
        # Order by creation date (newest first)
        query = query.order_by(Notification.created_at.desc())
        
        # Apply pagination
        notifications = query.offset(offset).limit(limit).all()
        
        # Mark notifications as read if requested
        mark_read = request.args.get('mark_read', 'false').lower() == 'true'
        if mark_read and notifications:
            notification_ids = [n.id for n in notifications if not n.read]
            if notification_ids:
                Notification.query.filter(Notification.id.in_(notification_ids)).update(
                    {'read': True, 'read_at': datetime.utcnow()},
                    synchronize_session=False
                )
                db.session.commit()
        
        return jsonify({
            'success': True,
            'notifications': [n.to_dict() for n in notifications],
            'total': query.count(),
            'unread_count': Notification.query.filter_by(user_id=current_user_id, read=False).count()
        })
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Get notifications error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve notifications. Please try again.'
        }), 500

@notification_bp.route('/<int:notification_id>', methods=['GET'])
@jwt_required()
def get_notification(notification_id):
    """Get a specific notification by ID."""
    current_user_id = get_jwt_identity()
    
    try:
        notification = Notification.query.filter_by(
            id=notification_id,
            user_id=current_user_id
        ).first_or_404()
        
        # Mark as read if unread
        if not notification.read:
            notification.read = True
            notification.read_at = datetime.utcnow()
            db.session.commit()
        
        return jsonify({
            'success': True,
            'notification': notification.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Get notification error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve notification. Please try again.'
        }), 500

@notification_bp.route('/<int:notification_id>/read', methods=['POST'])
@jwt_required()
def mark_notification_read(notification_id):
    """Mark a notification as read."""
    current_user_id = get_jwt_identity()
    
    try:
        notification = Notification.query.filter_by(
            id=notification_id,
            user_id=current_user_id
        ).first()
        
        if not notification:
            return jsonify({
                'success': False,
                'error': 'Notification not found.'
            }), 404
            
        if not notification.read:
            notification.read = True
            notification.read_at = datetime.utcnow()
            db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Notification marked as read',
            'notification': notification.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Mark notification read error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to update notification. Please try again.'
        }), 500

@notification_bp.route('/read-all', methods=['POST'])
@jwt_required()
def mark_all_notifications_read():
    """Mark all notifications as read for the current user."""
    current_user_id = get_jwt_identity()
    
    try:
        # Update all unread notifications for the user
        updated = Notification.query.filter_by(
            user_id=current_user_id,
            read=False
        ).update({
            'read': True,
            'read_at': datetime.utcnow()
        })
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Marked {updated} notifications as read',
            'count': updated
        })
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Mark all notifications read error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to update notifications. Please try again.'
        }), 500

@notification_bp.route('/<int:notification_id>', methods=['DELETE'])
@jwt_required()
def delete_notification(notification_id):
    """Delete a notification."""
    current_user_id = get_jwt_identity()
    
    try:
        notification = Notification.query.filter_by(
            id=notification_id,
            user_id=current_user_id
        ).first()
        
        if not notification:
            return jsonify({
                'success': False,
                'error': 'Notification not found.'
            }), 404
            
        db.session.delete(notification)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Notification deleted successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Delete notification error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to delete notification. Please try again.'
        }), 500

@notification_bp.route('/unread-count', methods=['GET'])
@jwt_required()
def get_unread_count():
    """Get the count of unread notifications for the current user."""
    current_user_id = get_jwt_identity()
    
    try:
        count = Notification.query.filter_by(
            user_id=current_user_id,
            read=False
        ).count()
        
        return jsonify({
            'success': True,
            'count': count
        })
        
    except Exception as e:
        current_app.logger.error(f'Get unread count error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to get unread count. Please try again.'
        }), 500
