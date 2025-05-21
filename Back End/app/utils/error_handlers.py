from flask import jsonify, request
from werkzeug.exceptions import HTTPException
import traceback
import logging

def register_error_handlers(app):
    """Register error handlers for the Flask application."""
    
    @app.errorhandler(400)
    def bad_request_error(error):
        """Handle 400 Bad Request errors."""
        app.logger.warning(f'Bad Request: {error.description}')
        return jsonify({
            'success': False,
            'error': error.description or 'Bad Request',
            'path': request.path
        }), 400
    
    @app.errorhandler(401)
    def unauthorized_error(error):
        """Handle 401 Unauthorized errors."""
        app.logger.warning(f'Unauthorized: {error.description}')
        return jsonify({
            'success': False,
            'error': error.description or 'Unauthorized',
            'path': request.path
        }), 401
    
    @app.errorhandler(403)
    def forbidden_error(error):
        """Handle 403 Forbidden errors."""
        app.logger.warning(f'Forbidden: {error.description}')
        return jsonify({
            'success': False,
            'error': error.description or 'Forbidden',
            'path': request.path
        }), 403
    
    @app.errorhandler(404)
    def not_found_error(error):
        """Handle 404 Not Found errors."""
        app.logger.warning(f'Not Found: {request.path}')
        return jsonify({
            'success': False,
            'error': 'The requested resource was not found.',
            'path': request.path
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed_error(error):
        """Handle 405 Method Not Allowed errors."""
        app.logger.warning(f'Method Not Allowed: {request.method} {request.path}')
        return jsonify({
            'success': False,
            'error': 'The method is not allowed for the requested URL.',
            'path': request.path,
            'method': request.method
        }), 405
    
    @app.errorhandler(409)
    def conflict_error(error):
        """Handle 409 Conflict errors."""
        app.logger.warning(f'Conflict: {error.description}')
        return jsonify({
            'success': False,
            'error': error.description or 'Conflict',
            'path': request.path
        }), 409
    
    @app.errorhandler(413)
    def request_entity_too_large_error(error):
        """Handle 413 Request Entity Too Large errors."""
        app.logger.warning('Request Entity Too Large')
        return jsonify({
            'success': False,
            'error': 'The request is too large.',
            'max_size': app.config.get('MAX_CONTENT_LENGTH', 0)
        }), 413
    
    @app.errorhandler(422)
    def unprocessable_entity_error(error):
        """Handle 422 Unprocessable Entity errors."""
        app.logger.warning(f'Unprocessable Entity: {error.description}')
        return jsonify({
            'success': False,
            'error': error.description or 'Unprocessable Entity',
            'path': request.path
        }), 422
    
    @app.errorhandler(429)
    def too_many_requests_error(error):
        """Handle 429 Too Many Requests errors."""
        app.logger.warning('Too Many Requests')
        return jsonify({
            'success': False,
            'error': 'Too many requests, please try again later.',
            'retry_after': error.retry_after if hasattr(error, 'retry_after') else None
        }), 429
    
    @app.errorhandler(500)
    def internal_server_error(error):
        """Handle 500 Internal Server errors."""
        app.logger.error(f'Internal Server Error: {error}')
        app.logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': 'An internal server error occurred. Please try again later.'
        }), 500
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        """Handle all other exceptions."""
        # Pass through HTTP exceptions
        if isinstance(error, HTTPException):
            return error
        
        # Log the error
        app.logger.error(f'Unhandled Exception: {str(error)}')
        app.logger.error(traceback.format_exc())
        
        # Return a 500 error
        return jsonify({
            'success': False,
            'error': 'An unexpected error occurred. Please try again later.'
        }), 500
    
    # Register a handler for 400 errors raised by Flask
    @app.errorhandler(400)
    def handle_bad_request(e):
        return jsonify({
            'success': False,
            'error': e.description or 'Bad Request',
            'path': request.path
        }), 400
    
    # Register a handler for 404 errors
    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify({
            'success': False,
            'error': 'The requested resource was not found.',
            'path': request.path
        }), 404
    
    # Register a handler for 405 errors
    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({
            'success': False,
            'error': 'The method is not allowed for the requested URL.',
            'path': request.path,
            'method': request.method
        }), 405
