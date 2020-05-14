# Import logging.handlers and logging
# modules for generating and saving logs
import logging.handlers
import logging

# Creating a logger object and setting the level
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Defining the path where the logs files will be made and
# logs of one week will be maintained
file_handler = logging.handlers.TimedRotatingFileHandler(
    filename="app/logger/logs", when='D', backupCount=7)

#  Stream Handler
stream_handler = logging.StreamHandler()

# Defining the formatting style of the file and stream
file_formatter = logging.Formatter(""
                                   "{'time': '%(asctime)s',"
                                   "'name': '%(name)s', "
                                   "level': '%(levelname)s',"
                                   "'threadName': '%(threadName)s', "
                                   "'message': '%(message)s'}"
                                   )

stream_formatter = logging.Formatter(
    '%(asctime)-15s %(levelname)-8s %(message)s')

# Setting up the formatter with handlers and
# adding the handlers to the logger
file_handler.setFormatter(file_formatter)
stream_handler.setFormatter(stream_formatter)


def decorate_emit(func):
    """
    This method will add colors to the
    logs accordingly
    :param func:
    :return:
    """
    def color_log(*args):
        levelno = args[0].levelno
        if levelno >= logging.CRITICAL:
            color = '\x1b[30;1m'  # White
        elif levelno >= logging.ERROR:
            color = '\x1b[31;1m'  # Red
        elif levelno >= logging.WARNING:
            color = '\x1b[33;1m'  # Yellow
        elif levelno >= logging.INFO:
            color = '\x1b[34;1m'  # Cyan
        elif levelno >= logging.DEBUG:
            color = '\x1b[35;1m'  # Violet
        else:
            color = '\x1b[0m'  # No Color

        # add colors in the level name and message
        args[0].levelname = f"{color} {args[0].levelname}\x1b[0m"
        args[0].msg = f"{color} {args[0].msg}\x1b[0m"

        return func(*args)

    return color_log


# Emitting colored stream
stream_handler.emit = decorate_emit(stream_handler.emit)

# Adding file and stream handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)
