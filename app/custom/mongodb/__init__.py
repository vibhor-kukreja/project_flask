from flask import Flask
from pymodm import MongoModel, fields
from pymodm.connection import connect
from pymongo.errors import ServerSelectionTimeoutError

from app.utils.constants import CONFIG_NOT_FOUND, DisplayMessage


class MongoAlchemy:

    fields = fields
    Model = MongoModel

    def __init__(self):
        """
        Initialize variables for the MongoDB database connection
        """
        self.database_uri = None
        self.db = None
        self.client = None
        self.config = dict()
        # default configuration for MongoDB server connection
        self.max_pool = 100
        self.min_pool = 0
        self.max_idle_time = None
        self.connection_timeout = 10000
        self.heartbeat_frequency = 10000
        self.server_timeout = 30000

    def init_app(self, app: Flask = None) -> None:
        """
        This function will get config values
        to set configurations for connection
        :param app: Instance of the Flask App
        :return: None
        """
        # get the database url to connect to
        self.database_uri = app.config.get("MONGODB_DATABASE_URI")

        # configuration for the connection
        self.config['maxPoolSize'] = \
            app.config.get("MAX_POOL_SIZE") or self.max_pool
        self.config["minPoolSize"] = \
            app.config.get("MIN_POOL_SIZE") or self.min_pool
        self.config["maxIdleTimeMS"] = \
            app.config.get("MAX_IDLE_TIME") or self.max_idle_time
        self.config["connectTimeoutMS"] = \
            app.config.get("CONNECTION_TIMEOUT") or self.connection_timeout
        self.config["heartbeatFrequencyMS"] = \
            app.config.get("HEARTBEAT_FREQUENCY") or self.heartbeat_frequency
        self.config["serverSelectionTimeoutMS"] = \
            app.config.get("SERVER_SELECTION_TIMEOUT") or self.server_timeout

        # connect with the database
        self._connect()

    def _connect(self) -> None:
        """
        This method will connect to the MongoDB
        via URL using a MongoClient
        :return: None
        """
        if not self.database_uri:
            raise KeyError(CONFIG_NOT_FOUND.format("MONGODB_DATABASE_URI"))
        connect(self.database_uri, connect=True, **self.config)

    @staticmethod
    def test_connection(model_name: MongoModel) -> None:
        """
        This method will test the connection to ensure whether the DB
        is available or not
        :param model_name: MongoModel instance to check connection on
        :return: None
        """
        # TODO: To change approach on how to check if connection is established
        try:
            _ = list(model_name.objects.all())
        except ServerSelectionTimeoutError:
            raise IOError(DisplayMessage.CONNECTION_REFUSED)
