from flask import Flask, jsonify, send_from_directory, current_app, render_template
import os
from datetime import timedelta

# Import extensions
from .extensions import db, jwt, migrate, cache, cors
from .services.cloudinary_storage import cloudinary_storage

# Import CLI commands
from commands import init_app as init_commands

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
    from .routes.places import places_bp
    from .routes.simple_places import simple_places_bp
    from .routes.admin import bp as admin_bp
    from .services.payment_service import mpesa_service
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(project_bp, url_prefix='/api/projects')
    app.register_blueprint(bid_bp, url_prefix='/api/bids')
    app.register_blueprint(document_bp, url_prefix='/api/documents')
    app.register_blueprint(notification_bp, url_prefix='/api/notifications')
    app.register_blueprint(payment_bp, url_prefix='/api/payments')
    app.register_blueprint(admin_bp)  
    app.register_blueprint(places_bp) 
    app.register_blueprint(simple_places_bp)  
    
    # Initialize CLI commands
    init_commands(app)
    
    # Route to serve the example HTML file
    @app.route('/examples/places')
    def serve_places_example():
        # Render the template with the API key
        return send_from_directory('../examples', 'simple_places.html')
        
    # Route to serve the places example with template rendering
    @app.route('/examples/places-demo')
    def serve_places_demo():
        return render_template('places_demo.html', 
                           GOOGLE_PLACES_API_KEY=current_app.config.get('GOOGLE_PLACES_API_KEY', ''))
    
    # Initialize payment service
    mpesa_service.init_app(app)
    
    # Initialize Cloudinary storage if configured
    if app.config.get('STORAGE_PROVIDER') == 'cloudinary':
        cloudinary_storage.init_app(app)
        app.logger.info('Cloudinary storage initialized')
    else:
        # Ensure upload directory exists for local storage
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        app.logger.info(f'Local storage initialized at {app.config["UPLOAD_FOLDER"]}')
    
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