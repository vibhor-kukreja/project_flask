import redis


class Redis:
    def __init__(self):
        self.url = None
        self.client = None

    def init_app(self, app):
        self.url = app.config.get("REDIS_URL")
        self.client = redis.from_url(self.url)

