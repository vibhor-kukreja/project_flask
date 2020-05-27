
from app.logger import logger
from celery_app import celery


# TODO: will be removed
@celery.task(bind=True, name='celery_add')
def c_add(self, a, c):
    """Dummy task"""
    logger.info(a + c)
    return a + c
