from flask import request

from app.auth.models import user_schema


def _get_error_list(_errors):
    errors = []
    for err in _errors:
        errors.append({
            "code": "VALIDATION_ERROR",
            "field": err,
            "msg": _errors.get(err, "")
        })
    return errors if errors else None


def user_signup():
    payload = request.get_json()
    _errors = user_schema.validate(payload)
    return _get_error_list(_errors)


def user_login():
    payload = request.get_json()
    _errors = user_schema.validate(
        payload,
        partial=['id', 'name', 'date_modified', 'date_created'])
    return _get_error_list(_errors)
