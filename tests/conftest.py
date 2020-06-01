# All fixtures will be added here.
# Make sure you add those fixtures
# which have usage all over the module.

import pytest

from app import create_app

from app import db


@pytest.fixture(scope='module')
def test_client():
    app = create_app()
    app.config['TESTING'] = True

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


@pytest.fixture(scope='function')
def new_user() -> object:
    """
    This method will create a new user
    but will not save it anywhere.
    :return: User object
    """
    from app.auth.models import User
    user = User(id=1,
                name="TestUser",
                email="test@email.com",
                password="TestPassword")
    return user


@pytest.fixture(scope='module')
def init_database():
    """
    This method will create
    the database.
    :return: None
    """
    from app.auth.models import User
    from werkzeug.security import generate_password_hash

    db.create_all()

    try:
        email = "test_user@email.com"
        password = "TestPassword"
        hashed_password = generate_password_hash(password)

        user1 = User(
            name="TestUser",
            email=email,
            password=hashed_password
        )

        # Insert user data
        db.session.add(user1)

        # Commit changes for user
        db.session.commit()

        yield db  # This is where testing happens

    finally:
        db.session.remove()
        db.drop_all()
