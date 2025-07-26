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
from shared.utils import current_timestamp, generate_id, create_response, create_error_response
from shared.config import config

# Google OAuth imports
import requests
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token




async def verify_google_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify Google OAuth token and return user info"""
    try:
        print(f"DEBUG: Verifying Google token (length: {len(token)})")
        
        # Try to verify as ID token first (this is what NextAuth sends)
        try:
            print("DEBUG: Attempting ID token verification")
            idinfo = id_token.verify_oauth2_token(
                token,
                google_requests.Request(),
                os.getenv('GOOGLE_CLIENT_ID')
            )
            print(f"DEBUG: ID token verification successful: {idinfo is not None}")
            
            if idinfo and idinfo.get('aud') == os.getenv('GOOGLE_CLIENT_ID'):
                print("DEBUG: ID token audience verified")
                return idinfo
            else:
                print("DEBUG: ID token audience mismatch or invalid")
                
        except Exception as e:
            print(f"DEBUG: ID token verification failed: {str(e)}")
            # If ID token fails, try as access token
            pass
        
        # Fallback: verify as access token using Google's userinfo endpoint
        try:
            print("DEBUG: Attempting access token verification via userinfo endpoint")
            response = requests.get(
                'https://www.googleapis.com/oauth2/v1/userinfo',
                headers={'Authorization': f'Bearer {token}'},
                timeout=3  # Reduced timeout
            )
            print(f"DEBUG: Userinfo endpoint response status: {response.status_code}")
            
            if response.status_code == 200:
                user_info = response.json()
                print(f"DEBUG: Access token verification successful: {user_info.get('email', 'no_email')}")
                return user_info
            else:
                print(f"DEBUG: Access token verification failed with status {response.status_code}")
                
        except Exception as e:
            print(f"DEBUG: Access token verification failed: {str(e)}")
            pass
            
        print("DEBUG: All token verification methods failed")
        return None
        
    except Exception as e:
        print(f"DEBUG: Token verification error: {str(e)}")
        return None


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return create_response({"status": "healthy", "service": "auth"})


@app.route("/google-auth", methods=["POST"])
def google_auth():
    """Authenticate user with Google OAuth"""
    try:
        print("DEBUG: Received google-auth request")
        
        # Get request data
        data = request.get_json()
        if not data:
            print("DEBUG: No JSON data received")
            return create_error_response("Invalid JSON data", 400)
        
        print(f"DEBUG: Request data keys: {list(data.keys())}")
        
        # Check that we have account and profile data
        if not data.get("account") or not data.get("profile"):
            print(f"DEBUG: Missing required data - account: {data.get('account') is not None}, profile: {data.get('profile') is not None}")
            return create_error_response("Account and profile data required", 400)
        
        account = data["account"]
        profile = data["profile"]
        
        print(f"DEBUG: Account keys: {list(account.keys()) if account else 'None'}")
        print(f"DEBUG: Profile keys: {list(profile.keys()) if profile else 'None'}")
        
        # Validate required fields
        if not account.get("id_token") and not account.get("access_token"):
            print("DEBUG: No valid token found in account data")
            return create_error_response("Google token (id_token or access_token) required", 400)
        if not profile.get("email"):
            print("DEBUG: No email found in profile data")
            return create_error_response("Email is required", 400)
        if not profile.get("sub"):
            print("DEBUG: No sub (Google ID) found in profile data")
            return create_error_response("Google ID (sub) is required", 400)
            
        print("DEBUG: Data validation passed, starting async processing")
        
        # Run async logic without timeout
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            print("DEBUG: Starting async auth without timeout")
            result = loop.run_until_complete(_google_auth_async(data))
            print("DEBUG: Async auth completed successfully")
            print(f"DEBUG: Result type: {type(result)}")
            print(f"DEBUG: Result content: {result}")
            
            # Close loop before creating response
            print("DEBUG: Closing event loop")
            if not loop.is_closed():
                loop.close()
            
            print(f"DEBUG: Returning successful auth response")
            return create_response(result, "Authentication successful")
        except Exception as e:
            print(f"DEBUG: Exception occurred, closing loop: {e}")
            if not loop.is_closed():
                loop.close()
            raise
            
    except Exception as e:
        print(f"Error during Google auth: {e}")
        return create_error_response(f"Authentication failed: {str(e)}", 500)


async def _google_auth_async(data: Dict):
    """Async logic for Google authentication"""
    print("DEBUG: _google_auth_async started")
    
    account = data["account"]
    profile = data["profile"]
    
    print(f"DEBUG: Starting auth for email: {profile.get('email', 'unknown')}")
    
    # Use the token from account data (prefer id_token, fallback to access_token)
    google_token = account.get("id_token") or account.get("access_token")
    print(f"DEBUG: Using token type: {'id_token' if account.get('id_token') else 'access_token'}")
    
    # Verify Google token
    print("DEBUG: About to verify Google token")
    google_user_info = await verify_google_token(google_token)
    print(f"DEBUG: Google token verification result: {google_user_info is not None}")
    
    if not google_user_info:
        raise Exception("Invalid Google token")
    
    print("DEBUG: Token verification passed, checking data consistency")
    
    # Verify that the token data matches profile data
    google_email = google_user_info.get('email')
    google_id = google_user_info.get('sub') or google_user_info.get('id')
    
    print(f"DEBUG: Token email: {google_email}, Profile email: {profile['email']}")
    print(f"DEBUG: Token ID: {google_id}, Profile ID: {profile['sub']}")
    
    if google_email != profile["email"]:
        raise Exception("Email mismatch between token and profile")
        
    if google_id != profile["sub"]:
        raise Exception("Google ID mismatch between token and profile")
    
    print("DEBUG: Data consistency check passed, connecting to database")
    
    # Get database connection
    users_collection = await get_users_collection()
    print("DEBUG: Database connection established")
    
    # Sanitize inputs from profile
    clean_google_id = str(profile["sub"]).strip()
    clean_email = str(profile["email"]).strip().lower()
    
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
                    "name": str(profile["name"] or "").strip(),
                    "avatar": str(profile["picture"] or "").strip(),
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
            "name": str(profile["name"] or "").strip(),
            "avatar": str(profile["picture"] or "").strip(),
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
    token = create_jwt_token(user_id, clean_email)
    
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
            if not loop.is_closed():
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
            if not loop.is_closed():
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
            if not loop.is_closed():
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