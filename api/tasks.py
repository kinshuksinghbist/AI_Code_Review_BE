from celery import Celery
from api.services.github_services import fetch_pr_details
from api.agents.code_review_agent import CodeReviewAgent
from dotenv import load_dotenv
import os
import redis
import json
from datetime import datetime

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_DB = os.getenv("REDIS_DB")

redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

app = Celery('code_review_tasks', broker=f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}')


@app.task
def process_code_review(repo_owner, repo_name, pr_number, github_token, task_id):
    try:
        # Update task status to processing
        status_key = f"task_status:{task_id}"
        redis_client.hmset(status_key, {
            "status": "processing",
            "started_at": datetime.now().isoformat()
        })
        
        # Fetch PR details
        pr_details = fetch_pr_details(
            repo_owner, 
            repo_name, 
            pr_number, 
            github_token
        )

        # Initialize CodeReview Agent
        review_agent = CodeReviewAgent()
        print("here1")
        # Generate Code Review
        review_result = review_agent.analyze_pull_request(pr_details)
        print(review_result)
        # Store review in Redis
        review_key = f"pr_review:{repo_owner}/{repo_name}:{pr_number}"
        redis_client.set(review_key, str(review_result), ex=86400)  # 24-hour expiry
        
        # Update task status
        redis_client.hmset(status_key, {
            "status": "completed",
            "result": str(review_result),
            "completed_at": datetime.now().isoformat()
        })
        
        return review_result
    
    except Exception as e:
        # Handle and log errors
        redis_client.hmset(status_key, {
            "status": "failed",
            "error": str(e),
            "failed_at": datetime.now().isoformat()
        })
        raise
