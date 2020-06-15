from datetime import datetime
from functools import partial
import time
from typing import AnyStr, Dict, Union

from flask import make_response
from flask_api import status
from werkzeug import Response

from app.utils.constants import APP_NAME, DATETIME_FORMAT


class ResponseMaker(object):
    """
    Class containing methods to construct response as output for APIs
    """
    @staticmethod
    def get_status(status_code: int) -> AnyStr:
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

    def build_response(self, **kwargs: dict) -> Dict:
        """
        This method is responsible to get values and call create_response
        :param kwargs: Dict
        :return: JSON Response
        """
        data = kwargs.get("data")
        errors = kwargs.get("errors")
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
                                       data, message, errors)

    def pdf_response(self, **kwargs: dict) -> Response:
        """
        This method is responsible to get pdf and return response
        :param kwargs: Dict
        :return: JSON Response
        """
        pdf = kwargs.get("pdf")
        pdf_name = kwargs.get('name')
        status_code = kwargs.get('status_code')
        response_type = self.get_status(status_code)

        # Creating a response object for sending pdf file
        response = make_response(pdf, response_type)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline;filename={}.pdf'\
            .format(pdf_name)
        return response

    @staticmethod
    def _format_response(input_arg: str) -> Union:
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
    def _generate_response(response_type: str,
                           status_code: int,
                           data=None, message=None,
                           errors=None) -> Dict:
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
            "data": data,
            "errors": errors
            }
        return base_response


# Initialised the response maker object
response_maker = ResponseMaker()

# Response in case of success
success_response = partial(response_maker.build_response,
                           status_code=status.HTTP_200_OK)

# Response in case of failure
failure_response = partial(response_maker.build_response,
                           status_code=status.HTTP_400_BAD_REQUEST)

# Response in case of error
error_response = partial(response_maker.build_response,
                         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Response in case of error
pdf_response = partial(response_maker.pdf_response,
                       status_code=status.HTTP_200_OK)
