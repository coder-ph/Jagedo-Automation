import os
import uuid
import re
from werkzeug.utils import secure_filename
from flask import current_app
from datetime import datetime
import json
from functools import wraps

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def save_uploaded_file(file, subfolder='uploads', prefix=''):
    """
    Save an uploaded file to the upload folder.
    
    Args:
        file: The file object to save
        subfolder: The subfolder within the uploads directory
        prefix: Optional prefix for the filename
        
    Returns:
        str: The relative path to the saved file, or None if saving failed
    """
    try:
        if file and file.filename:
            # Create a secure filename
            filename = secure_filename(file.filename)
            
            # Generate a unique filename to prevent collisions
            unique_id = str(uuid.uuid4().hex)[:8]
            filename = f"{prefix}_{unique_id}_{filename}" if prefix else f"{unique_id}_{filename}"
            
            # Create the upload directory if it doesn't exist
            upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], subfolder)
            os.makedirs(upload_dir, exist_ok=True)
            
            # Save the file
            filepath = os.path.join(upload_dir, filename)
            file.save(filepath)
            
            # Return the relative path
            return os.path.join(subfolder, filename)
        return None
    except Exception as e:
        current_app.logger.error(f'Error saving file: {str(e)}')
        return None

def validate_email(email):
    """
    Validate an email address.
    
    Args:
        email (str): The email address to validate
        
    Returns:
        bool: True if the email is valid, False otherwise
    """
    if not email:
        return False
    
    # Simple email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """
    Validate a password against complexity requirements.
    
    Args:
        password (str): The password to validate
        
    Returns:
        dict: A dictionary with 'valid' (bool) and 'requirements' (list of unmet requirements)
    """
    if not password:
        return {
            'valid': False,
            'requirements': ['Password is required.']
        }
    
    requirements = []
    
    # Check minimum length
    if len(password) < 8:
        requirements.append('Password must be at least 8 characters long.')
    
    # Check for at least one digit
    if not re.search(r'\d', password):
        requirements.append('Password must contain at least one number.')
    
    # Check for at least one uppercase letter
    if not re.search(r'[A-Z]', password):
        requirements.append('Password must contain at least one uppercase letter.')
    
    # Check for at least one lowercase letter
    if not re.search(r'[a-z]', password):
        requirements.append('Password must contain at least one lowercase letter.')
    
    # Check for at least one special character
    if not re.search(r'[^A-Za-z0-9]', password):
        requirements.append('Password must contain at least one special character.')
    
    return {
        'valid': len(requirements) == 0,
        'requirements': requirements
    }

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, datetime.date)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def to_json(data):
    """Convert object to JSON string"""
    return json.dumps(data, default=json_serial)

def from_json(json_str):
    """Convert JSON string to Python object"""
    return json.loads(json_str)

def format_currency(amount, currency='USD'):
    """Format a number as currency"""
    try:
        amount = float(amount)
        return f"{currency} {amount:,.2f}"
    except (ValueError, TypeError):
        return f"{currency} 0.00"

def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth specified in decimal degrees.
    
    Returns distance in kilometers.
    """
    from math import radians, cos, sin, asin, sqrt
    
    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    
    # Radius of earth in kilometers
    r = 6371
    return c * r

def parse_bool(value):
    """Convert a string representation of a boolean to a boolean value"""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ('true', '1', 't', 'y', 'yes')
    return bool(value)

def get_pagination_params(request):
    """Extract pagination parameters from request"""
    try:
        page = int(request.args.get('page', 1))
        per_page = min(int(request.args.get('per_page', 10)), 100)  # Max 100 items per page
        return max(1, page), max(1, min(per_page, 100))
    except (ValueError, TypeError):
        return 1, 10  # Default values

def generate_slug(text):
    """Generate a URL-friendly slug from a string"""
    if not text:
        return ''
    
    # Convert to lowercase and replace spaces with hyphens
    slug = text.lower().replace(' ', '-')
    
    # Remove all non-word characters (keeps letters, numbers, and hyphens)
    slug = re.sub(r'[^\w\-]', '', slug)
    
    # Replace multiple hyphens with a single one
    slug = re.sub(r'\-+', '-', slug)
    
    # Remove leading/trailing hyphens
    return slug.strip('-')

def truncate(text, length=100, suffix='...'):
    """Truncate text to a specified length, adding a suffix if truncated"""
    if not text:
        return ''
    
    if len(text) <= length:
        return text
    
    return text[:length-len(suffix)] + suffix

def generate_reference(prefix='PAY'):
    """
    Generate a unique reference number for payments.
    
    Format: PREFIX-YYMMDD-XXXXXX where X is a random string
    
    Args:
        prefix (str): A prefix for the reference (e.g., PAY, INV, etc.)
        
    Returns:
        str: A unique reference string
    """
    import random
    import string
    
    # Get current date in YYMMDD format
    date_str = datetime.utcnow().strftime('%y%m%d')
    
    # Generate a random 6-character string
    random_str = ''.join(random.choices(
        string.ascii_uppercase + string.digits, k=6
    ))
    
    return f"{prefix}-{date_str}-{random_str}"
