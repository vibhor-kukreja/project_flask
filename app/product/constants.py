"""To manage product constants"""


class ErrorMessage(object):
    """
    Constants for Error Messages
    """
    VALIDATION_ERROR = "Following errors while saving {}: {}"
    FETCH_DATA_ERROR = "Error while fetching data from the given database."
    ENTRY_DOES_NOT_EXISTS = "The requested entry with Object ID {} does not " \
                            "exists in the database"
