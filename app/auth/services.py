import datetime
import json
from typing import Tuple

from flask import current_app
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.auth.constants import ErrorMessage
from app.auth.models import User, user_schema


def create_user(name: str, email: str,
                password: str) -> Tuple:
    """
    This method creates the new user
    or throws ValueError if email
    already exists.
    :param name: Name of user in form of string
    :param email: Email of user in form of string
    :param password: Password of user in form of string
    :return: Tuple of None and ( ValueError or User Details )
    """
    user = User.query.filter_by(email=email).first()
    password = generate_password_hash(password)
    if not user:
        user = User(name=name,
                    email=email,
                    password=password)
        db.session.add(user)
        db.session.commit()
        return None, user_schema.dump(user)
    else:
        return ValueError(ErrorMessage.EMAIL_ALREADY_EXISTS), None


def get_auth_token(email: str, password: str) -> Tuple:
    """
    This method generates auth token for the existing user.
    :param email: Email string of user
    :param password: Password string of user
    :return: Tuple of None and ( ValueError or Access Token )
    """
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        expires = datetime.timedelta(
            minutes=current_app.config['AUTH_TOKEN_TTL_MINUTES'])
        access_token = create_access_token(
            identity=json.dumps({"id": user.id, "email": user.email}),
            expires_delta=expires)
        return None, access_token
    return ValueError(ErrorMessage.INVALID_CREDENTIALS), None
