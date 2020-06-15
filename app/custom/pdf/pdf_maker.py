import pdfkit
from flask import render_template
from jinja2 import TemplateNotFound

from app.custom.logger import logger
from .constants import ErrorMessage


def build_pdf(template: str, template_data: dict) -> bytes:
    """
    This method generates pdf.
    :param template: Name of the template file to be used
    :param template_data: Data to be rendered in the template
    :return: bytes of the generated pdf
    """

    try:
        template = render_template('pdf/{}.html'.format(template),
                                   **template_data)
    except TemplateNotFound as err:
        logger.error(ErrorMessage.TEMPLATE_404.format(err))
        raise ValueError(ErrorMessage.GENERIC_ERROR)

    pdf = pdfkit.from_string(template, False)
    return pdf
