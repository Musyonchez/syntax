"""
Auth Cloud Function for SyntaxMem
Handles user authentication using Flask
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
CORS(app, origins=["http://localhost:3000", "http://localhost:3001", "https://syntaxmem.com"], 
     methods=["GET", "POST", "OPTIONS"], headers=["Content-Type", "Authorization"])

import os
from dotenv import load_dotenv

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

# Import utilities
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from shared.auth_middleware import verify_jwt_token_simple, create_jwt_token
from shared.database import get_users_collection
from shared.utils import current_timestamp, generate_id

# Google OAuth imports
import requests
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token


def create_response(data=None, message="Success", status=200):
    """Create standardized response"""
    response = {"success": status < 400, "message": message, "data": data or {}}
    return jsonify(response), status


def create_error_response(message="Error", status=400):
    """Create standardized error response"""
    return create_response(data=None, message=message, status=status)


async def verify_google_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify Google OAuth token and return user info"""
    try:
        # Try to verify as ID token first
        try:
            idinfo = id_token.verify_oauth2_token(
                token,
                google_requests.Request(),
                os.getenv('GOOGLE_CLIENT_ID')
            )
            
            if idinfo and idinfo.get('aud') == os.getenv('GOOGLE_CLIENT_ID'):
                return idinfo
                
        except Exception:
            # If ID token fails, try as access token
            pass
        
        # Fallback: verify as access token using Google's userinfo endpoint
        try:
            response = requests.get(
                'https://www.googleapis.com/oauth2/v1/userinfo',
                headers={'Authorization': f'Bearer {token}'},
                timeout=5
            )
            
            if response.status_code == 200:
                return response.json()
                
        except Exception:
            pass
            
        return None
        
    except Exception:
        return None


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return create_response({"status": "healthy", "service": "auth"})


@app.route("/google-auth", methods=["POST"])
def google_auth():
    """Authenticate user with Google OAuth"""
    try:
        # Get request data
        data = request.get_json()
        if not data:
            return create_error_response("Invalid JSON data", 400)
        
        required_fields = ["google_token", "google_id", "email", "name", "avatar"]
        for field in required_fields:
            if not data.get(field):
                return create_error_response(f"{field} is required", 400)
        
        # Run async logic
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(_google_auth_async(data))
            return create_response(result, "Authentication successful")
        finally:
            loop.close()
            
    except Exception as e:
        print(f"Error during Google auth: {e}")
        return create_error_response(f"Authentication failed: {str(e)}", 500)


async def _google_auth_async(data: Dict):
    """Async logic for Google authentication"""
    print(f"DEBUG: Starting auth for email: {data.get('email', 'unknown')}")
    
    # Verify Google token
    google_user_info = await verify_google_token(data["google_token"])
    print(f"DEBUG: Google token verification result: {google_user_info is not None}")
    
    if not google_user_info:
        raise Exception("Invalid Google token")
    
    # Verify that the token data matches request data
    google_email = google_user_info.get('email')
    google_id = google_user_info.get('sub') or google_user_info.get('id')
    
    if google_email != data["email"]:
        raise Exception("Email mismatch between token and request")
        
    if google_id != data["google_id"]:
        raise Exception("Google ID mismatch between token and request")
    
    # Get database connection
    users_collection = await get_users_collection()
    
    # Sanitize inputs
    clean_google_id = str(data["google_id"]).strip()
    clean_email = str(data["email"]).strip().lower()
    
    # Check if user already exists
    print(f"DEBUG: Checking for existing user with Google ID: {clean_google_id}, Email: {clean_email}")
    existing_user = await users_collection.find_one({
        "$or": [
            {"googleId": clean_google_id},
            {"email": clean_email}
        ]
    })
    
    print(f"DEBUG: Existing user found: {existing_user is not None}")
    current_time = current_timestamp()
    
    if existing_user:
        # Update existing user
        user_id = str(existing_user["_id"])
        
        await users_collection.update_one(
            {"_id": existing_user["_id"]},
            {
                "$set": {
                    "googleId": clean_google_id,
                    "name": str(data["name"]).strip(),
                    "avatar": str(data["avatar"]).strip(),
                    "lastActive": current_time
                }
            }
        )
        
        # Get updated user data
        user = await users_collection.find_one({"_id": existing_user["_id"]})
    else:
        # Create new user
        print("DEBUG: Creating new user")
        user_id = generate_id()
        new_user = {
            "_id": user_id,
            "googleId": clean_google_id,
            "email": clean_email,
            "name": str(data["name"]).strip(),
            "avatar": str(data["avatar"]).strip(),
            "role": "user",
            "preferences": {
                "theme": "dark",
                "languages": ["python"],
                "difficulty": 5
            },
            "stats": {
                "totalScore": 0,
                "practiceTime": 0,
                "streak": 0,
                "level": 1,
                "achievements": []
            },
            "createdAt": current_time,
            "lastActive": current_time
        }
        
        print(f"DEBUG: Inserting new user with ID: {user_id}")
        await users_collection.insert_one(new_user)
        print("DEBUG: User successfully inserted into database")
        user = new_user
    
    # Create JWT token
    token = create_jwt_token(user_id, data["email"])
    
    # Prepare user data for response
    user_data = {
        "user_id": user_id,
        "email": user["email"],
        "name": user["name"],
        "avatar": user["avatar"],
        "role": user["role"],
        "preferences": user["preferences"],
        "stats": user["stats"]
    }
    
    return {
        "token": token,
        "user": user_data,
        "message": "Authentication successful"
    }


