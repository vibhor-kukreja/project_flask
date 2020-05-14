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