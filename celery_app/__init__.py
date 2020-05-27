from celery import Celery


def make_celery(app_name: str = __name__) -> Celery:
    """
    Will provide a raw instance of celery
    :arg app_name: defines the name of the app
    """
    return Celery(app_name)


celery = make_celery()
