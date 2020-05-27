"""Run a test server."""
from app import create_app
from celery_app import celery

if __name__ == "__main__":
    # Provided a celery instance for the Flask app to use
    app = create_app(celery=celery)
    app.run(host="0.0.0.0", port=3000, debug=True)
