"""Constant file for Utils"""


class DisplayMessage(object):
    EXECUTE_MISSING = "Module named '{}' has no method execute"
    MODULE_MISSING = "Module named '{}' doesn't exist"
    WRITING_SEED_DATA = "Writing seed data for {}"
    WRITING_SUCCESSFUL = "Writing successful for {}"
    CONNECTION_REFUSED = "Unable to connect with the database. " \
                         "Ensure connection and credentials and correct."


POOL_CHUNK_SIZE = 100
APP_NAME = "my_flask_app"
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
