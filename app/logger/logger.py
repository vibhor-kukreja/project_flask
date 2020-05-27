# Import logging.handlers and logging
# modules for generating and saving logs
import logging.handlers
import logging

# Importing app for getting ENV variables
# for log level and file path
from typing import Callable

logger = logging.getLogger()


def init_logger(app):

    # Creating a logger object and setting the level

    log_level = getattr(logging, app.config.get('LOG_LEVEL'))
    logger.setLevel(log_level)

    # Defining the path where the logs files will be made and
    # logs of one week will be maintained and when = 'D' means
    # logs for each day in maintained in a single file
    file_handler = logging.handlers.TimedRotatingFileHandler(
        filename=app.config.get("LOG_FILE_PATH"), when='D')

    #  Stream Handler
    stream_handler = logging.StreamHandler()

    # Defining the formatting style of the file and stream
    file_formatter = logging.Formatter(""
                                       "{'time': '%(asctime)s',"
                                       " 'name': '%(name)s', "
                                       " 'level': '%(levelname)s',"
                                       " 'file': '%(filename)s', "
                                       " 'line': '%(lineno)d', "
                                       " 'threadName': '%(threadName)s', "
                                       " 'message': '%(message)s'}"
                                       )

    stream_formatter = logging.Formatter(
        '%(asctime)-15s %(levelname)-8s '
        '%(filename)s %(lineno)d '
        '%(message)s')

    # Setting up the formatter with handlers and
    # adding the handlers to the logger
    file_handler.setFormatter(file_formatter)
    stream_handler.setFormatter(stream_formatter)

    def decorate_emit(func: callable) -> Callable:
        """
        This decorator method will add colors
        to the logs accordingly
        :param func: Emit function for stream
        :return: Function for emitting colors
        i.e. color_log
        """
        def color_log(*args: tuple) -> Callable:
            """
            This method will give
            different colors to the log.
            :param args:
            :return: function with changed colors
            """
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
            args[0].filename = f"{color} {args[0].filename}\x1b[0m"

            return func(*args)

        return color_log

    # Emitting colored stream
    stream_handler.emit = decorate_emit(stream_handler.emit)

    # Adding file and stream handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
