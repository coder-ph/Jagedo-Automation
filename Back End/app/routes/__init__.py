from flask import Blueprint

# Import all route blueprints
from .auth import auth_bp
from .project import project_bp
from .bid import bid_bp
from .document import document_bp
from .notification import notification_bp
from .payment import bp as payment_bp

# You can also initialize any route-specific extensions or utilities here

def init_app(app):
    """Register blueprints with the Flask application."""
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(project_bp, url_prefix='/api/projects')
    app.register_blueprint(bid_bp, url_prefix='/api/bids')
    app.register_blueprint(document_bp, url_prefix='/api/documents')
    app.register_blueprint(notification_bp, url_prefix='/api/notifications')
    app.register_blueprint(payment_bp, url_prefix='/api/payments')
    
    return app