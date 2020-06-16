from typing import Tuple

from app.product.constants import ErrorMessage
from app.product.models import Item, item_schema, items_schema
from bson.objectid import ObjectId


def fetch_all(filters=None) -> Tuple:
    """
    This method will fetch all
    the entries from database.
    :param: filters: Raw query filters
    :return: Tuple of None and ( ValueError or List of Items )
    """
    # TODO: Obtaining data when filters available

    items = Item.objects.all()

    if items:
        return None, items_schema.dump(items)
    else:
        return ValueError(ErrorMessage.FETCH_DATA_ERROR), None


def fetch_single(obj_id: id) -> Tuple:
    """
    This method will fetch a single
    entry from database.
    :param obj_id: Object ID (Primary Key)
    :return: Tuple of None and ( ValueError or a single item )
    """
    try:
        item = Item.objects.get({"_id": ObjectId(obj_id)})
        return None, item_schema.dump(item)
    except Item.DoesNotExist:
        return ValueError(ErrorMessage.ENTRY_DOES_NOT_EXISTS
                          .format(ObjectId(obj_id))), None
