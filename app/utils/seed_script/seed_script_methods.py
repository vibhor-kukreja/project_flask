"""This file contains code to run seed script"""
import json
import os
from werkzeug.security import generate_password_hash

from app import app, db, logger
from app.auth.models import User
from app.utils.constants import WRITING_SEED_DATA, WRITING_SUCCESSFUL


class SeedClass(object):
    """
    This class contains functions that will run as part of seed script
    Ex - Initializing database and storing some sample data
    """

    @staticmethod
    def init_database() -> None:
        """
        This function will initialize the database and store dummy records
        :return:
        """
        # try to connect to an existing database, otherwise create a new db
        db.engine.connect()
        db.create_all()

        logger.info(WRITING_SEED_DATA.format(User.__tablename__))
        auth_records_to_insert = []
        auth_seed_path = os.path.join(app.root_path, "auth", "seed.json")
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
        logger.info(WRITING_SUCCESSFUL.format(User.__tablename__))


