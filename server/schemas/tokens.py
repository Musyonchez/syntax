# Token Schema - Simple validation for refresh tokens
# Simple, Uniform, Consistent

from datetime import datetime, timezone, timedelta
from typing import Dict, Any

class RefreshTokenSchema:
    """Refresh token data validation"""
    
    @staticmethod
    def validate_create(user_id: str, token: str, expires_in_days: int = 30) -> Dict[str, Any]:
        """Validate data for creating a refresh token"""
        if not user_id or not isinstance(user_id, str):
            raise ValueError("Valid user_id is required")
        
        if not token or not isinstance(token, str):
            raise ValueError("Valid token is required")
        
        if not isinstance(expires_in_days, int):
            raise ValueError("Expires in days must be an integer")
        
        if expires_in_days <= 0:
            raise ValueError("Expires in days must be positive")
        
        now = datetime.now(timezone.utc)
        expires_at = now + timedelta(days=expires_in_days)
        
        return {
            'userId': user_id,
            'token': token,
            'createdAt': now,
            'expiresAt': expires_at
        }