"""
Input validation utilities for the application.
"""
import re
from werkzeug.exceptions import BadRequest
from flask import jsonify

def validate_email(email):
    """
    Validate an email address format.
    
    Args:
        email (str): The email address to validate.
        
    Returns:
        bool: True if the email is valid, False otherwise.
    """
    if not email:
        return False
    
    # Basic email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_password(password):
    """
    Validate a password meets complexity requirements.
    
    Requirements:
    - At least 8 characters long
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character
    
    Args:
        password (str): The password to validate.
        
    Returns:
        bool: True if the password is valid, False otherwise.
    """
    if not password or len(password) < 8:
        return False
    
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)
    
    return has_upper and has_lower and has_digit and has_special

def validate_phone(phone):
    """
    Validate a phone number format.
    
    Args:
        phone (str): The phone number to validate.
        
    Returns:
        bool: True if the phone number is valid, False otherwise.
    """
    if not phone:
        return False
    
    # Basic phone number pattern (supports international format with +)
    pattern = r'^\+?[0-9\s-]{10,}$'
    return bool(re.match(pattern, phone))

def validate_name(name):
    """
    Validate a person's name.
    
    Args:
        name (str): The name to validate.
        
    Returns:
        bool: True if the name is valid, False otherwise.
    """
    if not name or len(name.strip()) < 2:
        return False
    
    # Allow letters, spaces, hyphens, and apostrophes
    pattern = r'^[a-zA-Z\s\-\']+$'
    return bool(re.match(pattern, name))

def validate_json_content_type(request):
    """
    Validate that the request has JSON content type.
    
    Args:
        request: The Flask request object.
        
    Raises:
        BadRequest: If the content type is not application/json.
    """
    if not request.is_json:
        raise BadRequest('Content-Type must be application/json')

def handle_validation_error(error):
    """
    Handle validation errors and return a JSON response.
    
    Args:
        error: The validation error.
        
    Returns:
        Response: A JSON response with the error message.
    """
    response = jsonify({
        'status': 'error',
        'message': str(error),
        'error': 'validation_error'
    })
    response.status_code = 400
    return response
