import time
from flask import request, g
import logging

def init_request_logging(app):
    """Initialize request logging middleware."""
    logger = logging.getLogger('request')
    
    @app.before_request
    def start_timer():
        g.start_time = time.time()
    
    @app.after_request
    def log_request(response):
        """Log details of each request."""
        # Skip logging for health checks and other noisy endpoints
        if request.path in ['/health', '/favicon.ico']:
            return response
            
        # Calculate request processing time
        duration = round((time.time() - g.start_time) * 1000, 2)  # in milliseconds
        
        # Get client IP
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        
        # Get user agent
        user_agent = request.headers.get('User-Agent', '')
        
        # Get user ID if authenticated
        user_id = getattr(g, 'user_id', None)
        
        # Log the request details
        log_data = {
            'method': request.method,
            'path': request.path,
            'status': response.status_code,
            'duration': f"{duration}ms",
            'ip': ip,
            'user_agent': user_agent,
            'user_id': user_id,
            'query_params': dict(request.args),
            'content_type': request.content_type,
            'content_length': request.content_length or 0,
        }
        
        # Log form data for non-GET requests (excluding file uploads)
        if request.method != 'GET' and not request.files:
            try:
                if request.is_json:
                    log_data['request_data'] = request.get_json()
                elif request.form:
                    log_data['form_data'] = dict(request.form)
            except Exception:
                pass  # Don't fail if we can't log the request data
        
        # Log the request
        logger.info(
            "%s %s %s %s %s %dms",
            ip,
            request.method,
            request.path,
            request.query_string.decode('utf-8') if request.query_string else '',
            response.status,
            duration,
            extra={
                'request': log_data,
                'user_id': user_id,
                'duration': duration,
            }
        )
        
        return response

def log_request_metrics(response):
    """Log metrics for the request."""
    from flask import g, request
    from prometheus_client import Counter, Histogram
    import time
    
    # Define metrics
    REQUEST_COUNT = Counter(
        'http_requests_total',
        'Total HTTP Requests',
        ['method', 'endpoint', 'http_status']
    )
    
    REQUEST_LATENCY = Histogram(
        'http_request_duration_seconds',
        'HTTP Request Latency',
        ['method', 'endpoint']
    )
    
    # Get request duration
    request_duration = time.time() - g.get('start_time', time.time())
    
    # Get endpoint (use rule.endpoint if available, otherwise use request.path)
    endpoint = request.endpoint or request.path
    
    # Record metrics
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=endpoint,
        http_status=response.status_code
    ).inc()
    
    REQUEST_LATENCY.labels(
        method=request.method,
        endpoint=endpoint
    ).observe(request_duration)
    
    return response
