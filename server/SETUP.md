# Google Cloud Functions Setup Guide - SyntaxMem

Complete guide for setting up a serverless Python backend using Google Cloud Functions with FastAPI for the SyntaxMem coding practice platform.

## Prerequisites
1. **Google Cloud Account** - Free tier gives you plenty for development
2. **Google Cloud CLI** - Command line tool for managing GCP resources
3. **Python 3.8+** - For local development and testing

## Step-by-Step Process

### 1. Google Cloud Project Setup
```bash
# Install Google Cloud CLI (if not installed)
# Visit: https://cloud.google.com/sdk/docs/install

# Login to Google Cloud
gcloud auth login

# Create a new project
gcloud projects create syntaxmem --name="SyntaxMem"

# Set the project as active
gcloud config set project syntaxmem

# Enable required APIs
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable cloudresourcemanager.googleapis.com
```

### 2. Local Project Structure
```
server/
├── functions/              # Individual function directories
│   ├── auth/
│   │   ├── main.py        # Function entry point
│   │   └── requirements.txt
│   ├── snippets/
│   │   ├── main.py
│   │   └── requirements.txt
│   └── leaderboard/
│       ├── main.py
│       └── requirements.txt
├── shared/                 # Shared utilities
│   ├── __init__.py
│   ├── database.py        # MongoDB connection
│   ├── auth_middleware.py # JWT validation
│   ├── masking.py         # Code masking engine
│   └── utils.py
├── deploy.sh              # Deployment script
└── requirements.txt       # Common dependencies
```

### 3. Basic Function Example (FastAPI)
**`server/functions/auth/main.py`**:
```python
import functions_framework
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import json

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://syntaxmem.dev", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

@app.post("/verify")
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token from client"""
    
    token = credentials.credentials
    
    # Verify token logic here
    # ... JWT verification code ...
    
    return {
        "valid": True,
        "user_id": "user123"
    }

@functions_framework.http
def main(request):
    """Cloud Function entry point"""
    return app(request.environ, lambda status, headers: None)
```

### 4. Requirements File
**`server/functions/auth/requirements.txt`**:
```
functions-framework==3.*
fastapi==0.104.*
pymongo==4.*
PyJWT==2.*
python-dotenv==1.*
motor==3.*
```

### 5. Deployment Commands
```bash
# Deploy a single function
gcloud functions deploy verify-token \
    --runtime python311 \
    --trigger-http \
    --allow-unauthenticated \
    --source=./functions/auth \
    --entry-point=main \
    --region=us-central1

# Deploy with environment variables
gcloud functions deploy verify-token \
    --runtime python311 \
    --trigger-http \
    --allow-unauthenticated \
    --source=./functions/auth \
    --entry-point=main \
    --region=us-central1 \
    --set-env-vars MONGODB_URI=your-connection-string

# Deploy all functions (using deploy script)
./deploy.sh
```

### 6. Environment Variables & Secrets
```bash
# Set environment variables for functions
gcloud functions deploy verify-token \
    --set-env-vars MONGODB_URI=mongodb+srv://...,JWT_SECRET=your-secret

# Or use Secret Manager (more secure)
echo "your-mongodb-uri" | gcloud secrets create mongodb-uri --data-file=-

# Access in function
gcloud functions deploy verify-token \
    --set-secrets 'MONGODB_URI=mongodb-uri:latest'
```

## Development Workflow

### 1. Local Testing
```bash
# Install Functions Framework
pip install functions-framework

# Run function locally
functions-framework --target=main --port=8080

# Test with curl
curl -X POST http://localhost:8080/verify \
  -H "Authorization: Bearer your-test-token"
```

### 2. Function URL Structure
After deployment, your functions get URLs like:
```
https://us-central1-syntaxmem.cloudfunctions.net/verify-token
https://us-central1-syntaxmem.cloudfunctions.net/get-snippets
https://us-central1-syntaxmem.cloudfunctions.net/submit-practice
```

## SyntaxMem-Specific Functions

### Functions We'll Need:
1. **`auth-verify`** - Verify JWT tokens
2. **`snippets-official`** - Get official snippets
3. **`snippets-personal`** - Get user's personal snippets
4. **`snippets-mask`** - Generate masked code for practice
5. **`snippets-submit`** - Submit snippets for review
6. **`practice-submit`** - Submit practice attempts
7. **`leaderboard-get`** - Get leaderboard data
8. **`forum-posts`** - Get forum posts
9. **`forum-comments`** - Handle comments and voting
10. **`admin-review`** - Admin review queue

### Shared Services:
- **MongoDB Connection** - Shared across all functions using Motor (async)
- **JWT Middleware** - Token validation
- **Code Masking Engine** - Python/JS token masking with Pygments
- **Similarity Scoring** - Compare user answers with string-similarity
- **CORS Configuration** - Allow syntaxmem.dev domain

## FastAPI Function Template

### Standard Function Structure:
```python
import functions_framework
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from shared.database import get_database
from shared.auth_middleware import verify_token

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://syntaxmem.dev", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/endpoint")
async def my_endpoint(user=Depends(verify_token), db=Depends(get_database)):
    # Function logic here
    return {"message": "success"}

@functions_framework.http
def main(request):
    return app(request.environ, lambda status, headers: None)
```

## Cost Considerations
- **Free Tier**: 2 million requests/month
- **Typical Cost**: $0.0000004 per request + compute time
- **For SyntaxMem**: Likely under $10/month during development
- **Production**: Scales with usage, very cost-effective

## Security Setup
```bash
# Create service account for MongoDB access
gcloud iam service-accounts create syntaxmem-functions

# Store secrets securely
gcloud secrets create jwt-secret --data-file=jwt-secret.txt
gcloud secrets create mongodb-uri --data-file=mongodb-uri.txt

# Grant function access to secrets
gcloud secrets add-iam-policy-binding jwt-secret \
    --member="serviceAccount:syntaxmem-functions@syntaxmem.iam.gserviceaccount.com" \
    --role="roles/secretmanager.secretAccessor"
```

## Domain Configuration
Once deployed, you can map custom domains:
```bash
# Map to syntaxmem.dev subdomain
gcloud functions deploy my-function \
    --trigger-http \
    --allow-unauthenticated

# Then configure DNS:
# api.syntaxmem.dev -> Cloud Function URLs
```

## Deployment Script Example
**`server/deploy.sh`**:
```bash
#!/bin/bash

# Deploy all functions
functions=(
    "auth-verify:auth"
    "snippets-official:snippets" 
    "snippets-personal:snippets"
    "practice-submit:practice"
    "leaderboard-get:leaderboard"
    "forum-posts:forum"
)

for func in "${functions[@]}"; do
    IFS=':' read -r name dir <<< "$func"
    echo "Deploying $name..."
    
    gcloud functions deploy $name \
        --runtime python311 \
        --trigger-http \
        --allow-unauthenticated \
        --source=./functions/$dir \
        --entry-point=main \
        --region=us-central1 \
        --set-secrets 'MONGODB_URI=mongodb-uri:latest,JWT_SECRET=jwt-secret:latest'
done
```

---

**Next Steps**: 
1. Set up Google Cloud project
2. Create shared utilities (database, auth)
3. Implement core functions one by one
4. Test locally before deploying
5. Configure custom domain mapping