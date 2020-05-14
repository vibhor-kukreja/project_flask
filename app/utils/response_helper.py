from datetime import datetime
from functools import partial
import time

from flask_api import status
from app.utils.constants import APP_NAME, DATETIME_FORMAT


class ResponseMaker(object):
    """
    Class containing methods to construct response as output for APIs
    """
    @staticmethod
    def get_status(status_code):
        """
        To determine the type of response based on status_code
        :param status_code: Integer value ranging 200-500
        :return: String
        """
        if status.is_success(status_code):
            return "SUCCESS"
        elif status.is_client_error(status_code):
            return "FAILURE"

    def build_response(self, **kwargs):
        """
        This method is responsible to get values and call create_response
        :param kwargs:
        :return: JSON Response
        """
        status_code = kwargs.get('status_code')
        data = kwargs.get('data')
        message = kwargs.get('message')
        response_type = self.get_status(status_code)
        return self._create_response(response_type, status_code,
                                     data, message)

    @staticmethod
    def _create_response(response_type, status_code, data=None, message=None):
        """
        Defines the common response format with required parameters
        :param response_type: can be any one of 2 values: success or failure
        :param status_code: depending on the status of the response
        :param data: in case of success or failure, this value is used
        :param message: in case of error, this will contain the error
        :return: A JSON containing all response values
        """
        base_response = {
            "program": APP_NAME,
            "version": "1.0",
            "datetime": datetime.now().strftime(DATETIME_FORMAT),
            "timestamp": time.time(),
            "status": response_type,
            "code": status_code,
            "message": message,
            "data": data
            }
        return base_response
