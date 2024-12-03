# app/celery.py
from celery import Celery
from dotenv import load_dotenv
import os 

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_DB = os.getenv("REDIS_DB")


# Configure Celery app
app = Celery(
    'code_review_tasks',  # Name of the Celery app
    broker=f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}',  # Redis broker URL
)

from api.tasks import process_code_review  
