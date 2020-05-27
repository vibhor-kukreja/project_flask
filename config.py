"""Main configuration file"""
# Define the application directory
from os import getenv, path
from dotenv import load_dotenv

BASE_DIR = path.abspath(path.dirname(__file__))

current_env = getenv("FLASK_ENV") or 'local'
if not path.exists("{}.env".format(current_env)):
    raise EnvironmentError("FLASK_ENV not set properly for {} env.".format(
        current_env))

# loading the selected .env file
project_folder = path.expanduser(BASE_DIR)
load_dotenv(path.join(project_folder, "{}.env".format(current_env)))


# ######################## #
# #### Configurations #### #
# ######################## #


DEBUG = getenv('DEBUG')

SQLALCHEMY_DATABASE_URI = getenv('SQLALCHEMY_DATABASE_URI')
# To disable tracking modifications on Objects by Flask-SQLAlchemy
SQLALCHEMY_TRACK_MODIFICATIONS = getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
# MongoDB Configuration
MONGODB_DATABASE_URI = getenv("MONGODB_DATABASE_URI")
MAX_POOL_SIZE = getenv("MAX_POOL_SIZE")
MIN_POOL_SIZE = getenv("MIN_POOL_SIZE")
MAX_IDLE_TIME = getenv("MAX_IDLE_TIME")
CONNECTION_TIMEOUT = getenv("CONNECTION_TIMEOUT")
HEARTBEAT_FREQUENCY = getenv("HEARTBEAT_FREQUENCY")
SERVER_SELECTION_TIMEOUT = getenv("SERVER_SELECTION_TIMEOUT")


DATABASE_CONNECT_OPTIONS = getenv('DATABASE_CONNECT_OPTIONS')

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = getenv('THREADS_PER_PAGE')

# Enable protection again *Cr-site Request Forgery (CSRF)*
CSRF_ENABLED = getenv('CSRF_ENABLED')

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = getenv('CSRF_SESSION_KEY')

# Secret key for signing cookies
SECRET_KEY = getenv('SECRET_KEY')

AUTH_TOKEN_TTL_MINUTES = getenv('AUTH_TOKEN_TTL_MINUTES')
JWT_SECRET_KEY = getenv('JWT_SECRET_KEY')

HOOKS_REQUIRED = getenv('HOOKS_REQUIRED')

# Logs
LOG_LEVEL = getenv('LOG_LEVEL')
LOG_FILE_PATH = getenv('LOG_FILE_PATH')

# Celery
CELERY_BROKER_URL = getenv('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = getenv('CELERY_RESULT_BACKEND')
CELERY_SEND_TASK_SENT_EVENT = getenv('CELERY_SEND_TASK_SENT_EVENT')
