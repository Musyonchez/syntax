"""
Authentication Cloud Function for SyntaxMem
Handles user authentication, registration, and token verification
"""
import functions_framework
from fastapi import FastAPI, HTTPException, status, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, ValidationError
from typing import Optional, Dict, Any
import sys
import os
from a2wsgi import ASGIMiddleware
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
import requests


# Add shared modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from shared.database import get_users_collection, init_database
from shared.auth_middleware import create_jwt_token, verify_jwt_token, verify_token
from shared.utils import generate_id, current_timestamp, create_response, create_error_response

app = FastAPI(title="SyntaxMem Auth Service")

# Import configuration
from shared.config import config

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "Accept", "Origin", "X-Requested-With"],
)

security = HTTPBearer()


async def verify_google_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Verify Google OAuth token and return user info
    Returns None if token is invalid
    """
    try:
        # Try to verify as ID token first
        try:
            # Verify the ID token against Google's servers
            idinfo = id_token.verify_oauth2_token(
                token, 
                google_requests.Request(), 
                config.GOOGLE_CLIENT_ID
            )
            
            # Check if token is for our app
            if idinfo['aud'] != config.GOOGLE_CLIENT_ID:
                return None
                
            return idinfo
            
        except ValueError:
            # If ID token fails, try as access token
            pass
            
        # Verify access token by calling Google's userinfo endpoint
        response = requests.get(
            f'https://www.googleapis.com/oauth2/v1/userinfo',
            headers={'Authorization': f'Bearer {token}'},
            timeout=10
        )
        
        if response.status_code == 200:
            userinfo = response.json()
            return userinfo
        else:
            return None
            
    except Exception:
        return None


# Add validation error handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )


# Request/Response models
class GoogleAuthRequest(BaseModel):
    """Google OAuth authentication request"""
    google_token: str
    google_id: str
    email: EmailStr
    name: str
    avatar: str


class LoginResponse(BaseModel):
    """Login response"""
    token: str
    user: Dict[str, Any]
    message: str


class UserProfile(BaseModel):
    """User profile response"""
    user_id: str
    email: str
    name: str
    avatar: str
    role: str
    preferences: Dict[str, Any]
    stats: Dict[str, Any]
    created_at: str


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return create_response({"status": "healthy", "service": "auth"})


@app.post("/google-auth", response_model=LoginResponse)
async def google_auth(auth_request: GoogleAuthRequest):
    """
    Authenticate user with Google OAuth
    Creates new user if doesn't exist, returns JWT token
    """
    try:
        # Verify Google token with Google's servers
        google_user_info = await verify_google_token(auth_request.google_token)
        if not google_user_info:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Google token"
            )
        
        # Verify that the token data matches the request data
        google_email = google_user_info.get('email')
        google_id = google_user_info.get('sub') or google_user_info.get('id')
        
        if google_email != auth_request.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email mismatch between token and request"
            )
            
        if google_id != auth_request.google_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Google ID mismatch between token and request"
            )
        
        # Create a fresh database connection for this request to avoid event loop issues
        from motor.motor_asyncio import AsyncIOMotorClient
        client = AsyncIOMotorClient(config.MONGODB_URI)
        database = client[config.DATABASE_NAME]
        users_collection = database.users
        
        # Sanitize inputs to prevent injection
        clean_google_id = str(auth_request.google_id).strip()
        clean_email = str(auth_request.email).strip().lower()
        
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
                        "name": str(auth_request.name).strip(),
                        "avatar": str(auth_request.avatar).strip(),
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
                "name": str(auth_request.name).strip(),
                "avatar": str(auth_request.avatar).strip(),
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
            user = new_user
        
        # Create JWT token
        token = create_jwt_token(user_id, auth_request.email)
        
        # Prepare user data for response (remove sensitive fields)
        user_data = {
            "user_id": user_id,
            "email": user["email"],
            "name": user["name"],
            "avatar": user["avatar"],
            "role": user["role"],
            "preferences": user["preferences"],
            "stats": user["stats"]
        }
        
        # Close the database connection
        client.close()
        
        return {
            "token": token,
            "user": user_data,
            "message": "Authentication successful"
        }
        
    except Exception as e:
        # Close the database connection if it was created
        try:
            client.close()
        except:
            pass
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication failed"
        )


@app.post("/verify")
async def verify_token_endpoint(user_data: Dict[str, Any] = Depends(verify_token)):
    """
    Verify JWT token and return user data
    """
    return create_response(
        data={
            "valid": True,
            "user": {
                "user_id": user_data["user_id"],
                "email": user_data["email"],
                "name": user_data["user"]["name"],
                "avatar": user_data["user"]["avatar"],
                "role": user_data["user"]["role"]
            }
        },
        message="Token is valid"
    )


@app.get("/profile", response_model=UserProfile)
async def get_user_profile(user_data: Dict[str, Any] = Depends(verify_token)):
    """
    Get user profile data
    """
    user = user_data["user"]
    
    return UserProfile(
        user_id=user_data["user_id"],
        email=user["email"],
        name=user["name"],
        avatar=user["avatar"],
        role=user["role"],
        preferences=user["preferences"],
        stats=user["stats"],
        created_at=user["createdAt"].isoformat() if user.get("createdAt") else ""
    )


@app.put("/profile")
async def update_user_profile(
    profile_data: Dict[str, Any],
    user_data: Dict[str, Any] = Depends(verify_token)
):
    """
    Update user profile preferences
    """
    try:
        users_collection = await get_users_collection()
        user_id = user_data["user_id"]
        
        # Validate and sanitize update data
        allowed_updates = {
            "preferences": profile_data.get("preferences", {}),
            "lastActive": current_timestamp()
        }
        
        # Validate preferences
        if "preferences" in allowed_updates:
            prefs = allowed_updates["preferences"]
            if "theme" in prefs and prefs["theme"] not in ["light", "dark"]:
                raise HTTPException(status_code=400, detail="Invalid theme")
            if "difficulty" in prefs and not (1 <= prefs["difficulty"] <= 10):
                raise HTTPException(status_code=400, detail="Difficulty must be 1-10")
        
        await users_collection.update_one(
            {"_id": user_id},
            {"$set": allowed_updates}
        )
        
        return create_response(message="Profile updated successfully")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Profile update failed: {str(e)}"
        )


@app.delete("/account")
async def delete_user_account(user_data: Dict[str, Any] = Depends(verify_token)):
    """
    Delete user account (soft delete by marking as inactive)
    """
    try:
        users_collection = await get_users_collection()
        user_id = user_data["user_id"]
        
        # Mark user as deleted instead of actually deleting
        await users_collection.update_one(
            {"_id": user_id},
            {
                "$set": {
                    "deleted": True,
                    "deletedAt": current_timestamp()
                }
            }
        )
        
        return create_response(message="Account deleted successfully")
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Account deletion failed: {str(e)}"
        )


@functions_framework.http
def main(request):
    """Cloud Function entry point"""
    return ASGIMiddleware(app)