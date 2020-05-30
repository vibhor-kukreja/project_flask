# project_flask

```pip install -r requirements.txt```

To run the application:
```python run.py```

#### Logger In Application
```
Application uses an in-built logger system
which handles the logs generated in the application.
A log file for each day is maintained for a week.
``` 
```
Suppose you want to use it in form validation during signin
for logging wrong email or password.

 - from app import app

Use this line at appropriate place under signin method

 - app.logger.error("Wrong email or password")
```






## Using Response

In any part of the project, import success or failure from app

```from app import success, failure```

Usage:

Success

```return success(data=<YOUR_VALUE>)```

Failure/Error

```return failure(message=<YOUR_VALUE>)```


## Environments

To setup environments create a file with the environment name.
Example: `local.env`
```.env
DEBUG = True

# Define the database - we are working with
# url format: "postgresql://<username>:<password>@host:port/<db_name>"
# same as docker-compose
SQLALCHEMY_DATABASE_URI = "postgresql://postgres:password@localhost:5432/flask_db"
# sqlite db uri
# SQLALCHEMY_DATABASE_URI = "sqlite:///${HOME}/Desktop/app.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False
DATABASE_CONNECT_OPTIONS = {}

THREADS_PER_PAGE = 2
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "M0n3Y_H3!5T"
SECRET_KEY = "M0n3Y_H3!5T"
JWT_SECRET_KEY = "M0n3Y_H3!5T"

AUTH_TOKEN_TTL_MINUTES = 60

# Hooks
HOOKS_REQUIRED = True

# Logs
LOG_LEVEL = 'DEBUG'
LOG_FILE_PATH = "app/logger/logs"

# Celery
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_SEND_TASK_SENT_EVENT = True

```

Now, set the `FLASK_ENV` as `local` to use the `local.env` configuration.


## Docker-Compose Instructions
To setup and run in detached mode before launching application:

```docker-compose up -d```

Installing PostgreSQL CLI Client

```sudo apt-get install postgresql-client```

To connect with postgreSQL using PSQL at terminal
Username: 'postgres'
Password: 'password'

```psql -h localhost -p 5432 -U postgres -W```


# Celery

Create multiple worker for you app, that can distribute the task load
```javascript
celery worker -A celery_worker.celery --loglevel=debug -n Tokyo
celery worker -A celery_worker.celery --loglevel=debug -n Berlin
celery worker -A celery_worker.celery --loglevel=debug -n Nairobi
celery worker -A celery_worker.celery --loglevel=debug -n Rio
```

Start a flower server to monitor your tasks
```javascript
celery -A celery_worker.celery flower
```

To test
```python
from celery_app.tasks.auth import c_add
c_add.delay(3, 6)
```


Getting Up and Running Locally With Docker
==========================================

.. index:: Docker

The steps below will get you up and running with a local development environment.
All of these commands assume you are in the root of your generated project.

Prerequisites
-------------

* Docker; if you don't have it yet, follow the `installation instructions`_;
* Docker Compose; refer to the official documentation for the `installation guide`_.

.. _`installation instructions`: https://docs.docker.com/install/#supported-platforms
.. _`installation guide`: https://docs.docker.com/compose/install/


Build the Stack
---------------

This can take a while, especially the first time you run this particular command on your development system::

    $ docker-compose build


Run the Stack
-------------

This brings up both Flask, Redis, Celery and PostgreSQL. The first time it is run it might take a while to get started, but subsequent runs will occur quickly.

Open a terminal at the project root and run the following for local development::

    $ docker-compose up

To run in a detached (background) mode, just::

    $ docker-compose up -d


Execute Management Commands
---------------------------

As with any shell command that we wish to run in our container, this is done using the ``docker-compose run --rm`` command: ::

    $ docker-compose run --rm flask_app flask shell


.. _envs:

Configuring the Environment
---------------------------

This is the excerpt from your project's ``docker-compose.yml``: ::

  # ...

  postgres_db:
    build:
      context: .
      dockerfile: ./compose/postgres_db/Dockerfile
    restart: always
    env_file: 
      - ./.envs/.local/.postgres_db
    volumes:
      - local_postgres_data:/var/lib/postgresql/data
      - local_postgres_data_backups:/backups

  # ...

The most important thing for us here now is ``env_file`` section enlisting ``./.envs/.local/.postgres_db``. Generally, the stack's behavior is governed by a number of environment variables (`env(s)`, for short) residing in ``envs/``, for instance, this is what we generate for you: ::

    .envs
    ├── .local
    │   ├── .flask_app
    │   └── .postgres_db
    └── .production
        ├── .flask_app
        └── .postgres_db

PostgreSQL Backups with Docker
==============================

.. note:: For brevity it is assumed that you will be running the below commands against local environment, however, this is by no means mandatory so feel free to switch to ``production.yml`` when needed.


Prerequisites
-------------

#. the stack is up and running: ``docker-compose up -d postgres_db``.


Creating a Backup
-----------------

To create a backup, run::

    $ docker-compose exec postgres backup

Assuming your project's database is named ``my_project`` here is what you will see: ::

    Backing up the 'flask_db' database...
    SUCCESS: 'flask_db' database backup 'backup_2020_05_30T08_47_11.sql.gz' has been created and placed in '/backups'.

Keep in mind that ``/backups`` is the ``postgres_db`` container directory.


Viewing the Existing Backups
----------------------------

To list existing backups, ::

    $ docker-compose exec postgres_db backups

These are the sample contents of ``/backups``: ::

    These are the backups you have got:
    total 4.0K
    -rw-r--r-- 1 root root 1.2K May 30 08:47 backup_2020_05_30T08_47_11.sql.gz


Copying Backups Locally
-----------------------

If you want to copy backups from your ``postgres_db`` container locally, ``docker cp`` command_ will help you on that.

For example, given ``9c5c3f055843`` is the container ID copying all the backups over to a local directory is as simple as ::

    $ docker cp 9c5c3f055843:/backups ./backups

With a single backup file copied to ``.`` that would be ::

    $ docker cp 9c5c3f055843:/backups/backup_2020_05_30T08_47_11.sql.gz .

.. _`command`: https://docs.docker.com/engine/reference/commandline/cp/


Restoring from the Existing Backup
----------------------------------

To restore from one of the backups you have already got (take the ``backup_2020_05_30T08_47_11.sql.gz`` for example), ::

    $ docker-compose exec postgres restore backup_2020_05_30T08_47_11.sql.gz

You will see something like ::

    Restoring the 'my_project' database from the '/backups/backup_2018_03_13T09_05_07.sql.gz' backup...
    INFO: Dropping the database...
    INFO: Creating a new database...
    INFO: Applying the backup to the new database...
    SET
    SET
    SET
    SET
    SET
     set_config
    ------------

    (1 row)

    SET
    # ...
    ALTER TABLE
    SUCCESS: The 'my_project' database has been restored from the '/backups/backup_2020_05_30T08_47_11.sql.gz' backup.