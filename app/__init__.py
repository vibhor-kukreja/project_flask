"""This module is the core of the project."""

# Import flask and template operators
from flask import Flask

from .utils.mongo_init import MongoAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from app.exception_handler import init_error_handler
from app.hooks import init_hooks
from app.logger import init_logger
from app.seed import init_seed_script
from app.utils.response_helper import success_response as success, \
                                      failure_response as failure, \
                                      error_response as error
# Globally accessible libraries
db = SQLAlchemy()
ma = Marshmallow()
mongo_db = MongoAlchemy()


def create_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_pyfile('../config.py')

    db.init_app(app)
    mongo_db.init_app(app)
    ma.init_app(app)

    init_logger(app)
    init_error_handler(app)
    init_hooks(app, app.config['HOOKS_REQUIRED'])

    with app.app_context():
        # Import a module/component using its blueprint handler variable (auth)
        from app.auth.controllers import mod_auth as auth_module
        from app.init_services import init_database

        # Register blueprint(s)
        app.register_blueprint(auth_module)

        init_database()
        init_seed_script()
        return app
