"""
Snippets Cloud Function for SyntaxMem
Handles code snippet management using Flask
"""

import asyncio
import os
from datetime import datetime
from typing import Any, Dict, List, Optional
from bson import ObjectId

import functions_framework
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from the root of the `server` directory
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

# Create Flask app
app = Flask(__name__)

# Configure CORS with environment-based origins
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:3001,https://syntaxmem.com").split(",")
CORS(app, origins=[origin.strip() for origin in cors_origins], 
     methods=["GET", "POST", "OPTIONS"], allow_headers=["Content-Type", "Authorization"])

# Import utilities
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from shared.auth_middleware import verify_jwt_token_simple
from shared.database import get_official_snippets_collection, get_personal_snippets_collection, get_users_collection
from shared.utils import current_timestamp, generate_id, create_response, create_error_response
from shared.masking import mask_code
from shared.schemas import format_snippet_response, format_pagination_response

# Configure logging
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Response functions are now imported from shared.utils

def validate_pagination_params(page: str, per_page: str) -> tuple[int, int]:
    """Validate and sanitize pagination parameters"""
    try:
        page_num = max(1, int(page or 1))
        per_page_num = max(1, min(100, int(per_page or 20)))  # Limit per_page to 100
        return page_num, per_page_num
    except ValueError:
        return 1, 20

def validate_language(language: str) -> bool:
    """Validate programming language"""
    allowed_languages = ["python", "javascript"]
    return language.lower() in allowed_languages

def validate_difficulty(difficulty: int) -> bool:
    """Validate difficulty level"""
    return 1 <= difficulty <= 10

def sanitize_string(text: str, max_length: int = 255) -> str:
    """Sanitize string input"""
    if not text:
        return ""
    
    # Remove HTML tags and extra whitespace
    import re
    text = re.sub(r'<[^>]+>', '', str(text))
    text = ' '.join(text.split())
    
    # Limit length
    if len(text) > max_length:
        text = text[:max_length]
    
    return text.strip()


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return create_response({"status": "healthy", "service": "snippets"})


@app.route("/official", methods=["GET"])
def get_official_snippets():
    """Get official code snippets"""
    try:
        # Get and validate query parameters
        page, per_page = validate_pagination_params(
            request.args.get('page'), 
            request.args.get('per_page')
        )
        language = request.args.get('language')
        difficulty = request.args.get('difficulty')
        
        # Validate language if provided
        if language and not validate_language(language):
            return create_error_response("Invalid language specified", 400)
        
        # Validate difficulty if provided
        if difficulty:
            try:
                diff_int = int(difficulty)
                if not validate_difficulty(diff_int):
                    return create_error_response("Difficulty must be between 1 and 10", 400)
            except ValueError:
                return create_error_response("Invalid difficulty format", 400)
        
        # Run async logic
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(
                _get_official_snippets_async(page, per_page, language, difficulty)
            )
            return create_response(result, "Official snippets retrieved")
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"Error getting official snippets: {str(e)}")
        return create_error_response("Failed to retrieve official snippets", 500)


async def _get_official_snippets_async(page: int, per_page: int, language: str = None, difficulty: str = None):
    """Async logic for getting official snippets"""
    snippets_collection = await get_official_snippets_collection()
    
    # Build query (no type filter needed - collection determines it's official)
    query = {"status": "active"}  # Only show active snippets
    
    if language:
        query["language"] = language
        
    if difficulty:
        try:
            query["difficulty"] = int(difficulty)
        except ValueError:
            pass  # Ignore invalid difficulty values
    
    # Calculate pagination
    skip = (page - 1) * per_page
    
    # Get snippets
    cursor = snippets_collection.find(query).skip(skip).limit(per_page)
    snippets = await cursor.to_list(length=per_page)
    
    # Get total count
    total = await snippets_collection.count_documents(query)
    
    # Format snippets using shared schema
    formatted_snippets = [
        format_snippet_response(snippet, snippet_type="official", include_content=False)
        for snippet in snippets
    ]
    
    return format_pagination_response(formatted_snippets, page, per_page, total)


@app.route("/personal", methods=["GET"])
def get_personal_snippets():
    """Get user's personal snippets (requires auth)"""
    try:
        # Verify JWT token
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return create_error_response("Authorization token required", 401)
        
        token = auth_header.split(" ")[1]
        user_data = verify_jwt_token_simple(token)
        if not user_data:
            return create_error_response("Invalid or expired token", 401)
        
        user_id = user_data["user_id"]
        
        # Get and validate query parameters
        page, per_page = validate_pagination_params(
            request.args.get('page'), 
            request.args.get('per_page')
        )
        
        # Run async logic
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(
                _get_personal_snippets_async(user_id, page, per_page)
            )
            return create_response(result, "Personal snippets retrieved")
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"Error getting personal snippets: {str(e)}")
        return create_error_response("Failed to retrieve personal snippets", 500)


