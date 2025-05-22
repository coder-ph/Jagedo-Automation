"""
Scheduled background tasks using Celery Beat.
"""
import logging
from datetime import datetime, timedelta
from celery.schedules import crontab
from ..extensions import db
from ..models import Session, Notification, EmailQueue, User
from ..utils.email import email_service

logger = logging.getLogger(__name__)

def init_scheduled_tasks(celery):
    """Initialize scheduled tasks with Celery."""
    # This function is called during Celery initialization to set up periodic tasks
    pass

def cleanup_expired_sessions():
    """Clean up expired user sessions from the database."""
    try:
        # Delete sessions that have expired
        expired = Session.query.filter(
            Session.expires_at < datetime.utcnow()
        ).delete(synchronize_session=False)
        
        db.session.commit()
        logger.info(f"Cleaned up {expired} expired sessions")
        return expired
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error cleaning up expired sessions: {str(e)}")
        raise

def send_scheduled_emails():
    """Send emails that are queued for sending."""
    try:
        # Get emails that are pending and scheduled to be sent now or earlier
        pending_emails = EmailQueue.query.filter(
            EmailQueue.status == 'pending',
            EmailQueue.scheduled_at <= datetime.utcnow()
        ).order_by(EmailQueue.priority.desc(), EmailQueue.created_at).limit(100).all()
        
        sent_count = 0
        failed_count = 0
        
        for email in pending_emails:
            try:
                # Mark as sending
                email.status = 'sending'
                email.sent_at = datetime.utcnow()
                db.session.commit()
                
                # Send the email
                success = email_service.send_email(
                    subject=email.subject,
                    recipients=email.recipient_email,
                    text_body=email.text_body,
                    html_body=email.html_body,
                    sender=email.sender_email,
                    sender_name=email.sender_name
                )
                
                if success:
                    email.status = 'sent'
                    email.sent_at = datetime.utcnow()
                    sent_count += 1
                else:
                    email.status = 'failed'
                    email.error = 'Failed to send email'
                    failed_count += 1
                
                db.session.commit()
                
            except Exception as e:
                db.session.rollback()
                logger.error(f"Error sending email {email.id}: {str(e)}")
                
                # Update email status
                try:
                    email.status = 'failed'
                    email.error = str(e)
                    db.session.commit()
                except:
                    db.session.rollback()
                
                failed_count += 1
        
        logger.info(f"Sent {sent_count} emails, failed: {failed_count}")
        return {
            'sent': sent_count,
            'failed': failed_count,
            'total': len(pending_emails)
        }
        
    except Exception as e:
        logger.error(f"Error in send_scheduled_emails: {str(e)}")
        raise

def notify_inactive_users():
    """Send notifications to inactive users."""
    try:
        # Find users who haven't logged in for a while
        days_inactive = 30  # Notify users inactive for 30+ days
        threshold_date = datetime.utcnow() - timedelta(days=days_inactive)
        
        inactive_users = User.query.filter(
            User.last_login < threshold_date,
            User.is_active == True,
            ~User.notifications.any(Notification.type == 'inactive_user')
        ).all()
        
        notified_count = 0
        
        for user in inactive_users:
            try:
                # Create notification
                notification = Notification(
                    user_id=user.id,
                    type='inactive_user',
                    title='We miss you!',
                    message='You haven\'t logged in for a while. Come back and check out what\'s new!',
                    action_url='/app',
                    is_read=False
                )
                
                db.session.add(notification)
                db.session.commit()
                notified_count += 1
                
                # Queue email
                email = EmailQueue(
                    subject="We miss you on Our Platform!",
                    recipient_email=user.email,
                    recipient_name=user.name or 'User',
                    template_name='user_inactive_reminder',
                    context={
                        'user': user.to_dict(),
                        'days_inactive': days_inactive
                    },
                    priority='low',
                    scheduled_at=datetime.utcnow()
                )
                
                db.session.add(email)
                db.session.commit()
                
            except Exception as e:
                db.session.rollback()
                logger.error(f"Error notifying inactive user {user.id}: {str(e)}")
        
        logger.info(f"Notified {notified_count} inactive users")
        return {
            'notified': notified_count,
            'total_inactive': len(inactive_users)
        }
        
    except Exception as e:
        logger.error(f"Error in notify_inactive_users: {str(e)}")
        raise

def cleanup_old_notifications():
    """Clean up old notifications from the database."""
    try:
        # Delete read notifications older than 90 days
        threshold_date = datetime.utcnow() - timedelta(days=90)
        
        deleted = Notification.query.filter(
            Notification.is_read == True,
            Notification.created_at < threshold_date
        ).delete(synchronize_session=False)
        
        db.session.commit()
        logger.info(f"Cleaned up {deleted} old notifications")
        return deleted
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error cleaning up old notifications: {str(e)}")
        raise

# Register tasks with Celery when this module is imported
from .celery import celery_app

@celery_app.task(name='app.tasks.scheduled.cleanup_expired_sessions')
def cleanup_expired_sessions_task():
    return cleanup_expired_sessions()

@celery_app.task(name='app.tasks.scheduled.send_scheduled_emails')
def send_scheduled_emails_task():
    return send_scheduled_emails()

@celery_app.task(name='app.tasks.scheduled.notify_inactive_users')
def notify_inactive_users_task():
    return notify_inactive_users()

@celery_app.task(name='app.tasks.scheduled.cleanup_old_notifications')
def cleanup_old_notifications_task():
    return cleanup_old_notifications()
