from typing import Dict

from flask import Blueprint, request

from app.product.services import fetch_all, fetch_single
from app import success, failure

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_product = Blueprint("product", __name__, url_prefix="/product")


@mod_product.route("/all/", methods=["GET"])
def get_all_items() -> Dict:
    """
    This method will return all
    the items available.
    :return: JSON response
    """
    filters = request.args
    error, items = fetch_all(filters)
    return success(data=items) if not error else failure(message=error)


@mod_product.route("/single/<obj_id>", methods=["GET"])
def get_single_item(obj_id) -> Dict:
    """
    This method will return the
    single item with given object id.
    :param obj_id: Object ID
    :return: JSON response
    """
    error, item = fetch_single(obj_id)
    return success(data=item) if not error else failure(message=error)
