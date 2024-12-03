from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from api.tasks import process_code_review, add_the_nums
import redis 
import uuid
import os

os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')


### Create FastAPI instance with custom docs and openapi url
app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json")
REDIS_HOST = "localhost"  
REDIS_PORT = 6379         
REDIS_DB = 0   

redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

@app.get("/api/helloFastApi")
def hello_fast_api():
    return {"message": "Hello from FastAPI"}

class PRReviewRequest(BaseModel):
    repo_owner: str
    repo_name: str
    pr_number: int
    github_token: str

@app.post("/review-pr")
async def submit_pr_review(request: PRReviewRequest):

    task_id = str(uuid.uuid4())
    
    existing_review_key = f"pr_review:{request.repo_owner}/{request.repo_name}:{request.pr_number}"
    existing_review = redis_client.get(existing_review_key)
    
    if existing_review:
        return {
            "task_id": task_id,
            "status": "cached",
            "review": existing_review.decode('utf-8')
        }
    
    task2 = add_the_nums.delay(3,2)
    
    # task = process_code_review.delay(
    #     repo_owner=request.repo_owner,
    #     repo_name=request.repo_name,
    #     pr_number=request.pr_number,
    #     github_token=request.github_token,
    #     task_id=task_id
    # )
    
    print(task2)
    return {
        "task_id": task_id,
        "status": "pending"
    }

@app.get("/review-status/{task_id}")
async def get_review_status(task_id: str):

    status_key = f"task_status:{task_id}"
    status = redis_client.hgetall(status_key)
    
    if not status:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {
        "task_id": task_id,
        "status": status.get(b'status', b'unknown').decode('utf-8'),
        "result": status.get(b'result', b'').decode('utf-8') if status.get(b'result') else None
    }
