# Test cases for controllers.py in auth module
from tests.unittests.auth.test_data import user_details
from tests.constants import TestConstants


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
        :return: None
        """
        email = TestConstants.TEST_USER_EMAIL
        password = TestConstants.TEST_USER_PASSWORD
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
        :return: None
        """
        email = TestConstants.INVALID_USER_EMAIL
        password = TestConstants.TEST_USER_PASSWORD
        response = test_client.post('/auth/login/',
                                    json=dict(email=email,
                                              password=password),
                                    )
        assert response.status_code == 200
        assert response.json.get('status') == 'FAILURE'
        assert response.json.get('data') is None
        assert response.json.get('code') == 400

    def test_authenticate_ok(self, test_client,
                             init_database, auth,
                             module_mocker):
        """
        GIVEN a test client, user and jwt token
        WHEN the '/test' url is hit
        THEN check if user is authenticated
        :param test_client:
        :param init_database:
        :param auth:
        :param module_mocker:
        :return: None
        """
        token = auth(TestConstants.TEST_USER_EMAIL,
                     TestConstants.TEST_USER_PASSWORD)

        # mocked the get_jwt_identity() method from controllers
        module_mocker.patch(
            'app.auth.controllers.get_jwt_identity',
            return_value=user_details())

        response = test_client.get('/auth/test/',
                                   headers={
                                       'Authorization': 'Bearer ' + token[1]})

        assert 'test' in response.json.get('data')['email']
        assert 'Authenticated' in response.json.get('message')
