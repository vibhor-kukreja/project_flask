# Test cases for models.py in auth module
from tests.constants import TestConstants


class TestModels:
    """
    This class contains the test cases for
    auth models.
    """
    def test_new_user_ok(self, test_client) -> None:
        """
        GIVEN a User model
        WHEN a new User is created
        THEN check the name, email and password
        :return: None
        """
        from app.auth.models import User

        new_user = User(id=1,
                        name=TestConstants.TEST_USER_NAME,
                        email=TestConstants.TEST_USER_EMAIL_3,
                        password=TestConstants.TEST_USER_PASSWORD)

        assert new_user.id == 1
        assert new_user.name == TestConstants.TEST_USER_NAME
        assert new_user.email == TestConstants.TEST_USER_EMAIL_3
        assert new_user.password == TestConstants.TEST_USER_PASSWORD

    def test_new_user_fail(self, test_client) -> None:
        """
        GIVEN a wrong User model
        WHEN a new User is created
        THEN check the name, email and password
        :return: None
        """
        from app.auth.models import User

        new_user = User(name=TestConstants.TEST_USER_NAME,
                        email=TestConstants.TEST_USER_EMAIL_3,
                        password=TestConstants.TEST_USER_PASSWORD)

        assert new_user.id != 1
        assert new_user.name == TestConstants.TEST_USER_NAME
        assert new_user.email == TestConstants.TEST_USER_EMAIL_3
        assert new_user.password == TestConstants.TEST_USER_PASSWORD
