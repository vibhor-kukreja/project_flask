from typing import List, Union

from flask import request

from app.auth.models import user_schema


def _get_error_list(_errors: dict) -> Union[List, None]:
    """
    This method return a list of errors,
    if any exists
    :param _errors: Dict of errors
    :return: List of errors or None
    """
    errors = []
    for err in _errors:
        errors.append({
            "code": "VALIDATION_ERROR",
            "field": err,
            "msg": _errors.get(err, "")
        })
    return errors if errors else None


def user_signup() -> Union[List, None]:
    """
    This method validates the data
    during signup and returns the
    list of errors, if any exists.
    :return: List of errors or None
    """
    payload = request.get_json()
    _errors = user_schema.validate(payload)
    return _get_error_list(_errors)


def user_login() -> Union[List, None]:
    """
    This method validates the data
    during login and returns the
    list of errors, if any exists.
    :return: List of errors or None
    """
    payload = request.get_json()
    _errors = user_schema.validate(
        payload,
        partial=['id', 'name', 'date_modified', 'date_created'])
    return _get_error_list(_errors)
