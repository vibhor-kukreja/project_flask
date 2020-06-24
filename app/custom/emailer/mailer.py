from flask_mail import Message
from flask import render_template
from jinja2 import TemplateNotFound
from typing import AnyStr, Dict, Union, List, ByteString

from app import mailer
from app.custom.logger import logger

from .constants import TEMPLATE_SUBJECTS, ErrorMessage


def send_mail(to: Union[List, AnyStr],
              template: AnyStr = "",
              data: Dict = None,
              pdf: ByteString = None,
              pdf_name="sample.pdf") -> None:
    """
    This function is used to send an email via Flask-Mail extension.
    :param to: recipients in form of string or list
    :param template: template name
    :param data: data used to render the template in form of dict
    :param pdf: pdf data in form of byte string
    :param pdf_name: name of pdf in form of string
    """

    if not template:
        raise ValueError(ErrorMessage.TEMPLATE_REQUIRED)

    subject = TEMPLATE_SUBJECTS.get(template)
    msg = Message(subject=subject,
                  recipients=[to] if isinstance(to, str) else to)

    try:
        template = render_template(f"email_templates/{template}.html",
                                   data=data)
        msg.html = template
    except TemplateNotFound as err:
        logger.error(ErrorMessage.TEMPLATE_404.format(err))
        raise ValueError(ErrorMessage.GENERIC_ERROR)

    if pdf:
        msg.attach(filename=pdf_name, content_type="application/pdf", data=pdf)

    mailer.send(msg)
    logger.info("Mail Send Successfully")

