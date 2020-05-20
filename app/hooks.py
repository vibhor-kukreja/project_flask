from datetime import datetime as dt
from flask import request


def init_hooks(app, register_hooks=False):
    if not register_hooks:
        return
    from app import logger
    @app.before_first_request
    def before_first_request():
        pass
    
    @app.before_request
    def before_request():
        pass
    
    @app.after_request
    def after_request(response):
        """ Logging after every request. """
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