async def _get_personal_snippets_async(user_id: str, page: int, per_page: int):
    """Async logic for getting personal snippets"""
    snippets_collection = await get_personal_snippets_collection()
    
    # Build query for user's personal snippets (no type filter needed)
    query = {"userId": ObjectId(user_id)}
    
    # Calculate pagination
    skip = (page - 1) * per_page
    
    # Get snippets
    cursor = snippets_collection.find(query).skip(skip).limit(per_page)
    snippets = await cursor.to_list(length=per_page)
    
    # Get total count
    total = await snippets_collection.count_documents(query)
    
    # Format snippets using shared schema
    formatted_snippets = [
        format_snippet_response(snippet, snippet_type="personal", include_content=True)
        for snippet in snippets
    ]
    
    return format_pagination_response(formatted_snippets, page, per_page, total)


@app.route("/create", methods=["POST"])
def create_snippet():
    """Create a new personal snippet (requires auth)"""
    try:
        # Verify JWT token
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return create_error_response("Authorization token required", 401)
        
        token = auth_header.split(" ")[1]
        user_data = verify_jwt_token_simple(token)
        if not user_data:
            return create_error_response("Invalid or expired token", 401)
        
        user_id = user_data["user_id"]
        
        # Get request data
        data = request.get_json()
        if not data:
            return create_error_response("Invalid JSON data", 400)
        
        # Validate required fields
        required_fields = ["title", "language", "code", "difficulty"]
        for field in required_fields:
            if not data.get(field):
                return create_error_response(f"{field} is required", 400)
        
        # Validate field formats
        if not validate_language(data["language"]):
            return create_error_response("Invalid language. Supported: python, javascript", 400)
        
        try:
            difficulty = int(data["difficulty"])
            if not validate_difficulty(difficulty):
                return create_error_response("Difficulty must be between 1 and 10", 400)
        except ValueError:
            return create_error_response("Difficulty must be a number", 400)
        
        # Validate content lengths
        if len(data["title"].strip()) < 3:
            return create_error_response("Title must be at least 3 characters", 400)
        if len(data["code"]) < 10:
            return create_error_response("Code must be at least 10 characters", 400)
        if len(data["code"]) > 50000:
            return create_error_response("Code too long (max 50,000 characters)", 400)
        
        # Run async logic
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(
                _create_snippet_async(user_id, data)
            )
            return create_response(result, "Snippet created successfully")
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"Error creating snippet: {e}")
        return create_error_response("Failed to create snippet", 500)


async def _create_snippet_async(user_id: str, data: Dict):
    """Async logic for creating a snippet"""
    snippets_collection = await get_snippets_collection()
    
    # Create new snippet with sanitized data
    snippet_id = generate_id()
    snippet_data = {
        "_id": snippet_id,
        "userId": user_id,
        "type": "personal",
        "title": sanitize_string(data["title"], 100),
        "language": data["language"].strip().lower(),
        "code": data["code"],  # Don't sanitize code as it needs to preserve formatting
        "difficulty": int(data["difficulty"]),
        "description": sanitize_string(data.get("description", ""), 500),
        "authorName": "You",
        "solveCount": 0,
        "avgScore": 0.0,
        "status": "active",
        "createdAt": current_timestamp(),
        "updatedAt": current_timestamp(),
    }
    
    # Save snippet
    await snippets_collection.insert_one(snippet_data)
    
    return {
        "id": snippet_id,
        "title": snippet_data["title"],
        "language": snippet_data["language"],
        "difficulty": snippet_data["difficulty"],
        "created_at": snippet_data["createdAt"].isoformat()
    }


@app.route("/<snippet_id>", methods=["GET"])
def get_snippet_by_id(snippet_id: str):
    """Get specific snippet by ID"""
    try:
        # Verify JWT token
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return create_error_response("Authorization token required", 401)
        
        token = auth_header.split(" ")[1]
        user_data = verify_jwt_token_simple(token)
        if not user_data:
            return create_error_response("Invalid or expired token", 401)
        
        user_id = user_data["user_id"]
        
        # Run async logic
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(_get_snippet_by_id_async(user_id, snippet_id))
            return create_response(result, "Snippet retrieved")
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"Error getting snippet: {e}")
        return create_error_response("Failed to get snippet", 500)


