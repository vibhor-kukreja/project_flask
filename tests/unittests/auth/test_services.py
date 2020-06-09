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
        :return:
        """

        from app.auth.services import create_user

        name = 'Test User'
        email = 'test_user1@email.com'
        password = 'TestPassword'

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
        :return:
        """

        from app.auth.services import create_user

        name = 'Test User'
        email = 'test_user@email.com'
        password = 'TestPassword'

        user = create_user(name, email, password)

        assert str(user[0]) == 'Email already exists'
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
        :return:
        """

        from app.auth.services import get_auth_token

        email = 'test_user@email.com'
        password = 'TestPassword'

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
        :return:
        """

        from app.auth.services import get_auth_token

        email = 'test_user2@email.com'
        password = 'TestPassword'

        token = get_auth_token(email, password)

        assert str(token[0]) == "Invalid credentials"
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
        :return:
        """

        from app.auth.services import get_auth_token

        email = 'test_user2@email.com'
        password = 'WrongPassword'

        token = get_auth_token(email, password)

        assert str(token[0]) == "Invalid credentials"
        assert token[1] is None
