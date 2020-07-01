# All test cases related to the services will be written here.
from tests.constants import TestConstants


class TestServices:
    """
    This class will test the methods
    in auth services.
    """
    def test_create_user_ok(self,
                            test_client,
                            init_database):
        """
        GIVEN a database
        WHEN create_user() in auth services
        is called
        THEN creates a user
        :param test_client:
        :param init_database:
        :return: None
        """

        from app.auth.services import create_user

        name = TestConstants.TEST_USER_NAME
        email = TestConstants.TEST_USER_EMAIL_1
        password = TestConstants.TEST_USER_PASSWORD

        user = create_user(name, email, password)

        assert name == user[1].get('name')
        assert email == user[1].get('email')

    def test_create_user_fail(self,
                              test_client,
                              init_database):
        """
        GIVEN a database
        WHEN create_user() in auth services
        is called
        THEN throws an error that user
        already exists
        :param test_client:
        :param init_database:
        :return: None
        """

        from app.auth.services import create_user

        name = TestConstants.TEST_USER_NAME
        email = TestConstants.TEST_USER_EMAIL
        password = TestConstants.TEST_USER_PASSWORD

        user = create_user(name, email, password)

        assert str(user[0]) == TestConstants.EMAIL_ALREADY_EXISTS
        assert user[1] is None

    def test_get_auth_token_ok(self,
                               test_client,
                               init_database):
        """
        GIVEN a database
        WHEN get_auth_token() in auth
        services is called
        THEN return an auth token
        :param test_client:
        :param init_database:
        :return: None
        """

        from app.auth.services import get_auth_token

        email = TestConstants.TEST_USER_EMAIL
        password = TestConstants.TEST_USER_PASSWORD

        token = get_auth_token(email, password)

        assert token[0] is None
        assert type(token[1]) is str

    def test_get_auth_token_fail(self,
                                 test_client,
                                 init_database):
        """
        GIVEN a non existing user
        WHEN get_auth_token() in auth
        services is called
        THEN return an error
        :param test_client:
        :param init_database:
        :return: None
        """

        from app.auth.services import get_auth_token

        email = TestConstants.TEST_USER_EMAIL_2
        password = TestConstants.TEST_USER_PASSWORD

        token = get_auth_token(email, password)

        assert str(token[0]) == TestConstants.INVALID_CREDENTIALS
        assert token[1] is None

    def test_get_auth_token_fail2(self,
                                  test_client,
                                  init_database):
        """
        GIVEN an existing user
        WHEN get_auth_token() in auth
        services is called
        THEN return an error due to wrong password
        :param test_client:
        :param init_database:
        :return: None
        """

        from app.auth.services import get_auth_token

        email = TestConstants.TEST_USER_EMAIL_2
        password = TestConstants.WRONG_PASSWORD

        token = get_auth_token(email, password)

        assert str(token[0]) == TestConstants.INVALID_CREDENTIALS
        assert token[1] is None
