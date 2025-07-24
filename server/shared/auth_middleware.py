"""
JWT authentication middleware for SyntaxMem Flask functions
"""
import jwt
import os
from datetime import datetime
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
        # Decode the token
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        
        # Check if token is expired
        if 'exp' in payload:
            exp_timestamp = payload['exp']
            if datetime.utcnow().timestamp() > exp_timestamp:
                return None
        
        # Return user data
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


def create_jwt_token(user_id: str, email: str) -> str:
    """
    Create JWT token for user
    """
    payload = {
        'user_id': user_id,
        'email': email,
        'iat': datetime.utcnow().timestamp(),
        'exp': datetime.utcnow().timestamp() + (7 * 24 * 60 * 60)  # 7 days
    }
    
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)