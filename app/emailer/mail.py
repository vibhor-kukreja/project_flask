import socket
from flask_mail import Message
from typing import AnyStr, Dict, Union, List
from flask import render_template
from jinja2 import TemplateNotFound

from app import mailer
from app.custom.logger import logger

from .constants import TEMPLATES_SUBJECTS, ErrorMessage


def send_mail(to: Union[List, AnyStr], template: AnyStr = "",
              body: AnyStr = None, data: Dict = None) -> None:
    """
    This function is used to send an email via Flask-Mail extension.
    :param to: recipients in form of string or list
    :param template: template name
    :param body: body of the email
    :param data: data used to render the template in form of dict
    """
    try:
        if not body and not template:
            raise ValueError(ErrorMessage.NOT_BODY_TEMPLATE)

        subject = TEMPLATES_SUBJECTS.get(template)
        msg = Message(subject=subject,
                      recipients=[to] if isinstance(to, str) else to)

        if template:
            template = render_template(f"email_templates/{template}.html",
                                       data=data)
            msg.html = template

        msg.body = body
        mailer.send(msg)
        logger.info("mail send successfully")

    except TemplateNotFound as err:
        logger.error(ErrorMessage.TEMPLATE_404.format(err))
        ValueError(ErrorMessage.GENERIC_ERROR)

    except socket.gaierror as err:
        logger.error(ErrorMessage.NOT_SENT + str(err))
        ValueError(ErrorMessage.GENERIC_ERROR)

    except Exception as err:
        logger.error(str(err))
        raise ValueError(ErrorMessage.GENERIC_ERROR)


