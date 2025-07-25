"""
Practice Cloud Function for SyntaxMem
Handles practice sessions and scoring using Flask
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
     methods=["GET", "POST", "PUT", "OPTIONS"], headers=["Content-Type", "Authorization"])

import os
from dotenv import load_dotenv

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

# Import utilities
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from shared.auth_middleware import verify_jwt_token_simple
from shared.database import get_practice_sessions_collection, get_snippets_collection, get_users_collection
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
    return create_response({"status": "healthy", "service": "practice"})


@app.route("/start", methods=["POST"])
def start_practice_session():
    """Start a new practice session"""
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
            result = loop.run_until_complete(_start_practice_async(user_id, snippet_id))
            return create_response(result, "Practice session started")
        finally:
            loop.close()
            
    except Exception as e:
        print(f"Error starting practice session: {e}")
        return create_error_response(f"Failed to start practice session: {str(e)}", 500)


async def _start_practice_async(user_id: str, snippet_id: str):
    """Async logic for starting practice session"""
    # Get collections
    snippets_collection = await get_snippets_collection()
    practice_collection = await get_practice_sessions_collection()
    
    # Get snippet
    snippet = await snippets_collection.find_one({"_id": snippet_id})
    if not snippet:
        raise Exception("Snippet not found")
    
    # Check if user has access to this snippet
    if snippet.get("status") != "published" and snippet.get("createdBy") != user_id:
        raise Exception("Access denied to this snippet")
    
    # Generate masked code
    masked_result = mask_code(snippet["code"], snippet["language"], snippet["difficulty"])
    
    # Create practice session
    session_id = generate_id()
    practice_session = {
        "_id": session_id,
        "userId": user_id,
        "snippetId": snippet_id,
        "originalCode": snippet["code"],
        "maskedCode": masked_result["masked_code"],
        "blanks": masked_result["blanks"],
        "userAnswers": {},
        "score": 0,
        "timeSpent": 0,
        "status": "active",
        "startedAt": current_timestamp(),
        "completedAt": None
    }
    
    await practice_collection.insert_one(practice_session)
    
    return {
        "session_id": session_id,
        "snippet": {
            "id": snippet["_id"],
            "title": snippet["title"],
            "language": snippet["language"],
            "difficulty": snippet["difficulty"],
            "description": snippet.get("description", "")
        },
        "masked_code": masked_result["masked_code"],
        "blanks": masked_result["blanks"],
        "total_blanks": len(masked_result["blanks"])
    }


@app.route("/submit", methods=["POST"])
def submit_answer():
    """Submit answer for a practice session"""
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
        
        session_id = data.get("session_id")
        blank_id = data.get("blank_id")
        answer = data.get("answer")
        
        if not all([session_id, blank_id, answer is not None]):
            return create_error_response("session_id, blank_id, and answer are required", 400)
        
        # Run async logic
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(_submit_answer_async(user_id, session_id, blank_id, answer))
            return create_response(result, "Answer submitted")
        finally:
            loop.close()
            
    except Exception as e:
        print(f"Error submitting answer: {e}")
        return create_error_response(f"Failed to submit answer: {str(e)}", 500)


async def _submit_answer_async(user_id: str, session_id: str, blank_id: str, answer: str):
    """Async logic for submitting answer"""
    practice_collection = await get_practice_sessions_collection()
    
    # Get practice session
    session = await practice_collection.find_one({"_id": session_id, "userId": user_id})
    if not session:
        raise Exception("Practice session not found")
    
    if session["status"] != "active":
        raise Exception("Practice session is not active")
    
    # Find the blank
    blank_info = None
    for blank in session["blanks"]:
        if blank["id"] == blank_id:
            blank_info = blank
            break
    
    if not blank_info:
        raise Exception("Blank not found")
    
    # Check answer
    is_correct = answer.strip() == blank_info["correct_answer"].strip()
    
    # Update session with answer
    await practice_collection.update_one(
        {"_id": session_id},
        {
            "$set": {
                f"userAnswers.{blank_id}": {
                    "answer": answer,
                    "is_correct": is_correct,
                    "submitted_at": current_timestamp()
                }
            }
        }
    )
    
    return {
        "blank_id": blank_id,
        "is_correct": is_correct,
        "correct_answer": blank_info["correct_answer"] if not is_correct else None
    }


@app.route("/complete", methods=["POST"])
def complete_practice_session():
    """Complete a practice session and calculate final score"""
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
        
        session_id = data.get("session_id")
        time_spent = data.get("time_spent", 0)
        
        if not session_id:
            return create_error_response("session_id is required", 400)
        
        # Run async logic
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(_complete_session_async(user_id, session_id, time_spent))
            return create_response(result, "Practice session completed")
        finally:
            loop.close()
            
    except Exception as e:
        print(f"Error completing practice session: {e}")
        return create_error_response(f"Failed to complete practice session: {str(e)}", 500)


async def _complete_session_async(user_id: str, session_id: str, time_spent: int):
    """Async logic for completing practice session"""
    practice_collection = await get_practice_sessions_collection()
    users_collection = await get_users_collection()
    
    # Get practice session
    session = await practice_collection.find_one({"_id": session_id, "userId": user_id})
    if not session:
        raise Exception("Practice session not found")
    
    if session["status"] != "active":
        raise Exception("Practice session is not active")
    
    # Calculate score
    total_blanks = len(session["blanks"])
    correct_answers = 0
    
    for blank in session["blanks"]:
        user_answer = session["userAnswers"].get(blank["id"])
        if user_answer and user_answer["is_correct"]:
            correct_answers += 1
    
    # Calculate score (0-100)
    score = int((correct_answers / total_blanks) * 100) if total_blanks > 0 else 0
    
    # Update practice session
    await practice_collection.update_one(
        {"_id": session_id},
        {
            "$set": {
                "status": "completed",
                "score": score,
                "timeSpent": time_spent,
                "completedAt": current_timestamp()
            }
        }
    )
    
    # Update user stats
    await users_collection.update_one(
        {"_id": user_id},
        {
            "$inc": {
                "stats.totalScore": score,
                "stats.practiceTime": time_spent
            },
            "$set": {
                "lastActive": current_timestamp()
            }
        }
    )
    
    return {
        "session_id": session_id,
        "score": score,
        "correct_answers": correct_answers,
        "total_blanks": total_blanks,
        "time_spent": time_spent,
        "accuracy": round((correct_answers / total_blanks) * 100, 1) if total_blanks > 0 else 0
    }


@app.route("/session/<session_id>", methods=["GET"])
def get_practice_session(session_id):
    """Get practice session details"""
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
            result = loop.run_until_complete(_get_session_async(user_id, session_id))
            return create_response(result, "Practice session retrieved")
        finally:
            loop.close()
            
    except Exception as e:
        print(f"Error getting practice session: {e}")
        return create_error_response(f"Failed to get practice session: {str(e)}", 500)


async def _get_session_async(user_id: str, session_id: str):
    """Async logic for getting practice session"""
    practice_collection = await get_practice_sessions_collection()
    
    # Get practice session
    session = await practice_collection.find_one({"_id": session_id, "userId": user_id})
    if not session:
        raise Exception("Practice session not found")
    
    return {
        "session_id": session["_id"],
        "snippet_id": session["snippetId"],
        "masked_code": session["maskedCode"],
        "blanks": session["blanks"],
        "user_answers": session["userAnswers"],
        "score": session["score"],
        "time_spent": session["timeSpent"],
        "status": session["status"],
        "started_at": session["startedAt"],
        "completed_at": session.get("completedAt")
    }


@app.route("/history", methods=["GET"])
def get_practice_history():
    """Get user's practice history"""
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
        per_page = min(int(request.args.get('per_page', 20)), 50)
        
        # Run async logic
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(_get_history_async(user_id, page, per_page))
            return create_response(result, "Practice history retrieved")
        finally:
            loop.close()
            
    except Exception as e:
        print(f"Error getting practice history: {e}")
        return create_error_response(f"Failed to get practice history: {str(e)}", 500)


async def _get_history_async(user_id: str, page: int, per_page: int):
    """Async logic for getting practice history"""
    practice_collection = await get_practice_sessions_collection()
    
    # Calculate skip
    skip = (page - 1) * per_page
    
    # Get sessions
    cursor = practice_collection.find(
        {"userId": user_id}
    ).sort("startedAt", -1).skip(skip).limit(per_page)
    
    sessions = await cursor.to_list(length=per_page)
    
    # Get total count
    total = await practice_collection.count_documents({"userId": user_id})
    
    # Format sessions
    formatted_sessions = []
    for session in sessions:
        formatted_sessions.append({
            "session_id": session["_id"],
            "snippet_id": session["snippetId"],
            "score": session["score"],
            "time_spent": session["timeSpent"],
            "status": session["status"],
            "started_at": session["startedAt"],
            "completed_at": session.get("completedAt")
        })
    
    return {
        "sessions": formatted_sessions,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": total,
            "pages": (total + per_page - 1) // per_page
        }
    }


@functions_framework.http
def main(request):
    """Cloud Function entry point"""
    with app.request_context(request.environ):
        return app.full_dispatch_request()