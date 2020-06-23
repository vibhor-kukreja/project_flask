import json
from typing import Tuple, Dict, AnyStr

from app.product.constants import ErrorMessage
from app.product.models import Item, item_schema, items_schema
from bson.objectid import ObjectId


def _make_filter_dict(filter_dict: dict) -> Dict:
    """
    This private method will add an extra '$' to
    the keys in the dict to make raw query for MongoDB.
    :param filter_dict: Dictionary of filters
    :return: Formatted dictionary of filters
    """
    return {f'${key}': val for (key, val) in filter_dict.items()}


def _value_converter(value: AnyStr) -> Dict or AnyStr:
    """
    Converts the value of the key
    into a JSON or a normal string.
    :param value: String
    :return: JSON or String
    """
    try:
        return json.loads(value)
    except ValueError:
        return str(value)


def _query_maker(filters: dict) -> Dict:
    """
    This private method will create raw queries
    to fetch data accordingly.
    :param filters: Receives a multidict with filters
    :return: A dictionary with a MongoDB query
    """
    query_list = list()
    filters = filters.to_dict()

    for key in Item.filter_list:
        if key in filters.keys():
            filter_value = _value_converter(filters.get(key))
            if type(filter_value) is dict:
                query_list.append({key: _make_filter_dict(filter_value)})
            else:
                query_list.append({key: filter_value})
    return {
        "$and": query_list
    }


def fetch_all(filters=None) -> Tuple:
    """
    This method will fetch all
    the entries from database.
    :param: filters: Raw query filters
    :return: Tuple of None and ( ValueError or List of Items )
    """
    if filters:
        query = _query_maker(filters)
        items = Item.objects.raw(query).all()
        return None, items_schema.dump(items)

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
