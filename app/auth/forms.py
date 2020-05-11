# Import Form and RecaptchaField (optional)
# from flask.ext.wtf import Form # , RecaptchaField
from wtforms import Form

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import PasswordField, TextField  # BooleanField

# Import Form validators
from wtforms.validators import Email, EqualTo, Required

# Define the login form (WTForms)


class LoginForm(Form):
    email = TextField(
        "Email Address", [Email(), Required(message="Forgot your email address?")]
    )
    password = PasswordField(
        "Password", [Required(message="Must provide a password. ;-)")]
    )
