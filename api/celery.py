# app/celery.py
from celery import Celery

# Configure Celery app
app = Celery(
    'code_review_tasks',  # Name of the Celery app
    broker='redis://localhost:6379/1',  # Redis broker URL
)

# Import the tasks module
# Make sure Celery can discover the task definitions
# This will make sure that Celery can find the `process_code_review` task.
from api.tasks import process_code_review, add_the_nums  # Update the import path according to your directory structure
