"""
JWT authentication middleware for SyntaxMem Flask functions
"""
import jwt
import os
from datetime import datetime, timezone
from typing import Optional, Dict, Any

# JWT configuration
JWT_SECRET = os.getenv('JWT_SECRET')
JWT_ALGORITHM = 'HS256'

if not JWT_SECRET:
    raise ValueError("JWT_SECRET environment variable is required")


def verify_jwt_token_simple(token: str) -> Optional[Dict[str, Any]]:
    """
    Verify JWT token and return user data
    Simplified version for Flask functions
    """
    try:
        print(f"[DEBUG] Verifying token: {token[:20]}...")
        # Decode and verify the token (includes expiration check)
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        print(f"[DEBUG] Token valid, user_id: {payload.get('user_id')}")
        
        # Return user data
        return {
            'user_id': payload.get('user_id'),
            'email': payload.get('email')
        }
        
    except jwt.ExpiredSignatureError as e:
        print(f"[DEBUG] Token expired: {e}")
        return None
    except jwt.InvalidTokenError as e:
        print(f"[DEBUG] Invalid token: {e}")
        return None
    except Exception as e:
        print(f"[DEBUG] Token verification error: {e}")
        return None


def create_jwt_token(user_id: str, email: str) -> str:
    """
    Create short-lived access token for user (10 seconds for testing)
    """
    now = datetime.now(timezone.utc)
    payload = {
        'user_id': user_id,
        'email': email,
        'token_type': 'access',
        'iat': now.timestamp(),
        'exp': (now.timestamp() + 10)  # 10 seconds for testing
    }
    
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def create_refresh_token(user_id: str, email: str) -> str:
    """
    Create long-lived refresh token for user (30 seconds for testing)
    """
    now = datetime.now(timezone.utc)
    payload = {
        'user_id': user_id,
        'email': email,
        'token_type': 'refresh',
        'iat': now.timestamp(),
        'exp': (now.timestamp() + 30)  # 30 seconds for testing
    }
    
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_refresh_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Verify refresh token and return user data
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        
        # Check if it's a refresh token
        if payload.get('token_type') != 'refresh':
            return None
        
        return {
            'user_id': payload.get('user_id'),
            'email': payload.get('email')
        }
        
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    except Exception:
        return None