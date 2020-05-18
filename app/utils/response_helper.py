import json
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
        if status.is_success(status_code) or status.is_redirect(status_code):
            return "SUCCESS"
        elif status.is_client_error(status_code):
            return "FAILURE"
        else:
            return "ERROR"

    def build_response(self, **kwargs):
        """
        This method is responsible to get values and call create_response
        :param kwargs:
        :return: JSON Response
        """
        data = kwargs.get("data")
        message = kwargs.get("message")
        status_code = kwargs.get('status_code')
        response_type = self.get_status(status_code)

        # reformat the data or message based on the response_type
        if response_type == "SUCCESS":
            # in case of success
            data = self._format_response(data)
        else:
            # in case of error or failure
            message = self._format_response(message)

        return self._generate_response(response_type, status_code,
                                       data, message)

    @staticmethod
    def _format_response(input_arg):
        """
        This method will format the given input in a desired format
        :param input_arg: Can be value of any type including dict, list, None
        :return: formatted input_arg
        """
        if input_arg is None:
            return None
        elif isinstance(input_arg, dict):
            return input_arg
        elif isinstance(input_arg, bytes):
            return input_arg.decode()
        else:
            return str(input_arg)

    @staticmethod
    def _generate_response(response_type, status_code, data=None, message=None):
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


response_maker = ResponseMaker()
success_response = partial(response_maker.build_response,
                           status_code=status.HTTP_200_OK)
failure_response = partial(response_maker.build_response,
                           status_code=status.HTTP_400_BAD_REQUEST)
error_response = partial(response_maker.build_response,
                         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
