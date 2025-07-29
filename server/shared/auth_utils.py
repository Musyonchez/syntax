import jwt
import secrets
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional

class AuthUtils:
    def __init__(self, jwt_secret: str):
        self.jwt_secret = jwt_secret
        self.algorithm = "HS256"
        self.access_token_expiry = timedelta(hours=1)
        self.refresh_token_expiry = timedelta(days=30)
    
    def create_access_token(self, user_data: Dict[str, Any]) -> str:
        """Create JWT access token"""
        payload = {
            "user_id": user_data["_id"],
            "email": user_data["email"],
            "role": user_data["role"],
            "type": "access",
            "exp": datetime.now(timezone.utc) + self.access_token_expiry,
            "iat": datetime.now(timezone.utc)
        }
        return jwt.encode(payload, self.jwt_secret, algorithm=self.algorithm)
    
    def create_refresh_token(self, user_id: str) -> str:
        """Create JWT refresh token"""
        payload = {
            "user_id": user_id,
            "type": "refresh",
            "exp": datetime.now(timezone.utc) + self.refresh_token_expiry,
            "iat": datetime.now(timezone.utc),
            "jti": secrets.token_urlsafe(32)  # Unique token ID
        }
        return jwt.encode(payload, self.jwt_secret, algorithm=self.algorithm)
    
    def verify_token(self, token: str, token_type: str = "access") -> Optional[Dict[str, Any]]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=[self.algorithm])
            
            if payload.get("type") != token_type:
                return None
                
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def sanitize_string(self, text: str, max_length: int = 255) -> str:
        """Sanitize input string"""
        if not isinstance(text, str):
            return ""
        return text.strip()[:max_length]