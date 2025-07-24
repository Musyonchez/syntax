"""
Practice Cloud Function for SyntaxMem
Handles practice session management using Flask
"""

import asyncio
import json
from datetime import datetime
from typing import Any, Dict, Optional

import functions_framework
from flask import Flask, jsonify, request
from flask_cors import CORS

# Create Flask app
app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "https://syntaxmem.com"], methods=["GET", "POST", "OPTIONS"], headers=["Content-Type", "Authorization"])

import os
from dotenv import load_dotenv

# Load environment variables from the root of the `server` directory
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

# Import utilities (we'll create these)
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from shared.auth_middleware import verify_jwt_token_simple
from shared.database import (
    get_practice_sessions_collection,
    get_snippets_collection,
    get_users_collection,
)
from shared.utils import current_timestamp, generate_id


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
        # Get request data
        data = request.get_json()
        if not data:
            return create_error_response("Invalid JSON data", 400)

        snippet_id = data.get("snippet_id")
        if not snippet_id:
            return create_error_response("snippet_id is required", 400)

        # Verify JWT token
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return create_error_response("Authorization token required", 401)

        token = auth_header.split(" ")[1]
        user_data = verify_jwt_token_simple(token)
        if not user_data:
            return create_error_response("Invalid or expired token", 401)

        user_id = user_data["user_id"]

        # Run async logic in new event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(
                _start_practice_session_async(user_id, snippet_id)
            )
            return create_response(result, "Practice session started")
        finally:
            loop.close()

    except Exception as e:
        print(f"Error starting practice session: {e}")
        return create_error_response(f"Failed to start practice session: {str(e)}", 500)


async def _start_practice_session_async(user_id: str, snippet_id: str):
    """Async logic for starting practice session"""
    # Get snippet
    snippets_collection = await get_snippets_collection()
    snippet = await snippets_collection.find_one({"_id": snippet_id})

    if not snippet:
        raise Exception("Snippet not found")

    # Create new practice session
    session_id = generate_id()
    session_data = {
        "_id": session_id,
        "userId": user_id,
        "snippetId": snippet_id,
        "language": snippet["language"],
        "difficulty": snippet["difficulty"],
        "startTime": current_timestamp(),
        "status": "active",
        "maskedCode": snippet.get("maskedCode", ""),
        "originalCode": snippet["code"],
        "answers": {},
        "score": 0,
        "completed": False,
    }

    # Save session
    sessions_collection = await get_practice_sessions_collection()
    await sessions_collection.insert_one(session_data)

    # Return session data (without original code)
    return {
        "session_id": session_id,
        "snippet_id": snippet_id,
        "language": snippet["language"],
        "difficulty": snippet["difficulty"],
        "masked_code": snippet.get("maskedCode", ""),
        "title": snippet.get("title", "Practice Session"),
    }


@app.route("/submit/<session_id>", methods=["POST"])
def submit_practice_session(session_id):
    """Submit practice session answers"""
    try:
        # Get request data
        data = request.get_json()
        if not data:
            return create_error_response("Invalid JSON data", 400)

        answers = data.get("answers", {})

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
            result = loop.run_until_complete(
                _submit_practice_session_async(session_id, user_id, answers)
            )
            return create_response(result, "Practice session submitted")
        finally:
            loop.close()

    except Exception as e:
        print(f"Error submitting practice session: {e}")
        return create_error_response(
            f"Failed to submit practice session: {str(e)}", 500
        )


async def _submit_practice_session_async(session_id: str, user_id: str, answers: Dict):
    """Async logic for submitting practice session"""
    # Get session
    sessions_collection = await get_practice_sessions_collection()
    session = await sessions_collection.find_one({"_id": session_id, "userId": user_id})

    if not session:
        raise Exception("Practice session not found")

    if session.get("completed"):
        raise Exception("Practice session already completed")

    # Calculate score (simple scoring for now)
    total_masks = len(answers)
    correct_answers = 0

    # Get original snippet for comparison
    snippets_collection = await get_snippets_collection()
    snippet = await snippets_collection.find_one({"_id": session["snippetId"]})

    if snippet and snippet.get("solutions"):
        solutions = snippet["solutions"]
        for mask_id, answer in answers.items():
            if (
                mask_id in solutions
                and solutions[mask_id].strip().lower() == answer.strip().lower()
            ):
                correct_answers += 1

    # Calculate final score
    score = (correct_answers / max(total_masks, 1)) * 100 if total_masks > 0 else 0

    # Update session
    end_time = current_timestamp()
    time_spent = int((end_time - session["startTime"]).total_seconds())

    await sessions_collection.update_one(
        {"_id": session_id},
        {
            "$set": {
                "answers": answers,
                "score": score,
                "completed": True,
                "endTime": end_time,
                "timeSpent": time_spent,
                "correctAnswers": correct_answers,
                "totalQuestions": total_masks,
            }
        },
    )

    return {
        "session_id": session_id,
        "score": score,
        "correct_answers": correct_answers,
        "total_questions": total_masks,
        "time_spent": time_spent,
        "completed": True,
    }


@functions_framework.http
def main(request):
    """Cloud Function entry point"""
    with app.request_context(request.environ):
        return app.full_dispatch_request()

