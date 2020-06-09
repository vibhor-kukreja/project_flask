"""This file contains code to run seed script"""
import json
import os
from sqlalchemy.exc import OperationalError

from flask import current_app
from werkzeug.security import generate_password_hash

from app import db, mongodb
from app.auth.models import User
from app.custom.logger import logger
from app.product.models import Item
from app.utils.constants import DisplayMessage


def init_product() -> None:
    """
    This function will initialize the database for products using MongoDB
    :return: None
    """
    mongodb.test_connection(Item)  # to update in future
    logger.info(DisplayMessage.CONNECTION_SUCCESSFUL.format("MongoDB"))
    logger.info(DisplayMessage.WRITING_SEED_DATA.format(Item.__tablename__))
    items_to_insert = []

    # get data from seed file for products
    item_seed_path = \
        os.path.join(current_app.root_path, "product", "seed.json")
    with open(item_seed_path) as seed_data:
        item_seed_data = json.load(seed_data)
        current_items = item_seed_data.get(Item.__tablename__)

    item_count = Item.objects.count()
    # if seed_script is not running for the first time
    if item_count:
        logger.info(
            DisplayMessage.DATA_ALREADY_EXISTS.format(Item.__tablename__))
    else:
        # if seed script is running for the first time, insert records
        for item in current_items:
            item_instance = Item(**item)
            items_to_insert.append(item_instance)

        # Bulk Insert Records
        Item.objects.bulk_create(items_to_insert, full_clean=True)

        logger.info(
            DisplayMessage.WRITING_SUCCESSFUL.format(Item.__tablename__))





def init_auth() -> None:
    """
    This function will insert seed data for auth_user table in PostgreSQL DB
    :return: None
    """
    # TODO: Move this to __init__ file
    try:
        # Connect to an existing postgreSQL database, otherwise create a new db
        db.engine.connect()
    except OperationalError:
        raise IOError(DisplayMessage.CONNECTION_REFUSED)
    logger.info(DisplayMessage.CONNECTION_SUCCESSFUL.format("PostgreSQL"))

    # create models in database if they doesn't exist
    db.create_all()

    logger.info(DisplayMessage.WRITING_SEED_DATA.format(User.__tablename__))
    auth_records_to_insert = []
    auth_seed_path = os.path.join(current_app.root_path, "auth", "seed.json")
    with open(auth_seed_path) as seed_data:
        auth_seed_data = json.load(seed_data)
        auth_records = auth_seed_data.get(User.__tablename__)
        auth_mails = [record['email'] for record in auth_records]

    # TODO: on increasing tables, make this more generic
    # to accept a list, a query object and return unique values
    query = db.session.query(User)
    existing_records_mail = \
        [*query.filter(User.email.in_(auth_mails)).values('email')]
    existing_records_mail = [email[0] for email in existing_records_mail]

    # iterate over records in JSON
    for record in auth_records:
        if record['email'] not in existing_records_mail:
            encrypted_password = generate_password_hash(record['password'])
            record.update({"password": encrypted_password})
            auth_records_to_insert.append(record)

    # bulk insert
    if auth_records_to_insert:
        db.engine.execute(User.__table__.insert(), auth_records_to_insert)
    logger.info(DisplayMessage.WRITING_SUCCESSFUL.format(User.__tablename__))


def execute() -> None:
    """
    Executor for seed script for db
    :return: None
    """
    init_auth()
    init_product()
