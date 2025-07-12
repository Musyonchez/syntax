"""
Authentication Cloud Function for SyntaxMem
Handles user authentication, registration, and token verification
"""
import functions_framework
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any
import sys
import os

# Add shared modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from shared.database import get_users_collection, init_database
from shared.auth_middleware import create_jwt_token, verify_jwt_token, verify_token
from shared.utils import generate_id, current_timestamp, create_response, create_error_response

app = FastAPI(title="SyntaxMem Auth Service")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://syntaxmem.dev", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()


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
        users_collection = await get_users_collection()
        
        # Check if user already exists
        existing_user = await users_collection.find_one({
            "$or": [
                {"googleId": auth_request.google_id},
                {"email": auth_request.email}
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
                        "googleId": auth_request.google_id,
                        "name": auth_request.name,
                        "avatar": auth_request.avatar,
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
                "googleId": auth_request.google_id,
                "email": auth_request.email,
                "name": auth_request.name,
                "avatar": auth_request.avatar,
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
        
        return {
            "token": token,
            "user": user_data,
            "message": "Authentication successful"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Authentication failed: {str(e)}"
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
    return app(request.environ, lambda status, headers: None)