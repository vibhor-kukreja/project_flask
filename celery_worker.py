"""Celery worker script to initiate worker via celery cmd"""
from app import create_app
from celery_app import celery
from celery_app.celery_utils import init_celery

# Initialise a celery worker instance with the flask app
app = create_app()
init_celery(celery, app)
