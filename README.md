# AI PR Reviewer for PotPie AI

## Project Overview

An automated code review tool built with FastAPI, Celery, and Redis, deployed on Render. The application provides intelligent code review capabilities for GitHub pull requests.

🔗 Frontend Deployment: [https://ai-code-review-fe.vercel.app/](https://ai-code-review-fe.vercel.app/)
🔗 Live API URL :  [https://fastapi-app-y507.onrender.com](https://fastapi-app-y507.onrender.com)

## Tech Stack

- **Backend**: FastAPI
- **Task Queue**: Celery
- **Caching**: Redis
- **AI Model**: Mistral AI
- **Frontend**: Next.js
- **Deployment**: Vercel (Frontend), Render (Backend)

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/kinshuksinghbist/AI_Code_Review_BE.git
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the FastAPI server:
   ```bash
   uvicorn api.app:app --reload
   ```

5. Start the Celery worker (in a separate terminal):
   ```bash
   celery -A api.celery.app worker --loglevel=info
   ```
Known Issues currently
⚠️ In some cases, you may need to retry the same request multiple times to successfully retrieve the review results
This can happen due to  temporary system constraints
If initial request doesn't return results, wait briefly and resubmit the request

## Branches

- `main`: Deployment-ready version (without async Celery)
- `local`: Development branch with full async Celery support

## Design Rationale

- **Next.js**: Chosen for frontend development and easy deployment
- **Redis**: Selected for fast caching and personal experience with redis and redis-cli
- **Mistral AI & Langchain**: Utilized for straightforward AI integration. Also mistral ai is free 
- **Deployment Strategy**: Leveraged Vercel and Render for efficient hosting.

## Key Features

- Automated GitHub PR code reviews
- Asynchronous task processing
- Caching of review results using redis
- Flexible AI-powered analysis

## Documentation

Full API documentation with curl requests is available at `https://fastapi-app-y507.onrender.com/api/docs`


## API Endpoints

### 1. Analyze PR Review
- **Endpoint**: `POST /api/analyze-pr`
- **Purpose**: Submit a PR for code review
- **Request Body**:
  ```json
  {
    "repo_owner": "string",
    "repo_name": "string",
    "pr_number": 123,
    "github_token": "string"
  }
  ```

### 2. Get Review Status
- **Endpoint**: `GET /api/status/{task_id}`
- **Purpose**: Check the status of a code review task

### 3. Get Review Results
- **Endpoint**: `GET /api/results/{task_id}`
- **Purpose**: Retrieve the final results of a code review task

## Future Improvements

- [ ] Define more structured response formats, 
- [ ] Implement more granular AI task segmentati and  go through the git diffs assiging smaller and more precise roles to the ai agent, giving it more powerful tools
- [ ] Add Grafana logging
- [ ] Add async processing for deployment environments

