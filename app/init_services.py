"""File containing methods to initialize services for the app"""
from pymongo.errors import ServerSelectionTimeoutError
from sqlalchemy.exc import OperationalError

from app import mongo_db, db
from app.logger import logger
from app.utils.constants import DisplayMessage


def init_database() -> None:
    """
    This method will initialize database services and ensure their connection
    :return: None
    """
    try:
        # Connect to an existing postgreSQL database, otherwise create a new db
        db.engine.connect()
        # create models in database if they doesn't exist
        db.create_all()
        logger.info(DisplayMessage.CONNECTION_SUCCESSFUL.format("PostgreSQL"))

        # Connect to mongoDB Database
        mongo_db.connect()
        logger.info(DisplayMessage.CONNECTION_SUCCESSFUL.format("MongoDB"))

    except (OperationalError, ServerSelectionTimeoutError):
        raise IOError(DisplayMessage.CONNECTION_REFUSED)
    except Exception as err:
        raise err
