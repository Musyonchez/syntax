# User Schema - Simple validation for user data
# Simple, Uniform, Consistent

from datetime import datetime, timezone
from typing import Dict, Any, Optional

class UserSchema:
    """User data validation and sanitization"""
    
    @staticmethod
    def validate_create(data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate data for creating a new user"""
        if not isinstance(data, dict):
            raise ValueError("User data must be a dictionary")
        
        # Required fields
        email = data.get('email', '').strip().lower()
        name = data.get('name', '').strip()
        
        if not email or '@' not in email:
            raise ValueError("Valid email is required")
        
        if not name or len(name) < 1:
            raise ValueError("Name is required")
        
        # Optional fields with defaults
        avatar = data.get('avatar', '').strip()
        role = data.get('role', 'user').strip()
        
        # Validate role
        if role not in ['user', 'admin']:
            role = 'user'
        
        now = datetime.now(timezone.utc)
        
        return {
            'email': email,
            'name': name,
            'avatar': avatar,
            'role': role,
            'createdAt': now,
            'updatedAt': now,
            'lastLoginAt': now
        }
    
    @staticmethod
    def validate_update(data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate data for updating user profile"""
        if not isinstance(data, dict):
            raise ValueError("User data must be a dictionary")
        
        update_fields = {}
        
        # Optional updatable fields
        if 'name' in data:
            name = data['name'].strip()
            if name:
                update_fields['name'] = name
        
        if 'avatar' in data:
            avatar = data['avatar'].strip()
            update_fields['avatar'] = avatar
        
        if 'role' in data:
            role = data['role'].strip()
            if role in ['user', 'admin']:
                update_fields['role'] = role
        
        return update_fields

# Aliases for convenience
CreateUserSchema = UserSchema
UpdateUserSchema = UserSchema