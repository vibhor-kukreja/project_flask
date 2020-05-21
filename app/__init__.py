"""This module is the core of the project."""
import os

# Import flask and template operators
from typing import Dict

from flask import Flask

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from app.hooks import init_hooks
from config import APP_ENV_CONFIGS
from app.utils.response_helper import success_response as success, \
                                      failure_response as failure, \
                                      error_response as error

# Define the WSGI application object
app = Flask(__name__)

# Configurations
if not os.getenv("FLASK_ENV"):
    app.config["ENV"] = "local"
try:
    environment_config = APP_ENV_CONFIGS[app.config["ENV"]]
except KeyError:
    raise EnvironmentError(
        "FLASK_ENV not set properly. Options: [local, production, staging]")

app.config.from_object(environment_config)

# Import logger
from app.logger import logger

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)
ma = Marshmallow(app)


@app.errorhandler(Exception)
def handle_invalid_usage(err):
    return error(message=err)


# Import a module / component using its blueprint handler variable (auth)
from app.auth.controllers import mod_auth as auth_module

# Register blueprint(s)
app.register_blueprint(auth_module)
# app.register_blueprint(xyz_module)

# Added hooks event to the request workflow.
init_hooks(app, app.config['HOOKS_REQUIRED'])

# This will call seed script and run related methods
from app.utils.seed_script import initialize_seed_script
initialize_seed_script()
