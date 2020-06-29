import redis
from flask import Flask


class Redis:
    """
    This class acts as a wrapper over redis library
    Initializing methods which are used in flask nomenclature
    To keep the code for initialization similar to other modules
    """
    def __init__(self) -> None:
        """
        This method initializes the 2 values to be used in init_app() method
        """
        self.url = None
        self.client = None

    def init_app(self, app: Flask) -> None:
        """
        This method is responsible for initializing the redis client
        :param app: Flask
        :return:
        """
        self.url = app.config.get("REDIS_URL")
        if not self.url:
            raise ValueError("URL for redis not configured properly.")
        self.client = redis.from_url(self.url)
