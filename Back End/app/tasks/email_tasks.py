"""
Background tasks for sending emails asynchronously.
"""
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List, Union

from flask import current_app
from ..extensions import db
from ..models import EmailQueue, Notification, User, Bid, Job
from ..utils.email import email_service
from .celery import celery_app

logger = logging.getLogger(__name__)

class EmailError(Exception):
    """Base exception for email task errors."""
    pass

def queue_email(
    subject: str,
    recipient_email: str,
    template_name: str = None,
    context: Dict[str, Any] = None,
    text_body: str = None,
    html_body: str = None,
    sender_email: str = None,
    sender_name: str = None,
    recipient_name: str = None,
    priority: str = 'normal',
    send_at: datetime = None,
    notification_user_id: int = None,
    notification_title: str = None,
    notification_message: str = None,
    notification_data: Dict[str, Any] = None
) -> EmailQueue:
    """
    Queue an email to be sent asynchronously.
    
    Args:
        subject: Email subject
        recipient_email: Recipient email address
        template_name: Name of the email template (without extension)
        context: Context variables for the template
        text_body: Plain text email body (alternative to template)
        html_body: HTML email body (alternative to template)
        sender_email: Sender email address
        sender_name: Sender name
        recipient_name: Recipient name
        priority: Email priority ('high', 'normal', 'low')
        send_at: When to send the email (default: now)
        notification_user_id: User ID for creating a notification
        notification_title: Notification title
        notification_message: Notification message
        notification_data: Additional notification data
        
    Returns:
        EmailQueue: The queued email record
    """
    email = EmailQueue(
        subject=subject,
        recipient_email=recipient_email,
        recipient_name=recipient_name,
        template_name=template_name,
        context=context or {},
        text_body=text_body,
        html_body=html_body,
        sender_email=sender_email,
        sender_name=sender_name,
        priority=priority,
        scheduled_at=send_at or datetime.utcnow(),
        status='pending',
        notification_user_id=notification_user_id,
        notification_title=notification_title,
        notification_message=notification_message,
        notification_data=notification_data or {}
    )
    
    try:
        db.session.add(email)
        db.session.commit()
        
        # Trigger the send email task if not scheduled for future
        if not send_at or send_at <= datetime.utcnow():
            send_queued_email.delay(email.id)
            
        return email
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Failed to queue email: {str(e)}")
        raise EmailError(f"Failed to queue email: {str(e)}")

@celery_app.task(bind=True, max_retries=3, default_retry_delay=300)
def send_queued_email(self, email_id: int) -> bool:
    """
    Send a queued email.
    
    Args:
        email_id: ID of the email to send
        
    Returns:
        bool: True if sent successfully, False otherwise
    """
    try:
        email = EmailQueue.query.get(email_id)
        if not email:
            logger.error(f"Email with ID {email_id} not found")
            return False
            
        if email.status == 'sent':
            logger.info(f"Email {email_id} already sent")
            return True
            
        # Mark as sending
        email.status = 'sending'
        email.attempts += 1
        email.last_attempt_at = datetime.utcnow()
        db.session.commit()
        
        # Send the email
        success = email_service.send_email(
            subject=email.subject,
            recipients=[email.recipient_email],
            text_body=email.text_body,
            html_body=email.html_body,
            sender=email.sender_email,
            sender_name=email.sender_name
        )
        
        if success:
            email.status = 'sent'
            email.sent_at = datetime.utcnow()
            
            # Create notification if requested
            if email.notification_user_id:
                try:
                    notification = Notification(
                        user_id=email.notification_user_id,
                        title=email.notification_title or email.subject,
                        message=email.notification_message or f"Email sent to {email.recipient_email}",
                        data={
                            'email_id': email.id,
                            'recipient': email.recipient_email,
                            **email.notification_data
                        }
                    )
                    db.session.add(notification)
                except Exception as e:
                    logger.error(f"Failed to create notification for email {email.id}: {str(e)}")
            
            db.session.commit()
            logger.info(f"Email {email.id} sent successfully to {email.recipient_email}")
            return True
        else:
            raise Exception("Email service returned failure")
            
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error sending email {email_id}: {str(e)}")
        
        # Update email status
        try:
            if email:
                email.status = 'failed'
                email.error = str(e)
                email.last_error = str(e)
                email.last_attempt_at = datetime.utcnow()
                db.session.commit()
        except:
            db.session.rollback()
        
        # Retry with exponential backoff
        try:
            raise self.retry(exc=e, countdown=60 * (2 ** (self.request.retries - 1)))
        except self.MaxRetriesExceededError:
            logger.error(f"Max retries exceeded for email {email_id}")
            return False

