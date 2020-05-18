from flask_jwt_extended import JWTManager

from app import app, failure
# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = app.config['JWT_SECRET_KEY']
jwt = JWTManager(app)


@jwt.expired_token_loader
@jwt.invalid_token_loader
@jwt.unauthorized_loader
def token_error_callback(error):
    error = error if isinstance(error, str) else "Token expired"
    return failure(message=error, status_code=401)
