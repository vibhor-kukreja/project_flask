# project_flask

```pip install -r requirements.txt```

To run the application:
```python run.py```


## Using Response

In any part of the project, import success or failure from app

```from app import success, failure```

Usage:

Success

```return success(data=<YOUR_VALUE>)```

Failure/Error

```return failure(message=<YOUR_VALUE>)```