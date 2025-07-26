"""
Practice Cloud Function for SyntaxMem
Handles practice sessions and scoring using Flask
"""

import asyncio
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

import functions_framework
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

# Create Flask app
app = Flask(__name__)

# Configure CORS with environment-based origins
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:3001,https://syntaxmem.com").split(",")
CORS(app, origins=[origin.strip() for origin in cors_origins], 
     methods=["GET", "POST", "PUT", "OPTIONS"], headers=["Content-Type", "Authorization"])

# Import utilities
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from shared.auth_middleware import verify_jwt_token_simple
from shared.database import get_practice_sessions_collection, get_snippets_collection, get_users_collection
from shared.utils import current_timestamp, generate_id, create_response, create_error_response
from shared.masking import mask_code

# Configure logging
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Response functions now imported from shared.utils


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
        custom_difficulty = data.get("difficulty")
        
        if not snippet_id:
            return create_error_response("snippet_id is required", 400)
        
        # Run async logic
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(_start_practice_async(user_id, snippet_id, custom_difficulty))
            return create_response(result, "Practice session started")
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"Error starting practice session: {str(e)}")
        return create_error_response("Failed to start practice session", 500)


async def _start_practice_async(user_id: str, snippet_id: str, custom_difficulty: int = None):
    """Async logic for starting practice session"""
    # Get collections
    snippets_collection = await get_snippets_collection()
    practice_collection = await get_practice_sessions_collection()
    
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
    
    # Create practice session
    session_id = generate_id()
    practice_session = {
        "_id": session_id,
        "userId": user_id,
        "snippetId": snippet_id,
        "snippetTitle": snippet.get("title", "Untitled"),
        "snippetType": snippet.get("type", "official"),
        "language": snippet["language"],
        "difficulty": difficulty,
        "originalCode": snippet["code"],
        "maskedCode": masked_result["masked_code"],
        "blanks": masked_result["blanks"],
        "userAnswers": [],
        "totalScore": 0,
        "timeSpent": 0,
        "status": "active",
        "startedAt": current_timestamp(),
        "completedAt": None
    }
    
    await practice_collection.insert_one(practice_session)
    
    # Return data in format expected by client
    return {
        "session_id": session_id,
        "snippet_id": snippet_id,
        "snippet_title": snippet.get("title", "Untitled"),
        "language": snippet["language"],
        "difficulty": difficulty,
        "masked_code": masked_result["masked_code"],
        "answer_count": len(masked_result["blanks"]),
        "max_time": 300,  # 5 minutes default
        "created_at": practice_session["startedAt"].isoformat()
    }


@app.route("/submit", methods=["POST"])
def submit_practice_session():
    """Submit complete practice session for scoring"""
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
        user_answers = data.get("user_answers", [])
        time_taken = data.get("time_taken", 0)
        
        if not session_id:
            return create_error_response("session_id is required", 400)
        
        # Run async logic
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(_submit_session_async(user_id, session_id, user_answers, time_taken))
            return create_response(result, "Practice session submitted")
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"Error submitting practice session: {str(e)}")
        return create_error_response("Failed to submit practice session", 500)


async def _submit_session_async(user_id: str, session_id: str, user_answers: List[str], time_taken: int):
    """Async logic for submitting complete practice session"""
    practice_collection = await get_practice_sessions_collection()
    users_collection = await get_users_collection()
    
    # Get practice session
    session = await practice_collection.find_one({"_id": session_id, "userId": user_id})
    if not session:
        raise Exception("Practice session not found")
    
    if session["status"] != "active":
        raise Exception("Practice session is not active")
    
    # Calculate detailed results
    detailed_results = []
    correct_count = 0
    total_blanks = len(session["blanks"])
    
    for i, blank in enumerate(session["blanks"]):
        user_answer = user_answers[i] if i < len(user_answers) else ""
        correct_answer = blank.get("correct_answer", "")
        
        # Calculate similarity (simple string comparison for now)
        is_correct = user_answer.strip().lower() == correct_answer.strip().lower()
        similarity = 1.0 if is_correct else 0.0
        
        if is_correct:
            correct_count += 1
        
        detailed_results.append({
            "position": i,
            "user_answer": user_answer,
            "correct_answer": correct_answer,
            "similarity": similarity,
            "is_correct": is_correct
        })
    
    # Calculate scores
    accuracy = (correct_count / total_blanks * 100) if total_blanks > 0 else 0
    base_score = accuracy
    
    # Time bonus: faster completion gives bonus points
    max_time = 300  # 5 minutes
    time_bonus = max(0, (max_time - time_taken) / max_time * 20) if time_taken < max_time else 0
    
    total_score = min(100, base_score + time_bonus)
    mistakes = total_blanks - correct_count
    
    # Check if eligible for leaderboard (official snippets only, >80% accuracy)
    leaderboard_eligible = (
        session.get("snippetType") == "official" and 
        accuracy >= 80 and 
        mistakes <= 2
    )
    
    # Update practice session
    await practice_collection.update_one(
        {"_id": session_id},
        {
            "$set": {
                "status": "completed",
                "userAnswers": user_answers,
                "totalScore": total_score,
                "accuracy": accuracy,
                "timeSpent": time_taken,
                "mistakes": mistakes,
                "completedAt": current_timestamp()
            }
        }
    )
    
    # Update user stats
    await users_collection.update_one(
        {"_id": user_id},
        {
            "$inc": {
                "stats.totalScore": total_score,
                "stats.practiceTime": time_taken
            },
            "$set": {
                "lastActive": current_timestamp()
            }
        }
    )
    
    # Return score data in expected format
    return {
        "session_id": session_id,
        "total_score": round(total_score, 1),
        "accuracy": round(accuracy, 1),
        "time_bonus": round(time_bonus, 1),
        "mistakes": mistakes,
        "time_taken": time_taken,
        "detailed_results": detailed_results,
        "leaderboard_eligible": leaderboard_eligible
    }


