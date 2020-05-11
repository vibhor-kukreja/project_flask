"""Defines the Auth forms"""
# Import Form and RecaptchaField (optional)
# from flask.ext.wtf import Form # , RecaptchaField
from wtforms import Form

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import PasswordField, StringField  # BooleanField

# Import Form validators
from wtforms.validators import Email, DataRequired


# Define the login form (WTForms)


class LoginForm(Form):
    """
    Class defining the login form
    """

    email = StringField(
        "Email Address",
        [Email(), DataRequired(message="Forgot your email address?")]
    )
    password = PasswordField(
        "Password", [DataRequired(message="Must provide a password. ;-)")]
    )
