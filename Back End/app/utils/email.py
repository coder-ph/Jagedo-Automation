import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from flask import current_app, render_template_string
from jinja2 import Template
import logging
from typing import Optional, Dict, Any, List, Union

logger = logging.getLogger(__name__)

class EmailService:
    """Service for sending emails."""
    
    def __init__(self, app=None):
        """Initialize the email service."""
        self.app = None
        self.smtp_server = None
        self.smtp_port = None
        self.smtp_username = None
        self.smtp_password = None
        self.smtp_use_tls = True
        self.smtp_use_ssl = False
        self.default_sender = None
        self.default_sender_name = None
        
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize the email service with the Flask app."""
        self.app = app
        
        # Load configuration
        self.smtp_server = app.config.get('MAIL_SERVER', 'localhost')
        self.smtp_port = app.config.get('MAIL_PORT', 25)
        self.smtp_username = app.config.get('MAIL_USERNAME')
        self.smtp_password = app.config.get('MAIL_PASSWORD')
        self.smtp_use_tls = app.config.get('MAIL_USE_TLS', True)
        self.smtp_use_ssl = app.config.get('MAIL_USE_SSL', False)
        
        # Default sender
        self.default_sender = app.config.get('MAIL_DEFAULT_SENDER')
        self.default_sender_name = app.config.get('MAIL_DEFAULT_SENDER_NAME', app.name)
        
        # Add to app.extensions
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['email'] = self
    
    def create_message(
        self,
        subject: str,
        recipients: Union[str, List[str]],
        text_body: Optional[str] = None,
        html_body: Optional[str] = None,
        sender: Optional[str] = None,
        sender_name: Optional[str] = None,
        cc: Optional[Union[str, List[str]]] = None,
        bcc: Optional[Union[str, List[str]]] = None,
        reply_to: Optional[str] = None,
        attachments: Optional[List[Dict[str, Any]]] = None
    ) -> MIMEMultipart:
        """
        Create an email message.
        
        Args:
            subject: Email subject
            recipients: Email recipient(s)
            text_body: Plain text body
            html_body: HTML body
            sender: Sender email address
            sender_name: Sender name
            cc: CC recipient(s)
            bcc: BCC recipient(s)
            reply_to: Reply-To address
            attachments: List of attachments (dict with 'data', 'filename', and 'content_type')
            
        Returns:
            MIMEMultipart: The email message
        """
        if isinstance(recipients, str):
            recipients = [recipients]
            
        # Create message container
        msg = MIMEMultipart('alternative')
        
        # Set headers
        msg['Subject'] = subject
        msg['From'] = formataddr((sender_name or self.default_sender_name, 
                                sender or self.default_sender))
        msg['To'] = ', '.join(recipients)
        
        if cc:
            if isinstance(cc, str):
                cc = [cc]
            msg['Cc'] = ', '.join(cc)
            
        if bcc:
            if isinstance(bcc, str):
                bcc = [bcc]
            msg['Bcc'] = ', '.join(bcc)
            
        if reply_to:
            msg['Reply-To'] = reply_to
        
        # Attach text and HTML bodies
        if text_body:
            part1 = MIMEText(text_body, 'plain')
            msg.attach(part1)
            
        if html_body:
            part2 = MIMEText(html_body, 'html')
            msg.attach(part2)
        
        # Handle attachments
        if attachments:
            from email.mime.base import MIMEBase
            from email import encoders
            
            for attachment in attachments:
                part = MIMEBase(
                    'application', 
                    'octet-stream',
                    Name=attachment['filename']
                )
                part.set_payload(attachment['data'])
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename="{attachment["filename"]}"'
                )
                if 'content_type' in attachment:
                    part.set_type(attachment['content_type'])
                msg.attach(part)
        
        return msg
    
    def send_message(self, msg: MIMEMultipart) -> bool:
        """
        Send an email message.
        
        Args:
            msg: The email message to send
            
        Returns:
            bool: True if the message was sent successfully, False otherwise
        """
        if not self.smtp_server:
            logger.warning('No SMTP server configured. Email not sent.')
            return False
            
        try:
            # Create secure connection to server
            context = ssl.create_default_context()
            
            if self.smtp_use_ssl:
                server = smtplib.SMTP_SSL(
                    self.smtp_server, 
                    self.smtp_port,
                    context=context
                )
            else:
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                if self.smtp_use_tls:
                    server.starttls(context=context)
            
            # Login if credentials are provided
            if self.smtp_username and self.smtp_password:
                server.login(self.smtp_username, self.smtp_password)
            
            # Send email
            server.send_message(msg)
            server.quit()
            
            logger.info(f'Email sent to {msg["To"]}')
            return True
            
        except Exception as e:
            logger.error(f'Error sending email: {str(e)}')
            return False
    
    def send_email(
        self,
        subject: str,
        recipients: Union[str, List[str]],
        text_body: Optional[str] = None,
        html_body: Optional[str] = None,
        sender: Optional[str] = None,
        sender_name: Optional[str] = None,
        cc: Optional[Union[str, List[str]]] = None,
        bcc: Optional[Union[str, List[str]]] = None,
        reply_to: Optional[str] = None,
        attachments: Optional[List[Dict[str, Any]]] = None
    ) -> bool:
        """
        Send an email.
        
        Args:
            subject: Email subject
            recipients: Email recipient(s)
            text_body: Plain text body
            html_body: HTML body
            sender: Sender email address
            sender_name: Sender name
            cc: CC recipient(s)
            bcc: BCC recipient(s)
            reply_to: Reply-To address
            attachments: List of attachments (dict with 'data', 'filename', and 'content_type')
            
        Returns:
            bool: True if the email was sent successfully, False otherwise
        """
        msg = self.create_message(
            subject=subject,
            recipients=recipients,
            text_body=text_body,
            html_body=html_body,
            sender=sender,
            sender_name=sender_name,
            cc=cc,
            bcc=bcc,
            reply_to=reply_to,
            attachments=attachments
        )
        
        return self.send_message(msg)
    
    def send_template_email(
        self,
        template_name: str,
        subject: str,
        recipients: Union[str, List[str]],
        context: Optional[Dict[str, Any]] = None,
        sender: Optional[str] = None,
        sender_name: Optional[str] = None,
        cc: Optional[Union[str, List[str]]] = None,
        bcc: Optional[Union[str, List[str]]] = None,
        reply_to: Optional[str] = None,
        attachments: Optional[List[Dict[str, Any]]] = None
    ) -> bool:
        """
        Send an email using a template.
        
        Args:
            template_name: Name of the template file (without extension)
            subject: Email subject (can include template variables)
            recipients: Email recipient(s)
            context: Context variables for the template
            sender: Sender email address
            sender_name: Sender name
            cc: CC recipient(s)
            bcc: BCC recipient(s)
            reply_to: Reply-To address
            attachments: List of attachments (dict with 'data', 'filename', and 'content_type')
            
        Returns:
            bool: True if the email was sent successfully, False otherwise
        """
        if context is None:
            context = {}
            
        # Load templates
        try:
            # Try to load text template
            with open(f'app/templates/emails/{template_name}.txt') as f:
                text_template = Template(f.read())
            
            # Try to load HTML template
            with open(f'app/templates/emails/{template_name}.html') as f:
                html_template = Template(f.read())
                
            # Render templates
            text_body = text_template.render(**context)
            html_body = html_template.render(**context)
            
            # Render subject
            subject_template = Template(subject)
            rendered_subject = subject_template.render(**context)
            
            # Send email
            return self.send_email(
                subject=rendered_subject,
                recipients=recipients,
                text_body=text_body,
                html_body=html_body,
                sender=sender,
                sender_name=sender_name,
                cc=cc,
                bcc=bcc,
                reply_to=reply_to,
                attachments=attachments
            )
            
        except FileNotFoundError as e:
            logger.error(f'Email template not found: {template_name}')
            return False
        except Exception as e:
            logger.error(f'Error rendering email template: {str(e)}')
            return False

# Create a default instance
email_service = EmailService()

def init_email_service(app):
    """Initialize the email service with the Flask app."""
    email_service.init_app(app)
    return email_service
