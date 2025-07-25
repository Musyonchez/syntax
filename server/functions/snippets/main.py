"""
Snippets Cloud Function for SyntaxMem
Handles code snippet management using Flask
"""

import asyncio
import json
from datetime import datetime
from typing import Any, Dict, List, Optional

import functions_framework
from flask import Flask, jsonify, request
from flask_cors import CORS

# Create Flask app
app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "http://localhost:3001", "https://syntaxmem.com"], 
     methods=["GET", "POST", "OPTIONS"], headers=["Content-Type", "Authorization"])

import os
from dotenv import load_dotenv

# Load environment variables from the root of the `server` directory
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

# Import utilities
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from shared.auth_middleware import verify_jwt_token_simple
from shared.database import get_snippets_collection, get_users_collection
from shared.utils import current_timestamp, generate_id
from shared.masking import mask_code


def create_response(data=None, message="Success", status=200):
    """Create standardized response"""
    response = {"success": status < 400, "message": message, "data": data or {}}
    return jsonify(response), status


def create_error_response(message="Error", status=400):
    """Create standardized error response"""
    return create_response(data=None, message=message, status=status)


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return create_response({"status": "healthy", "service": "snippets"})


@app.route("/official", methods=["GET"])
def get_official_snippets():
    """Get official code snippets"""
    try:
        # Get query parameters
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        language = request.args.get('language')
        difficulty = request.args.get('difficulty')
        
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
        print(f"Error getting official snippets: {e}")
        return create_error_response(f"Failed to get snippets: {str(e)}", 500)


async def _get_official_snippets_async(page: int, per_page: int, language: str = None, difficulty: str = None):
    """Async logic for getting official snippets"""
    snippets_collection = await get_snippets_collection()
    
    # Build query
    query = {"type": "official"}
    
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
    
    # Format snippets for response (remove sensitive data)
    formatted_snippets = []
    for snippet in snippets:
        formatted_snippet = {
            "id": str(snippet["_id"]),
            "title": snippet.get("title", "Untitled"),
            "language": snippet["language"],
            "difficulty": snippet["difficulty"],
            "description": snippet.get("description", ""),
            "tags": snippet.get("tags", []),
            "created_at": snippet.get("createdAt", "").isoformat() if isinstance(snippet.get("createdAt"), datetime) else snippet.get("createdAt", ""),
            # Don't include the actual code or solutions for security
        }
        formatted_snippets.append(formatted_snippet)
    
    return {
        "snippets": formatted_snippets,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": total,
            "pages": (total + per_page - 1) // per_page
        }
    }


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
        
        # Get query parameters
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        
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
        print(f"Error getting personal snippets: {e}")
        return create_error_response(f"Failed to get personal snippets: {str(e)}", 500)


async def _get_personal_snippets_async(user_id: str, page: int, per_page: int):
    """Async logic for getting personal snippets"""
    snippets_collection = await get_snippets_collection()
    
    # Build query for user's personal snippets
    query = {"type": "personal", "userId": user_id}
    
    # Calculate pagination
    skip = (page - 1) * per_page
    
    # Get snippets
    cursor = snippets_collection.find(query).skip(skip).limit(per_page)
    snippets = await cursor.to_list(length=per_page)
    
    # Get total count
    total = await snippets_collection.count_documents(query)
    
    # Format snippets for response
    formatted_snippets = []
    for snippet in snippets:
        formatted_snippet = {
            "id": str(snippet["_id"]),
            "title": snippet.get("title", "Untitled"),
            "language": snippet["language"],
            "difficulty": snippet["difficulty"],
            "description": snippet.get("description", ""),
            "tags": snippet.get("tags", []),
            "created_at": snippet.get("createdAt", "").isoformat() if isinstance(snippet.get("createdAt"), datetime) else snippet.get("createdAt", ""),
            "code": snippet.get("code", ""),  # Include code for personal snippets
        }
        formatted_snippets.append(formatted_snippet)
    
    return {
        "snippets": formatted_snippets,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": total,
            "pages": (total + per_page - 1) // per_page
        }
    }


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
        print(f"Error creating snippet: {e}")
        return create_error_response(f"Failed to create snippet: {str(e)}", 500)


async def _create_snippet_async(user_id: str, data: Dict):
    """Async logic for creating a snippet"""
    snippets_collection = await get_snippets_collection()
    
    # Create new snippet
    snippet_id = generate_id()
    snippet_data = {
        "_id": snippet_id,
        "userId": user_id,
        "type": "personal",
        "title": data["title"].strip(),
        "language": data["language"].strip().lower(),
        "code": data["code"],
        "difficulty": int(data["difficulty"]),
        "description": data.get("description", "").strip(),
        "tags": data.get("tags", []),
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


@app.route("/mask", methods=["POST"])
def mask_snippet():
    """Generate masked version of a snippet for practice"""
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
        print(f"Error masking snippet: {e}")
        return create_error_response(f"Failed to mask snippet: {str(e)}", 500)


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