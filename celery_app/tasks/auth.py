from app.custom.logger import logger
from celery_app import celery
from app.custom.emailer import send_mail


# TODO: will be removed
@celery.task(bind=True, name='celery_add')
def c_add(self, a, c):
    """Dummy task"""
    logger.info(a + c)
    return a + c


@celery.task(bind=True, name='celery_mail')
def send_mail_async(self, *args):
    """
    Asynchronous task to send mail
    """
    send_mail(*args)
    logger.info("Celery task Send Mail done Successfully")
