"""
Background tasks package.

This package contains all background task definitions and utilities.
"""
from .celery import celery_app, init_celery
from . import email_tasks, file_tasks, scheduled

# Initialize Celery when this package is imported
# The actual initialization with Flask app happens in create_app()
__all__ = ['celery_app', 'init_celery', 'email_tasks', 'file_tasks', 'scheduled']
