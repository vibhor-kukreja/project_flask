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
from app.auth.validations import user_signup, user_login
from app.utils.validator import validator

mod_auth = Blueprint("auth", __name__, url_prefix="/auth")


@mod_auth.route("/signup/", methods=["POST"])
@validator([user_signup])
def signup():
    """
       API to Sign up with a new user.
       :return: JSON response
    """
    payload = request.get_json()
    try:
        payload['password'] = generate_password_hash(payload['password'])
        user = User.create(**payload)
        return success(data=user)
    except ValueError as err:
        return failure(message=err)


@mod_auth.route("/login/", methods=["POST"])
@validator([user_login])
def login():
    """
       API to login user.
       :return: JSON response
    """
    payload = request.get_json()
    user = User.query.filter_by(email=payload.get('email')).first()
    if user and check_password_hash(user.password, payload.get('password')):
        expires = datetime.timedelta(
            minutes=current_app.config['AUTH_TOKEN_TTL_MINUTES'])
        access_token = create_access_token(
            identity=json.dumps({"id": user.id, "email": user.email}),
            expires_delta=expires)
        return success(data={"access_token": access_token})
    return failure(message="Invalid credentials")


@mod_auth.route("/test/", methods=["GET"])
@jwt_required
def test():
    """
       API to test AUTH.
       :return: String
    """
    user = json.loads(get_jwt_identity())
    return success(data=user, message="Authenticated")
