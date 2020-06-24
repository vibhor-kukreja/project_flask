# Constants for templates subjects
TEMPLATE_SUBJECTS = {
    'confirm_email': 'EMAIL CONFIRMATION',
    'reset_password': 'RESET PASSWORD'
}


class ErrorMessage(object):
    """
    Constants for Error Messages
    """
    TEMPLATE_404 = 'Unable to locate template {}'
    GENERIC_ERROR = 'Something went wrong'
    NOT_SENT = 'Not able to send, Please check your connection'
    TEMPLATE_REQUIRED = 'Template name is required'
