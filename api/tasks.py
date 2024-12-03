from celery import Celery
from api.services.github_services import fetch_pr_details
from api.agents.code_review_agent import CodeReviewAgent
from dotenv import load_dotenv
import os
import redis
import json
from datetime import datetime

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/10")  # Default for local dev

app = Celery('code_review_tasks', broker=REDIS_URL)

redis_client = redis.StrictRedis.from_url(REDIS_URL, decode_responses=True)


@app.task
def process_code_review(repo_owner, repo_name, pr_number, github_token, task_id):
    try:
        status_key = f"task_status:{task_id}"
        redis_client.hmset(status_key, {
            "status": "processing",
            "started_at": datetime.now().isoformat()
        })
        
        pr_details = fetch_pr_details(
            repo_owner, 
            repo_name, 
            pr_number, 
            github_token
        )

        review_agent = CodeReviewAgent()
        print("here1")
        review_result = review_agent.analyze_pull_request(pr_details)
        print(review_result)
        review_key = f"pr_review:{repo_owner}/{repo_name}:{pr_number}"
        redis_client.set(review_key, str(review_result), ex=86400)  # 24-hour expiry
        
        redis_client.hmset(status_key, {
            "status": "completed",
            "result": str(f"TASK_ID:{task_id}" + review_result),
            "completed_at": datetime.now().isoformat()
        })
        
        return review_result
    
    except Exception as e:
        redis_client.hmset(status_key, {
            "status": "failed",
            "error": str(e),
            "failed_at": datetime.now().isoformat()
        })
        raise

