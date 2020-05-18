import datetime
import json

from flask import (Blueprint, request, Response, jsonify, current_app)
from flask_api import status
from flask_jwt_extended import create_access_token, jwt_required, \
    get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash

# Import module models and schemas (i.e. User)
from app import success, failure
from app.auth.models import User, user_schema

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint("auth", __name__, url_prefix="/auth")


@mod_auth.route("/signup/", methods=["POST"])
def signup():
    """
       API to Sign up with a new user.
       :return: JSON response
    """
    payload = request.get_json()
    errors = user_schema.validate(payload)
    if errors:
        return failure(message=errors, status_code=status.HTTP_403_FORBIDDEN)
    try:
        payload['password'] = generate_password_hash(payload['password'])
        user = User.create(**payload)
        return success(data=user)
    except ValueError as err:
        return failure(message=err)


@mod_auth.route("/login/", methods=["POST"])
def login():
    """
       API to login user.
       :return: JSON response
    """
    payload = request.get_json()
    errors = user_schema.validate(
        payload,
        partial=['id', 'name', 'date_modified', 'date_created'])
    if errors:
        return Response(str(errors), 403)
    user = User.query.filter_by(email=payload.get('email')).first()
    if user and check_password_hash(user.password, payload.get('password')):
        expires = datetime.timedelta(
            minutes=current_app.config['AUTH_TOKEN_TTL_MINUTES'])
        access_token = create_access_token(
            identity=json.dumps({"id": user.id, "email": user.email}),
            expires_delta=expires)
        return jsonify({"access_token": access_token})
    return Response("", 403)


@mod_auth.route("/test/", methods=["GET"])
@jwt_required
def test():
    """
       API to test AUTH.
       :return: String
    """
    user = get_jwt_identity()
    print(user)
    return "Authenticated", 200
