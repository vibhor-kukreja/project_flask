"""Celery utility to update the celery configuration on runtime."""
from celery import Celery
from flask import Flask


def init_celery(celery: Celery, app: Flask) -> None:
    """
    Function to setup the celery configuration as the flask app and will
    bind the tasks with app context.
    """
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
