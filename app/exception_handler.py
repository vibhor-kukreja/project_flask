import traceback
from typing import Dict


from app.logger import logger
from app.utils.response_helper import error_response as error


def init_error_handler(app):
    """ Function to initial global error handler for API response
    :arg app : Application reference
    """
    @app.errorhandler(Exception)
    def handle_invalid_usage(err: Exception) -> Dict:
        """
        This method will handle the exceptions
        if any type of invalid access is reported.
        :param err: Any kind of exception
        :return: A JSON response with essential
        information and an error message
        """
        logger.error(traceback.print_exc())
        return error(message=err)
