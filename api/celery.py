# app/celery.py
from celery import Celery
from dotenv import load_dotenv
import os 

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/10")  # Default for local dev


# Configure Celery app
app = Celery(
    'code_review_tasks', 
    broker=REDIS_URL,  
)

from api.tasks import process_code_review  
