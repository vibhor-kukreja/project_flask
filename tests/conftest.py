# All fixtures will be added here.
# Make sure you add those fixtures
# which have usage all over the module.

from typing import AnyStr, Tuple
import pytest
from flask_jwt_extended import JWTManager

from app import create_app

from app import db
from .constants import TestConstants
from app.custom.logger import logger


@pytest.fixture(scope='module')
def test_client():
    """
    This will create a client for the testing purpose.
    :return:
    """
    app = create_app()
    app.config['TESTING'] = True
    jwt = JWTManager(app)

    # Flask provides a way to test your application
    # by exposing the Werkzeug test Client and
    # handling the context locals for you.
    testing_client = app.test_client()

    # Establish an application context
    # before running the tests.
    ctx = app.app_context()
    ctx.push()

    yield testing_client  # This is where testing happens

    ctx.pop()


def get_hashed_password(password: str) -> AnyStr:
    """
    This method will return the hashed password
    :param password:
    :return: Hashed password
    """
    from werkzeug.security import generate_password_hash

    return generate_password_hash(password)


@pytest.fixture(scope='module')
def init_database():
    """
    This method will create
    the database.
    :return: None
    """
    from app.auth.models import User

    db.create_all()

    try:
        email = TestConstants.TEST_USER_EMAIL
        password = TestConstants.TEST_USER_PASSWORD
        hashed_password = get_hashed_password(password)

        user = User(
            name=TestConstants.TEST_USER_NAME,
            email=email,
            password=hashed_password
        )

        # Insert user data
        db.session.add(user)

        # Commit changes for user
        db.session.commit()

        yield db  # This is where testing happens

    except Exception as err:
        logger.info(err)
        raise Exception(err)

    finally:
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='module')
def auth() -> callable:
    """
    This method will return the auth
    token for the specified user.
    :return: Callable with tuple of None and (Token or Value Error)
    """
    def _get_user(email: str, password: str) -> Tuple:
        """
        This private method will help in
        fetching the auth token by
        hitting the get_auth_token method.
        :param email: email address in the form of string
        :param password: password in the form of string
        :return: Tuple of None and (Token or Value Error)
        """

        from app.auth.services import get_auth_token

        return get_auth_token(email, password)
    return _get_user