@app.route("/verify", methods=["POST"])
def verify_token():
    """Verify JWT token and return user data"""
    try:
        # Get Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return create_error_response("Authorization token required", 401)
        
        token = auth_header.split(" ")[1]
        user_data = verify_jwt_token_simple(token)
        
        if not user_data:
            return create_error_response("Invalid or expired token", 401)
        
        # Run async logic to get full user data
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(_get_user_data_async(user_data["user_id"]))
            return create_response(result, "Token is valid")
        finally:
            loop.close()
            
    except Exception as e:
        print(f"Error verifying token: {e}")
        return create_error_response(f"Token verification failed: {str(e)}", 500)


async def _get_user_data_async(user_id: str):
    """Get full user data from database"""
    users_collection = await get_users_collection()
    user = await users_collection.find_one({"_id": user_id})
    
    if not user:
        raise Exception("User not found")
    
    return {
        "valid": True,
        "user": {
            "user_id": user_id,
            "email": user["email"],
            "name": user["name"],
            "avatar": user["avatar"],
            "role": user["role"],
            "preferences": user["preferences"],
            "stats": user["stats"]
        }
    }


@app.route("/profile", methods=["GET"])
def get_user_profile():
    """Get user profile data"""
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
            result = loop.run_until_complete(_get_user_data_async(user_id))
            return create_response(result["user"], "Profile retrieved")
        finally:
            loop.close()
            
    except Exception as e:
        print(f"Error getting profile: {e}")
        return create_error_response(f"Failed to get profile: {str(e)}", 500)


@app.route("/profile", methods=["PUT"])
def update_user_profile():
    """Update user profile preferences"""
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
        profile_data = request.get_json()
        if not profile_data:
            return create_error_response("Invalid JSON data", 400)
        
        # Run async logic
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(_update_profile_async(user_id, profile_data))
            return create_response(result, "Profile updated successfully")
        finally:
            loop.close()
            
    except Exception as e:
        print(f"Error updating profile: {e}")
        return create_error_response(f"Failed to update profile: {str(e)}", 500)


async def _update_profile_async(user_id: str, profile_data: Dict):
    """Async logic for updating user profile"""
    users_collection = await get_users_collection()
    
    # Validate and sanitize update data
    allowed_updates = {
        "preferences": profile_data.get("preferences", {}),
        "lastActive": current_timestamp()
    }
    
    # Validate preferences
    if "preferences" in allowed_updates:
        prefs = allowed_updates["preferences"]
        if "theme" in prefs and prefs["theme"] not in ["light", "dark"]:
            raise Exception("Invalid theme")
        if "difficulty" in prefs and not (1 <= prefs["difficulty"] <= 10):
            raise Exception("Difficulty must be 1-10")
    
    await users_collection.update_one(
        {"_id": user_id},
        {"$set": allowed_updates}
    )
    
    return {"updated": True}


@functions_framework.http
def main(request):
    """Cloud Function entry point"""
    with app.request_context(request.environ):
        return app.full_dispatch_request()