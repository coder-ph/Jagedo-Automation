import os
from datetime import timedelta

class Config:
    
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-123'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-123'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    
    # File upload configuration
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {
        'images': {'jpg', 'jpeg', 'png', 'gif', 'webp'},
        'documents': {'pdf', 'doc', 'docx', 'txt', 'rtf'},
        'archives': {'zip', 'rar', '7z'},
        'spreadsheets': {'xls', 'xlsx', 'csv'},
        'presentations': {'ppt', 'pptx'},
        'code': {'py', 'js', 'html', 'css', 'json', 'xml'},
    }
    
    # Cache configuration
    CACHE_TYPE = 'SimpleCache'  
    CACHE_DEFAULT_TIMEOUT = 300
    
    # Redis configuration
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    JWT_BLOCKLIST_ENABLED = True  # Enable Redis-based JWT blacklist when Redis is available
    
    # Celery configuration
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
    
    # Google OAuth and Places API configuration
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
    GOOGLE_PROJECT_ID = os.environ.get('GOOGLE_PROJECT_ID')
    GOOGLE_REDIRECT_URI = os.environ.get('GOOGLE_REDIRECT_URI')
    GOOGLE_AUTH_URI = os.environ.get('GOOGLE_AUTH_URI', 'https://accounts.google.com/o/oauth2/auth')
    GOOGLE_TOKEN_URI = os.environ.get('GOOGLE_TOKEN_URI', 'https://oauth2.googleapis.com/token')
    GOOGLE_USER_INFO_URI = os.environ.get('GOOGLE_USER_INFO_URI', 'https://www.googleapis.com/oauth2/v1/userinfo')
    GOOGLE_SCOPES = os.environ.get('GOOGLE_SCOPES', 'email profile https://www.googleapis.com/auth/places')
    
    # Google Places API
    GOOGLE_PLACES_API_KEY = os.environ.get('GOOGLE_PLACES_API_KEY')
    
    # Base URL for OAuth callbacks
    BASE_URL = os.environ.get('BASE_URL', 'http://localhost:5000')
    
    # Cloudinary Configuration
    CLOUDINARY_CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME')
    CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY')
    CLOUDINARY_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET')
    CLOUDINARY_URL = os.environ.get('CLOUDINARY_URL')
    
    # Storage configuration
    STORAGE_PROVIDER = os.environ.get('STORAGE_PROVIDER', 'local')  # 'local' or 'cloudinary'
    
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data-dev.sqlite')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data.sqlite')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
