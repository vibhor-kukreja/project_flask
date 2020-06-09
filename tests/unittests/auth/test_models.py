# Test cases for models.py in auth module


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
                        name="TestUser",
                        email="test@email.com",
                        password="TestPassword")

        assert new_user.id == 1
        assert new_user.name == "TestUser"
        assert new_user.email == "test@email.com"
        assert new_user.password == "TestPassword"

    def test_new_user_fail(self, test_client) -> None:
        """
        GIVEN a wrong User model
        WHEN a new User is created
        THEN check the name, email and password
        :return: None
        """
        from app.auth.models import User

        new_user = User(name="TestUser",
                        email="test@email.com",
                        password="TestPassword")

        assert new_user.id != 1
        assert new_user.name == "TestUser"
        assert new_user.email == "test@email.com"
        assert new_user.password == "TestPassword"
