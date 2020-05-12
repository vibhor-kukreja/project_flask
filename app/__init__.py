import os

# Import flask and template operators
from flask import Flask, render_template

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from config import flask_config

# Define the WSGI application object
app = Flask(__name__)

# Configurations
if not os.getenv("FLASK_ENV"):
    raise EnvironmentError("FLASK_ENV not set")
environment_config = flask_config[app.config["ENV"]]
app.config.from_object(environment_config)

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)


# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    print(error)
    return render_template("404.html"), 404


# Import a module / component using its blu eprint handler variable (auth)
from app.auth.controllers import mod_auth as auth_module

# Register blueprint(s)
app.register_blueprint(auth_module)
# app.register_blueprint(xyz_module)
# ..

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()
