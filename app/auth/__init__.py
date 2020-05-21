from flask_jwt_extended import JWTManager
from typing import Dict, Union

from app import app, failure

# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = app.config['JWT_SECRET_KEY']
jwt = JWTManager(app)


@jwt.expired_token_loader
@jwt.invalid_token_loader
@jwt.unauthorized_loader
def token_error_callback(error: Union[str, dict]) -> Dict:
    """
    This method returns a callback error
    if the token is expired, invalid
    or is unauthorized.
    :param error: Any kind of error string
    :return: A JSON response containing
    essential information with an error message.
    """
    error = error if isinstance(error, str) else "Token expired"
    return failure(message=error, status_code=401)
