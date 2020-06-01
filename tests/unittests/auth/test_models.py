# Test cases for models.py in auth module


def test_new_user(test_client, new_user) -> None:
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the name, email and password
    :return: None
    """
    assert new_user.id == 1
    assert new_user.name == "TestUser"
    assert new_user.email == "test@email.com"
    assert new_user.password == "TestPassword"
