from flask import Flask, jsonify
import os
from datetime import timedelta

# Import extensions
from .extensions import db, jwt, migrate, cache, cors

def create_app(config_name=None):
    app = Flask(__name__)
    
    # Load configuration
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    if config_name == 'production':
        app.config.from_object('config.ProductionConfig')
    elif config_name == 'testing':
        app.config.from_object('config.TestingConfig')
    else:
        app.config.from_object('config.DevelopmentConfig')
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)
    cors.init_app(app)
    
    # Import and register blueprints
    from .routes import auth_bp, project_bp, bid_bp, document_bp, notification_bp, payment_bp
    from .services.payment_service import mpesa_service
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(project_bp, url_prefix='/api/projects')
    app.register_blueprint(bid_bp, url_prefix='/api/bids')
    app.register_blueprint(document_bp, url_prefix='/api/documents')
    app.register_blueprint(notification_bp, url_prefix='/api/notifications')
    app.register_blueprint(payment_bp, url_prefix='/api/payments')
    
    # Initialize payment service
    mpesa_service.init_app(app)
    
    # Register error handlers
    from .utils.error_handlers import register_error_handlers
    register_error_handlers(app)
    
    # Shell context
    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'User': User,
            'Job': Job,
            'Bid': Bid,
            'Message': Message,
            'Notification': Notification
        }
        
    return app
    
    return app