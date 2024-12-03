from celery import Celery
from api.services.github_services import fetch_pr_details
from api.services.review_services import generate_code_review
from api.agents.code_review_agent import CodeReviewAgent
import redis
REDIS_HOST = "localhost"  
REDIS_PORT = 6379         
REDIS_DB = 0   

redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

app = Celery('code_review_tasks', broker='redis://localhost:6379/1')

@app.task
def add_the_nums(x,y):
    return x + y

@app.task
def process_code_review(repo_owner, repo_name, pr_number, github_token, task_id):
    try:
        # Update task status to processing
        status_key = f"task_status:{task_id}"
        print("Idhar tak aa gya")
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
        
        # Generate Code Review
        review_result = review_agent.analyze_pull_request(pr_details)
        
        # Store review in Redis
        review_key = f"pr_review:{repo_owner}/{repo_name}:{pr_number}"
        redis_client.set(review_key, json.dumps(review_result), ex=86400)  # 24-hour expiry
        
        # Update task status
        redis_client.hmset(status_key, {
            "status": "completed",
            "result": json.dumps(review_result),
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