@celery_app.task
def send_welcome_email(user_id: int) -> bool:
    """
    Send a welcome email to a new user.
    
    Args:
        user_id: ID of the user to welcome
        
    Returns:
        bool: True if email was queued successfully
    """
    try:
        user = User.query.get(user_id)
        if not user:
            logger.error(f"User {user_id} not found")
            return False
            
        return bool(queue_email(
            subject=f"Welcome to Our Platform, {user.name or 'there'}!",
            recipient_email=user.email,
            template_name='welcome_email',
            context={
                'user': user.to_dict(),
                'login_url': '/login',
                'support_email': 'support@example.com'
            },
            notification_user_id=user.id,
            notification_title='Welcome to Our Platform!',
            notification_message='Check your email for a welcome message.'
        ))
        
    except Exception as e:
        logger.error(f"Error in send_welcome_email: {str(e)}")
        return False

@celery_app.task
def send_password_reset_email(user_id: int, reset_token: str) -> bool:
    """
    Send a password reset email.
    
    Args:
        user_id: ID of the user
        reset_token: Password reset token
        
    Returns:
        bool: True if email was queued successfully
    """
    try:
        user = User.query.get(user_id)
        if not user:
            logger.error(f"User {user_id} not found")
            return False
            
        reset_url = f"{current_app.config.get('FRONTEND_URL', '')}/reset-password?token={reset_token}"
        
        return bool(queue_email(
            subject="Password Reset Request",
            recipient_email=user.email,
            template_name='password_reset',
            context={
                'user': user.to_dict(),
                'reset_url': reset_url,
                'expiry_hours': current_app.config.get('RESET_PASSWORD_EXPIRATION', 24)
            },
            priority='high'
        ))
        
    except Exception as e:
        logger.error(f"Error in send_password_reset_email: {str(e)}")
        return False

@celery_app.task
def send_bid_notification(bid_id: int, notification_type: str) -> bool:
    """
    Send a bid-related notification email.
    
    Args:
        bid_id: ID of the bid
        notification_type: Type of notification ('received', 'accepted', 'rejected', 'new_message')
        
    Returns:
        bool: True if notification was queued successfully
    """
    try:
        bid = Bid.query.get(bid_id)
        if not bid:
            logger.error(f"Bid {bid_id} not found")
            return False
            
        job = Job.query.get(bid.job_id)
        if not job:
            logger.error(f"Job {bid.job_id} not found for bid {bid_id}")
            return False
            
        professional = User.query.get(bid.professional_id)
        if not professional:
            logger.error(f"Professional {bid.professional_id} not found for bid {bid_id}")
            return False
            
        customer = User.query.get(job.customer_id)
        if not customer:
            logger.error(f"Customer {job.customer_id} not found for job {job.id}")
            return False
            
        # Determine notification details based on type
        if notification_type == 'received':
            # Notify customer about new bid
            subject = f"New Bid Received for {job.title}"
            template = 'bid_received'
            recipient = customer
            context = {
                'job': job.to_dict(),
                'bid': bid.to_dict(),
                'professional': professional.to_dict(),
                'bid_url': f"/jobs/{job.id}/bids/{bid.id}"
            }
            notification_title = "New Bid Received"
            notification_message = f"You've received a new bid from {professional.name} for '{job.title}'"
            
        elif notification_type == 'accepted':
            # Notify professional their bid was accepted
            subject = f"Your Bid Was Accepted - {job.title}"
            template = 'bid_accepted'
            recipient = professional
            context = {
                'job': job.to_dict(),
                'bid': bid.to_dict(),
                'customer': customer.to_dict(),
                'job_url': f"/jobs/{job.id}"
            }
            notification_title = "Bid Accepted!"
            notification_message = f"Your bid for '{job.title}' was accepted!"
            
        elif notification_type == 'rejected':
            # Notify professional their bid was rejected
            subject = f"Update on Your Bid for {job.title}"
            template = 'bid_rejected'
            recipient = professional
            context = {
                'job': job.to_dict(),
                'bid': bid.to_dict(),
                'customer': customer.to_dict(),
                'browse_jobs_url': "/jobs"
            }
            notification_title = "Bid Not Selected"
            notification_message = f"Your bid for '{job.title}' was not selected"
            
        elif notification_type == 'new_message':
            # Notify about new message on bid
            subject = f"New Message About Your Bid for {job.title}"
            template = 'bid_new_message'
            recipient = professional if bid.last_message_sender_id != professional.id else customer
            context = {
                'job': job.to_dict(),
                'bid': bid.to_dict(),
                'other_user': customer if bid.last_message_sender_id != professional.id else professional,
                'message_url': f"/messages/bid/{bid.id}"
            }
            notification_title = "New Message About Your Bid"
            notification_message = f"You have a new message about your bid for '{job.title}'"
            
        else:
            logger.error(f"Unknown notification type: {notification_type}")
            return False
        
        # Queue the email
        return bool(queue_email(
            subject=subject,
            recipient_email=recipient.email,
            template_name=template,
            context=context,
            notification_user_id=recipient.id,
            notification_title=notification_title,
            notification_message=notification_message,
            notification_data={
                'type': 'bid_notification',
                'bid_id': bid.id,
                'job_id': job.id,
                'notification_type': notification_type
            }
        ))
        
    except Exception as e:
        logger.error(f"Error in send_bid_notification: {str(e)}")
        return False