@app.route("/stats", methods=["GET"])
def get_practice_stats():
    """Get user's practice statistics"""
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
            result = loop.run_until_complete(_get_stats_async(user_id))
            return create_response(result, "Practice statistics retrieved")
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"Error getting practice stats: {str(e)}")
        return create_error_response("Failed to get practice statistics", 500)


async def _get_stats_async(user_id: str):
    """Async logic for getting practice statistics"""
    practice_collection = await get_practice_sessions_collection()
    
    # Get all completed sessions
    cursor = practice_collection.find({
        "userId": user_id,
        "status": "completed"
    })
    sessions = await cursor.to_list(length=None)
    
    if not sessions:
        return {
            "total_sessions": 0,
            "average_score": 0,
            "average_accuracy": 0,
            "total_practice_time": 0,
            "total_mistakes": 0,
            "languages": {}
        }
    
    # Calculate overall stats
    total_sessions = len(sessions)
    total_score = sum(s.get("totalScore", 0) for s in sessions)
    total_accuracy = sum(s.get("accuracy", 0) for s in sessions)
    total_practice_time = sum(s.get("timeSpent", 0) for s in sessions)
    total_mistakes = sum(s.get("mistakes", 0) for s in sessions)
    
    # Calculate language-specific stats
    language_stats = {}
    for session in sessions:
        lang = session.get("language", "unknown")
        if lang not in language_stats:
            language_stats[lang] = {
                "sessions": 0,
                "total_score": 0,
                "total_accuracy": 0
            }
        
        language_stats[lang]["sessions"] += 1
        language_stats[lang]["total_score"] += session.get("totalScore", 0)
        language_stats[lang]["total_accuracy"] += session.get("accuracy", 0)
    
    # Calculate averages for each language
    languages = {}
    for lang, stats in language_stats.items():
        languages[lang] = {
            "sessions": stats["sessions"],
            "avg_score": round(stats["total_score"] / stats["sessions"], 1),
            "avg_accuracy": round(stats["total_accuracy"] / stats["sessions"], 1)
        }
    
    return {
        "total_sessions": total_sessions,
        "average_score": round(total_score / total_sessions, 1),
        "average_accuracy": round(total_accuracy / total_sessions, 1),
        "total_practice_time": total_practice_time,
        "total_mistakes": total_mistakes,
        "languages": languages
    }


# Complete endpoint removed - functionality moved to submit endpoint


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
        logger.error(f"Error getting practice session: {str(e)}")
        return create_error_response("Failed to get practice session", 500)


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
        
        # Get query parameters with validation
        try:
            page = max(1, int(request.args.get('page', 1)))
            per_page = max(1, min(50, int(request.args.get('per_page', 20))))
        except ValueError:
            page, per_page = 1, 20
        
        language = request.args.get('language')
        completed_only = request.args.get('completed_only', '').lower() in ('true', '1')
        
        # Run async logic
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(_get_history_async(user_id, page, per_page, language, completed_only))
            return create_response(result, "Practice history retrieved")
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"Error getting practice history: {str(e)}")
        return create_error_response("Failed to get practice history", 500)


async def _get_history_async(user_id: str, page: int, per_page: int, language: str = None, completed_only: bool = False):
    """Async logic for getting practice history"""
    practice_collection = await get_practice_sessions_collection()
    
    # Build query with filters
    query = {"userId": user_id}
    if language:
        query["language"] = language
    if completed_only:
        query["status"] = "completed"
    
    # Calculate skip
    skip = (page - 1) * per_page
    
    # Get sessions
    cursor = practice_collection.find(query).sort("startedAt", -1).skip(skip).limit(per_page)
    sessions = await cursor.to_list(length=per_page)
    
    # Get total count
    total = await practice_collection.count_documents(query)
    
    # Format sessions to match client expectations
    formatted_sessions = []
    for session in sessions:
        formatted_sessions.append({
            "session_id": session["_id"],
            "snippet_id": session["snippetId"],
            "snippet_title": session.get("snippetTitle", "Untitled"),
            "snippet_type": session.get("snippetType", "official"),
            "language": session.get("language", "unknown"),
            "difficulty": session.get("difficulty", 1),
            "completed": session.get("status") == "completed",
            "created_at": session["startedAt"].isoformat() if isinstance(session.get("startedAt"), datetime) else session.get("startedAt", ""),
            "total_score": session.get("totalScore"),
            "accuracy": session.get("accuracy"),
            "time_taken": session.get("timeSpent"),
            "mistakes": session.get("mistakes"),
            "completed_at": session.get("completedAt").isoformat() if isinstance(session.get("completedAt"), datetime) else session.get("completedAt")
        })
    
    return {
        "sessions": formatted_sessions,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total_count": total,
            "total_pages": (total + per_page - 1) // per_page,
            "has_next": page * per_page < total,
            "has_prev": page > 1
        }
    }


@functions_framework.http
def main(request):
    """Cloud Function entry point"""
    with app.request_context(request.environ):
        return app.full_dispatch_request()