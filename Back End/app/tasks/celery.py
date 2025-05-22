"""
Celery configuration and task definitions.
"""
import os
from celery import Celery
from flask import current_app
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

def make_celery(app):
    """
    Create and configure a new Celery instance.
    
    Args:
        app: Flask application instance
        
    Returns:
        Celery: Configured Celery application
    """
    # Create Celery instance
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    
    # Set default Celery config
    celery.conf.update(
        broker_connection_retry_on_startup=True,
        broker_connection_retry=True,
        broker_connection_max_retries=5,
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='UTC',
        enable_utc=True,
        task_track_started=True,
        task_time_limit=30 * 60,  # 30 minutes
        task_soft_time_limit=25 * 60,  # 25 minutes
        worker_max_tasks_per_child=100,
        worker_prefetch_multiplier=1,
        worker_send_task_events=True,
        task_send_sent_event=True,
        event_queue_ttl=60,  # 1 minute
        worker_cancel_long_running_tasks_on_connection_loss=True,
        broker_heartbeat=10,  # 10 seconds
        broker_connection_timeout=30,  # 30 seconds
        broker_transport_options={
            'max_retries': 3,
            'interval_start': 0,
            'interval_step': 0.2,
            'interval_max': 0.5,
        },
        beat_schedule={
            # Scheduled tasks can be added here
            'cleanup-expired-sessions': {
                'task': 'app.tasks.scheduled.cleanup_expired_sessions',
                'schedule': timedelta(hours=24),  # Run daily
            },
            'send-scheduled-emails': {
                'task': 'app.tasks.scheduled.send_scheduled_emails',
                'schedule': timedelta(minutes=5),  # Run every 5 minutes
            },
        },
    )
    
    # Set up context so tasks have access to Flask app
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    
    celery.Task = ContextTask
    
    # Configure logging
    if app.config.get('CELERYD_HIJACK_ROOT_LOGGER', False):
        celery.conf.update(
            worker_hijack_root_logger=False,
            worker_log_format=app.config.get('CELERYD_LOG_FORMAT'),
            worker_task_log_format=app.config.get('CELERYD_TASK_LOG_FORMAT'),
        )
    
    return celery

# Create a default Celery instance that will be configured later
celery_app = None

def init_celery(app):
    """
    Initialize Celery with the Flask application.
    
    Args:
        app: Flask application instance
        
    Returns:
        Celery: Configured Celery application
    """
    global celery_app
    
    # Set default configuration
    app.config.setdefault('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    app.config.setdefault('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
    app.config.setdefault('CELERY_ACCEPT_CONTENT', ['json'])
    app.config.setdefault('CELERY_TASK_SERIALIZER', 'json')
    app.config.setdefault('CELERY_RESULT_SERIALIZER', 'json')
    app.config.setdefault('CELERYD_HIJACK_ROOT_LOGGER', False)
    
    # Configure logging
    app.config.setdefault(
        'CELERYD_LOG_FORMAT',
        '[%(asctime)s: %(levelname)s/%(processName)s] %(message)s'
    )
    app.config.setdefault(
        'CELERYD_TASK_LOG_FORMAT',
        ('[%(asctime)s: %(levelname)s/%(processName)s] ' +
         '[%(task_name)s(%(task_id)s)] %(message)s')
    )
    
    # Create Celery app
    celery_app = make_celery(app)
    
    # Import tasks to register them with Celery
    from . import email_tasks, scheduled, file_tasks
    
    # Log Celery configuration
    if app.debug:
        logger.info('Celery configuration:')
        for key, value in celery_app.conf.humanize().items():
            logger.info(f'  {key}: {value}')
    
    return celery_app