async def _get_snippet_by_id_async(user_id: str, snippet_id: str):
    """Async logic for getting snippet by ID"""
    snippets_collection = await get_snippets_collection()
    
    # Get snippet
    snippet = await snippets_collection.find_one({"_id": snippet_id})
    if not snippet:
        raise Exception("Snippet not found")
    
    # Check access permissions
    if snippet.get("type") == "personal" and snippet.get("userId") != user_id:
        raise Exception("Access denied to this snippet")
    
    # Format snippet response with all required fields
    return {
        "id": str(snippet["_id"]),
        "title": snippet.get("title", "Untitled"),
        "content": snippet.get("code", ""),
        "language": snippet["language"],
        "difficulty": snippet["difficulty"],
        "type": snippet.get("type", "personal"),
        "status": snippet.get("status", "active"),
        "author_name": snippet.get("authorName", "Unknown"),
        "solve_count": snippet.get("solveCount", 0),
        "avg_score": snippet.get("avgScore", 0.0),
        "created_at": snippet.get("createdAt", "").isoformat() if isinstance(snippet.get("createdAt"), datetime) else snippet.get("createdAt", "")
    }


@app.route("/<snippet_id>/mask", methods=["POST"])
def mask_snippet_by_id(snippet_id: str):
    """Generate masked version of a specific snippet for practice"""
    try:
        # Verify JWT token
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return create_error_response("Authorization token required", 401)
        
        token = auth_header.split(" ")[1]
        user_data = verify_jwt_token_simple(token)
        if not user_data:
            return create_error_response("Invalid or expired token", 401)
        
        user_id = user_data["user_id"]
        
        # Get request data for optional difficulty override
        data = request.get_json() or {}
        custom_difficulty = data.get("difficulty")
        
        # Run async logic
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(_mask_snippet_by_id_async(user_id, snippet_id, custom_difficulty))
            return create_response(result, "Snippet masked successfully")
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"Error masking snippet: {e}")
        return create_error_response("Failed to mask snippet", 500)


async def _mask_snippet_by_id_async(user_id: str, snippet_id: str, custom_difficulty: int = None):
    """Async logic for masking a snippet by ID"""
    snippets_collection = await get_snippets_collection()
    
    # Get snippet
    snippet = await snippets_collection.find_one({"_id": snippet_id})
    if not snippet:
        raise Exception("Snippet not found")
    
    # Check if user has access to this snippet
    if snippet.get("type") == "personal" and snippet.get("userId") != user_id:
        raise Exception("Access denied to this snippet")
    
    # Use custom difficulty if provided, otherwise use snippet's difficulty
    difficulty = custom_difficulty if custom_difficulty is not None else snippet["difficulty"]
    
    # Generate masked code
    masked_result = mask_code(snippet["code"], snippet["language"], difficulty)
    
    return {
        "snippet_id": snippet_id,
        "title": snippet.get("title", "Untitled"),
        "language": snippet["language"],
        "difficulty": difficulty,
        "masked_code": masked_result["masked_code"],
        "answer_count": len(masked_result["blanks"]),
        "type": snippet.get("type", "personal")
    }


@app.route("/submit", methods=["POST"])
def submit_snippet():
    """Submit snippet for review to become official"""
    try:
        # Verify JWT token
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return create_error_response("Authorization token required", 401)
        
        token = auth_header.split(" ")[1]
        user_data = verify_jwt_token_simple(token)
        if not user_data:
            return create_error_response("Invalid or expired token", 401)
        
        user_id = user_data["user_id"]
        
        # Get request data
        data = request.get_json()
        if not data:
            return create_error_response("Invalid JSON data", 400)
        
        # Validate required fields
        required_fields = ["title", "content", "language", "difficulty"]
        for field in required_fields:
            if not data.get(field):
                return create_error_response(f"{field} is required", 400)
        
        # Run async logic
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(_submit_snippet_async(user_id, data))
            return create_response(result, "Snippet submitted for review")
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"Error submitting snippet: {e}")
        return create_error_response("Failed to submit snippet", 500)


