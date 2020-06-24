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

To connect with Mongo_DB from terminal
Username: 'user'
Password: 'password'
Connection Database: 'flask_db'

```mongo -u user -p 'password' --authenticationDatabase flask_db```


## Testing
We've used `pytest` framework for testing
```
1.  To run all the tests, go to the parent directory 
    where tests folder is present and run the 
    following command:
        - pytest tests

2. To run a single test case:
        - pytest path/to/test_file.py::ClassName::TestName
            Eg: pytest tests/unittests/auth/test_services.py::TestServices::test_create_user_ok

3. To run a single file of test case:
        - pytest path/to/test_file.py
            Eg: Eg: pytest tests/unittests/auth/test_services.py

```

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

To test, you can simply add these two lines inside any flask app API.
```python
from celery_app.tasks.auth import c_add
c_add.delay(3, 6)
```

###PDF generation
-------------------------------
A binary(`wkhtmltopdf`) needs to be added to generate pdf.

It can be installed from here: https://wkhtmltopdf.org/downloads.html 

Template for the pdf can be added in the pdf directory inside templates. And the same name of the template file can be 
used to referred as the template name while generating the pdf.

Example:

```javascript
@mod_auth.route("/pdf/", methods=["GET"])
@jwt_required
def pdf_test() -> Dict:
    """
       API to test PDF.
       :return: PDF bytes
    """
    template_name = 'welcome'
    user = json.loads(get_jwt_identity())
    pdf = build_pdf(template=template_name, template_data=user)
    return pdf_response(pdf=pdf, name=template_name)
```
## Emailer

A service to send mail Synchronously or Asynchronously.


#####for synchronous:

import the send_mail function from mailer app

```python
from app.custom.emailer import send_mail

# normal send mail utility
send_mail(to="sender@gmail.com", template="template_name", data={'name':'shubham'}) # data is template data

# send mail with attachment
send_mail(to="sender@gmail.com", template="template_name", data={'name':'shubham'}, 
          pdf_name="attachment.pdf", pdf="pdf_byte_string") 
```

#####for Asynchronous

import the send_mail_async from celery_app

```python
from celery_app.tasks.auth import send_mail_async

send_mail_async.delay("sender@gmail.com", "template_name")


send_mail_async.apply_async(args=(["sender@gmail.com", "template_name"]), countdown=10) # countdown in sec
```



