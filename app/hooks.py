from datetime import datetime as dt
from flask import request

from app.custom.logger import logger


def init_hooks(app, register_hooks=False):
    """
    This method will initialize the
    hooks accordingly
    :param app: Flask object
    :param register_hooks:
    :return: Response
    """
    if not register_hooks:
        return

    @app.before_first_request
    def before_first_request():
        pass
    
    @app.before_request
    def before_request():
        pass
    
    @app.after_request
    def after_request(response: object) -> object:
        """
        Logging after every request
        :param response:
        :return:
        """
        logger.debug(
            "{} {} {} {} {} {} {} {} {}".format(
                request.remote_addr,
                dt.utcnow(),
                request.method,
                request.path,
                request.scheme,
                response.status,
                response.content_length,
                request.referrer,
                request.user_agent))
        return response
    
    @app.teardown_request
    def teardown_request(error):
        pass