async def _submit_snippet_async(user_id: str, data: Dict):
    """Async logic for submitting a snippet for review"""
    snippets_collection = await get_snippets_collection()
    users_collection = await get_users_collection()
    
    # Get user info for author name
    user = await users_collection.find_one({"_id": user_id})
    author_name = user.get("name", "Anonymous") if user else "Anonymous"
    
    # Create submission record
    submission_id = generate_id()
    submission_data = {
        "_id": submission_id,
        "userId": user_id,
        "authorName": author_name,
        "type": "submission",
        "status": "pending",
        "title": data["title"].strip(),
        "language": data["language"].strip().lower(),
        "code": data["content"],
        "difficulty": int(data["difficulty"]),
        "description": data.get("description", "").strip(),
        "submittedAt": current_timestamp(),
        "reviewNotes": "",
        "reviewedAt": None
    }
    
    # Save submission
    await snippets_collection.insert_one(submission_data)
    
    return {
        "id": submission_id,
        "title": submission_data["title"],
        "language": submission_data["language"],
        "difficulty": submission_data["difficulty"],
        "status": submission_data["status"],
        "submitted_at": submission_data["submittedAt"].isoformat(),
        "reviewed_at": None,
        "review_notes": None
    }


@app.route("/submissions", methods=["GET"])
def get_submissions():
    """Get user's snippet submissions"""
    try:
        # Verify JWT token
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return create_error_response("Authorization token required", 401)
        
        token = auth_header.split(" ")[1]
        user_data = verify_jwt_token_simple(token)
        if not user_data:
            return create_error_response("Invalid or expired token", 401)
        
        user_id = user_data["user_id"]
        
        # Run async logic
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(_get_submissions_async(user_id))
            return create_response(result, "Submissions retrieved")
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"Error getting submissions: {e}")
        return create_error_response("Failed to get submissions", 500)


async def _get_submissions_async(user_id: str):
    """Async logic for getting user submissions"""
    snippets_collection = await get_snippets_collection()
    
    # Get user's submissions
    cursor = snippets_collection.find({"type": "submission", "userId": user_id})
    submissions = await cursor.to_list(length=None)
    
    # Format submissions
    formatted_submissions = []
    for submission in submissions:
        formatted_submission = {
            "id": str(submission["_id"]),
            "title": submission.get("title", "Untitled"),
            "language": submission["language"],
            "difficulty": submission["difficulty"],
            "status": submission.get("status", "pending"),
            "submitted_at": submission.get("submittedAt", "").isoformat() if isinstance(submission.get("submittedAt"), datetime) else submission.get("submittedAt", ""),
            "reviewed_at": submission.get("reviewedAt", "").isoformat() if isinstance(submission.get("reviewedAt"), datetime) else submission.get("reviewedAt"),
            "review_notes": submission.get("reviewNotes", "")
        }
        formatted_submissions.append(formatted_submission)
    
    return {"submissions": formatted_submissions}


@app.route("/mask", methods=["POST"])
def mask_snippet():
    """Legacy endpoint - Generate masked version of a snippet for practice"""
    try:
        # Verify JWT token
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return create_error_response("Authorization token required", 401)
        
        token = auth_header.split(" ")[1]
        user_data = verify_jwt_token_simple(token)
        if not user_data:
            return create_error_response("Invalid or expired token", 401)
        
        user_id = user_data["user_id"]
        
        # Get request data
        data = request.get_json()
        if not data:
            return create_error_response("Invalid JSON data", 400)
        
        snippet_id = data.get("snippet_id")
        if not snippet_id:
            return create_error_response("snippet_id is required", 400)
        
        # Run async logic
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(_mask_snippet_async(user_id, snippet_id))
            return create_response(result, "Snippet masked successfully")
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"Error masking snippet: {e}")
        return create_error_response("Failed to mask snippet", 500)


async def _mask_snippet_async(user_id: str, snippet_id: str):
    """Async logic for masking a snippet"""
    snippets_collection = await get_snippets_collection()
    
    # Get snippet
    snippet = await snippets_collection.find_one({"_id": snippet_id})
    if not snippet:
        raise Exception("Snippet not found")
    
    # Check if user has access to this snippet
    if snippet.get("type") == "personal" and snippet.get("userId") != user_id:
        raise Exception("Access denied to this snippet")
    
    # Generate masked code
    masked_result = mask_code(snippet["code"], snippet["language"], snippet["difficulty"])
    
    return {
        "snippet_id": snippet_id,
        "original_code": snippet["code"],
        "masked_code": masked_result["masked_code"],
        "blanks": masked_result["blanks"],
        "snippet_info": {
            "title": snippet.get("title", "Untitled"),
            "language": snippet["language"],
            "difficulty": snippet["difficulty"],
            "description": snippet.get("description", "")
        }
    }


@functions_framework.http
def main(request):
    """Cloud Function entry point"""
    with app.request_context(request.environ):
        return app.full_dispatch_request()