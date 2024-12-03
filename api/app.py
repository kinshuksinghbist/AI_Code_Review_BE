import uuid
import os
import json

from dotenv import load_dotenv
import redis
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from api.tasks import process_code_review

app = FastAPI(docs_url="/api/docs")

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_DB = os.getenv("REDIS_DB")

redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

class PRReviewRequest(BaseModel):
    repo_owner: str
    repo_name: str
    pr_number: int
    github_token: str

@app.post("/api/analyze-pr")
async def submit_pr_review(request: PRReviewRequest):
    print(REDIS_HOST,REDIS_PORT,REDIS_DB)
    task_id = str(uuid.uuid4())
    
    existing_review_key = f"pr_review:{request.repo_owner}/{request.repo_name}:{request.pr_number}"
    existing_review = redis_client.get(existing_review_key)
    
    if existing_review:
        return {
            "task_id": task_id,
            "status": "cached",
            "review": existing_review
        }

    task = process_code_review.delay(
        repo_owner=request.repo_owner,
        repo_name=request.repo_name,
        pr_number=request.pr_number,
        github_token=request.github_token,
        task_id=task_id
    )

    return {
        "task_id": task_id,
        "status": "pending"
    }

@app.get("/status/{task_id}")
async def get_review_status(task_id: str):
    status_key = f"task_status:{task_id}"
    status = redis_client.hgetall(status_key) 

    if not status:
        raise HTTPException(status_code=404, detail="Task not found")

    return {
        "task_id": task_id,
        "status": status.get('status', 'unknown'), 
        "result": json.loads(status.get('result', None))  
    }

@app.get("/api/results/{task_id}")
async def get_review_status1(task_id: str):
    status_key = f"task_status:{task_id}"
    status = redis_client.hgetall(status_key) 
    if not status:
        raise HTTPException(status_code=404, detail="Task not found")
   
    return {
        "task_id": task_id,
        "status": status.get('status', 'unknown'), 
        "result": json.loads(status.get('result', None))  
    }
