"""
Auth Cloud Function for SyntaxMem
Handles user authentication using Flask
"""

import asyncio
import logging
import os
import re
import time
from collections import defaultdict
from typing import Any, Dict, Optional

import functions_framework
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

# Create Flask app
app = Flask(__name__)

# Configure CORS with environment-based origins
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:3001,https://syntaxmem.com").split(",")
CORS(app, origins=[origin.strip() for origin in cors_origins], 
     methods=["GET", "POST", "OPTIONS"], headers=["Content-Type", "Authorization"])

# Import utilities
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from shared.auth_middleware import verify_jwt_token_simple, create_jwt_token, create_refresh_token, verify_refresh_token
from shared.database import get_users_collection
from shared.utils import current_timestamp, generate_id, create_response, create_error_response
from shared.config import config

# Google OAuth imports
import requests
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token


def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def sanitize_string(value: str, max_length: int = 255) -> str:
    """Sanitize string input"""
    if not value:
        return ""
    
    # Remove any HTML tags and extra whitespace
    value = re.sub(r'<[^>]+>', '', str(value))
    value = ' '.join(value.split())
    
    # Limit length
    if len(value) > max_length:
        value = value[:max_length]
    
    return value.strip()


def validate_google_id(google_id: str) -> bool:
    """Validate Google ID format (should be numeric string)"""
    return google_id.isdigit() and len(google_id) > 10


# Simple in-memory rate limiting (for serverless functions)
request_counts = defaultdict(list)

def is_rate_limited(client_ip: str, max_requests: int = 10, window_minutes: int = 15) -> bool:
    """Check if client IP is rate limited"""
    now = time.time()
    window_start = now - (window_minutes * 60)
    
    # Clean old requests
    request_counts[client_ip] = [req_time for req_time in request_counts[client_ip] if req_time > window_start]
    
    # Check if over limit
    if len(request_counts[client_ip]) >= max_requests:
        return True
    
    # Add current request
    request_counts[client_ip].append(now)
    return False


async def log_auth_event(event_type: str, client_ip: str, user_email: str = None, user_id: str = None, 
                        success: bool = True, error_message: str = None, metadata: dict = None):
    """Log authentication events for security monitoring"""
    try:
        from shared.database import get_database
        db = await get_database()
        audit_collection = db.audit_logs
        
        audit_entry = {
            "event_type": event_type,  # "login_attempt", "login_success", "login_failure", "token_refresh"
            "timestamp": current_timestamp(),
            "client_ip": client_ip,
            "user_email": user_email,
            "user_id": user_id,
            "success": success,
            "error_message": error_message,
            "metadata": metadata or {},
            "service": "auth"
        }
        
        await audit_collection.insert_one(audit_entry)
        logger.info(f"Audit log recorded: {event_type} for {user_email or 'unknown'}")
    except Exception as e:
        # Don't fail auth if audit logging fails
        logger.error(f"Failed to write audit log: {str(e)}")
        pass




