# Test cases for controllers.py in auth module


class TestLogin:
    """
    This class contains the E2E test cases
    for auth login method.
    """

    def test_login_ok(self, test_client, init_database):
        """
        GIVEN a database
        WHEN the '/login' page is posted to (POST)
        THEN check if response is valid
        :param test_client:
        :param init_database:
        :return:
        """
        email = 'test_user@email.com'
        password = "TestPassword"
        response = test_client.post('/auth/login/',
                                    json=dict(email=email,
                                              password=password),
                                    )
        assert response.status_code == 200
        assert response.json.get('status') == 'SUCCESS'
        assert response.json.get('data') is not None
        assert response.json.get('code') == 200

    def test_login_fail(self, test_client, init_database):
        """
        GIVEN a database
        WHEN the '/login' page is posted to (POST)
        THEN check if response is invalid
        :param test_client:
        :param init_database:
        :return:
        """
        email = 'test_user@email'
        password = "TestPassword"
        response = test_client.post('/auth/login/',
                                    json=dict(email=email,
                                              password=password),
                                    )
        assert response.status_code == 200
        assert response.json.get('status') == 'FAILURE'
        assert response.json.get('data') is None
        assert response.json.get('code') == 400
