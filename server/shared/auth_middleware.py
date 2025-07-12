"""
Authentication middleware for SyntaxMem Cloud Functions
Handles JWT token validation and user authentication
"""
import jwt
import os
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, Dict, Any
from .database import get_users_collection

# Import configuration
from .config import config

# JWT configuration from config
JWT_SECRET = config.JWT_SECRET
JWT_ALGORITHM = config.JWT_ALGORITHM
JWT_EXPIRATION_HOURS = config.JWT_EXPIRATION_HOURS

security = HTTPBearer()


def create_jwt_token(user_id: str, email: str) -> str:
    """Create JWT token for user"""
    payload = {
        "user_id": user_id,
        "email": email,
        "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
        "iat": datetime.utcnow()
    }
    
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


def verify_jwt_token(token: str) -> Dict[str, Any]:
    """Verify JWT token and return payload"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )


async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """Dependency to verify JWT token from Authorization header"""
    token = credentials.credentials
    payload = verify_jwt_token(token)
    
    # Verify user still exists in database
    users_collection = await get_users_collection()
    user = await users_collection.find_one({"_id": payload["user_id"]})
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return {
        "user_id": payload["user_id"],
        "email": payload["email"],
        "user": user
    }


async def verify_admin(user_data: Dict[str, Any] = Depends(verify_token)) -> Dict[str, Any]:
    """Dependency to verify admin privileges"""
    user = user_data["user"]
    
    if user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    
    return user_data


# Optional authentication (for public endpoints that benefit from user context)
async def optional_auth(credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False))) -> Optional[Dict[str, Any]]:
    """Optional authentication - returns user data if token is provided and valid, None otherwise"""
    if not credentials:
        return None
    
    try:
        return await verify_token(credentials)
    except HTTPException:
        return None


class AuthUser:
    """User object from authentication"""
    def __init__(self, user_data: Dict[str, Any]):
        self.user_id = user_data["user_id"]
        self.email = user_data["email"]
        self.user = user_data["user"]
        self.name = self.user.get("name", "")
        self.avatar = self.user.get("avatar", "")
        self.role = self.user.get("role", "user")
        self.preferences = self.user.get("preferences", {})
        self.stats = self.user.get("stats", {})
    
    def is_admin(self) -> bool:
        return self.role == "admin"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "email": self.email,
            "name": self.name,
            "avatar": self.avatar,
            "role": self.role,
            "preferences": self.preferences,
            "stats": self.stats
        }