async def verify_google_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify Google OAuth token and return user info"""
    try:
        logger.info("Starting Google token verification")
        
        # Try to verify as ID token first (this is what NextAuth sends)
        try:
            idinfo = id_token.verify_oauth2_token(
                token,
                google_requests.Request(),
                os.getenv('GOOGLE_CLIENT_ID')
            )
            
            if idinfo and idinfo.get('aud') == os.getenv('GOOGLE_CLIENT_ID'):
                logger.info("ID token verification successful")
                return idinfo
            else:
                logger.warning("ID token audience mismatch")
                
        except Exception as e:
            logger.debug(f"ID token verification failed: {str(e)}")
            # If ID token fails, try as access token
            pass
        
        # Fallback: verify as access token using Google's userinfo endpoint
        try:
            response = requests.get(
                'https://www.googleapis.com/oauth2/v1/userinfo',
                headers={'Authorization': f'Bearer {token}'},
                timeout=5  # Increased timeout slightly
            )
            
            if response.status_code == 200:
                user_info = response.json()
                logger.info("Access token verification successful")
                return user_info
            else:
                logger.warning(f"Userinfo endpoint returned status {response.status_code}")
                
        except Exception as e:
            logger.debug(f"Access token verification failed: {str(e)}")
            pass
            
        logger.warning("All token verification methods failed")
        return None
        
    except Exception as e:
        logger.error(f"Token verification error: {str(e)}")
        return None


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return create_response({"status": "healthy", "service": "auth"})


@app.route("/google-auth", methods=["POST"])
def google_auth():
    """Authenticate user with Google OAuth"""
    try:
        # Rate limiting check
        client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR', 'unknown'))
        if is_rate_limited(client_ip):
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            # Log rate limit exceeded event (async)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(log_auth_event(
                    "rate_limit_exceeded", client_ip, success=False, 
                    error_message="Too many authentication attempts"
                ))
            finally:
                loop.close()
            return create_error_response("Too many authentication attempts. Please try again later.", 429)
        
        logger.info("Received Google OAuth authentication request")
        
        # Get request data
        data = request.get_json()
        if not data:
            logger.warning("No JSON data received in auth request")
            return create_error_response("Invalid JSON data", 400)
        
        # Check that we have account and profile data
        if not data.get("account") or not data.get("profile"):
            logger.warning("Missing required account or profile data")
            return create_error_response("Account and profile data required", 400)
        
        account = data["account"]
        profile = data["profile"]
        
        # Validate required fields
        if not account.get("id_token") and not account.get("access_token"):
            logger.warning("No valid Google token found in request")
            return create_error_response("Google token (id_token or access_token) required", 400)
        
        email = profile.get("email")
        google_id = profile.get("sub")
        
        if not email:
            logger.warning("Email missing from profile data")
            return create_error_response("Email is required", 400)
        if not validate_email(email):
            logger.warning("Invalid email format in profile data")
            return create_error_response("Invalid email format", 400)
        if not google_id:
            logger.warning("Google ID (sub) missing from profile data")
            return create_error_response("Google ID (sub) is required", 400)
        if not validate_google_id(str(google_id)):
            logger.warning("Invalid Google ID format")
            return create_error_response("Invalid Google ID format", 400)
            
        logger.info("Input validation passed, starting authentication process")
        
        # Run async logic without timeout
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(_google_auth_async(data, client_ip))
            logger.info("Authentication process completed successfully")
            
            # Close loop before creating response
            if not loop.is_closed():
                loop.close()
            
            return create_response(result, "Authentication successful")
        except Exception as e:
            logger.error(f"Authentication process failed: {str(e)}")
            if not loop.is_closed():
                loop.close()
            raise
            
    except Exception as e:
        logger.error(f"Google authentication error: {str(e)}")
        return create_error_response(f"Authentication failed: {str(e)}", 500)


async def _google_auth_async(data: Dict, client_ip: str):
    """Async logic for Google authentication"""
    account = data["account"]
    profile = data["profile"]
    
    # Use the token from account data (prefer id_token, fallback to access_token)
    google_token = account.get("id_token") or account.get("access_token")
    
    # Verify Google token
    user_email = profile["email"]
    await log_auth_event("login_attempt", client_ip, user_email)
    
    google_user_info = await verify_google_token(google_token)
    
    if not google_user_info:
        await log_auth_event("login_failure", client_ip, user_email, 
                           success=False, error_message="Invalid Google token")
        raise Exception("Invalid Google token")
    
    # Verify that the token data matches profile data
    google_email = google_user_info.get('email')
    google_id = google_user_info.get('sub') or google_user_info.get('id')
    
    if google_email != profile["email"]:
        await log_auth_event("login_failure", client_ip, user_email, 
                           success=False, error_message="Email mismatch between token and profile")
        raise Exception("Email mismatch between token and profile")
        
    if google_id != profile["sub"]:
        await log_auth_event("login_failure", client_ip, user_email, 
                           success=False, error_message="Google ID mismatch between token and profile")
        raise Exception("Google ID mismatch between token and profile")
    
    # Get database connection
    users_collection = await get_users_collection()
    
    # Sanitize inputs from profile
    clean_google_id = str(profile["sub"]).strip()
    clean_email = profile["email"].strip().lower()
    clean_name = sanitize_string(profile.get("name", ""), 100)
    clean_avatar = sanitize_string(profile.get("picture", ""), 500)
    
    # Check if user already exists
    existing_user = await users_collection.find_one({
        "$or": [
            {"googleId": clean_google_id},
            {"email": clean_email}
        ]
    })
    
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
        user_id = generate_id()
        new_user = {
            "_id": user_id,
            "googleId": clean_google_id,
            "email": clean_email,
            "name": clean_name,
            "avatar": clean_avatar,
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
        
        await users_collection.insert_one(new_user)
        logger.info(f"Created new user account")
        user = new_user
    
    # Create access and refresh tokens
    access_token = create_jwt_token(user_id, clean_email)
    refresh_token = create_refresh_token(user_id, clean_email)
    
    # Log successful authentication
    await log_auth_event("login_success", client_ip, clean_email, user_id, 
                       metadata={"new_user": existing_user is None})
    
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
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token": access_token,  # Keep for backward compatibility
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


@app.route("/refresh", methods=["POST"])
def refresh_token():
    """Refresh access token using refresh token"""
    try:
        # Rate limiting check
        client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR', 'unknown'))
        if is_rate_limited(client_ip, max_requests=20, window_minutes=15):  # More lenient for refresh
            logger.warning(f"Rate limit exceeded for refresh endpoint IP: {client_ip}")
            return create_error_response("Too many refresh attempts. Please try again later.", 429)
        
        # Get request data
        data = request.get_json()
        if not data or not data.get("refresh_token"):
            return create_error_response("Refresh token required", 400)
        
        refresh_token = data["refresh_token"]
        
        # Verify refresh token
        user_data = verify_refresh_token(refresh_token)
        if not user_data:
            logger.warning("Invalid or expired refresh token used")
            return create_error_response("Invalid or expired refresh token", 401)
        
        user_id = user_data["user_id"]
        email = user_data["email"]
        
        # Create new access token
        new_access_token = create_jwt_token(user_id, email)
        
        # Log token refresh event
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(log_auth_event(
                "token_refresh", client_ip, email, user_id, 
                metadata={"refresh_token_used": True}
            ))
        finally:
            loop.close()
        
        logger.info(f"Token refreshed successfully for user: {user_id}")
        
        return create_response({
            "access_token": new_access_token,
            "token": new_access_token,  # Backward compatibility
            "expires_in": 3600  # 1 hour in seconds
        }, "Token refreshed successfully")
        
    except Exception as e:
        logger.error(f"Token refresh error: {str(e)}")
        return create_error_response(f"Token refresh failed: {str(e)}", 500)


@functions_framework.http
def main(request):
    """Cloud Function entry point"""
    with app.request_context(request.environ):
        return app.full_dispatch_request()