# User Schema - Robust validation for user data
# Simple, Uniform, Consistent with Enhanced Security

import re
from datetime import datetime, timezone
from typing import Dict, Any, Optional

class UserSchema:
    """User data validation and sanitization with enhanced security"""
    
    # Email validation regex - Simple but effective
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    
    # Field length limits
    MAX_EMAIL_LENGTH = 254      # RFC 5321 standard
    MAX_NAME_LENGTH = 100       # Reasonable limit for names
    MAX_AVATAR_URL_LENGTH = 500 # Reasonable limit for URLs
    
    @staticmethod
    def _sanitize_string(value: str, max_length: int = None) -> str:
        """Sanitize string input by stripping whitespace and enforcing length limits"""
        if not isinstance(value, str):
            raise ValueError("Input must be a string")
        
        sanitized = value.strip()
        
        if max_length and len(sanitized) > max_length:
            raise ValueError(f"Input exceeds maximum length of {max_length} characters")
        
        return sanitized
    
    @staticmethod
    def _validate_email(email: str) -> str:
        """Validate and sanitize email address"""
        if not isinstance(email, str):
            raise ValueError("Email must be a string")
        
        # Sanitize and normalize
        email = UserSchema._sanitize_string(email, UserSchema.MAX_EMAIL_LENGTH).lower()
        
        if not email:
            raise ValueError("Email is required")
        
        # Basic format validation
        if not UserSchema.EMAIL_REGEX.match(email):
            raise ValueError("Invalid email format")
        
        # Additional security checks
        if '..' in email:
            raise ValueError("Email contains invalid consecutive dots")
        
        if email.startswith('.') or email.endswith('.'):
            raise ValueError("Email cannot start or end with a dot")
        
        # Check local part (before @)
        local_part = email.split('@')[0]
        if local_part.startswith('.') or local_part.endswith('.'):
            raise ValueError("Email local part cannot start or end with a dot")
        
        # Check domain part (after @)
        domain_part = email.split('@')[1]
        if domain_part.startswith('.') or domain_part.endswith('.'):
            raise ValueError("Email domain cannot start or end with a dot")
        
        return email
    
    @staticmethod
    def _validate_name(name: str) -> str:
        """Validate and sanitize name"""
        if not isinstance(name, str):
            raise ValueError("Name must be a string")
        
        name = UserSchema._sanitize_string(name, UserSchema.MAX_NAME_LENGTH)
        
        if not name:
            raise ValueError("Name is required")
        
        if len(name) < 2:
            raise ValueError("Name must be at least 2 characters long")
        
        # Check for potentially malicious content
        if '<' in name or '>' in name or '&' in name:
            raise ValueError("Name contains invalid characters")
        
        return name
    
    @staticmethod
    def _validate_avatar_url(avatar: str) -> str:
        """Validate and sanitize avatar URL"""
        if not isinstance(avatar, str):
            raise ValueError("Avatar URL must be a string")
        
        avatar = UserSchema._sanitize_string(avatar, UserSchema.MAX_AVATAR_URL_LENGTH)
        
        # Empty avatar is allowed (will use default)
        if not avatar:
            return avatar
        
        # Basic URL validation
        if not (avatar.startswith('http://') or avatar.startswith('https://')):
            raise ValueError("Avatar URL must start with http:// or https://")
        
        # Check for potentially malicious content
        if '<' in avatar or '>' in avatar or '"' in avatar or "'" in avatar:
            raise ValueError("Avatar URL contains invalid characters")
        
        return avatar
    
    @staticmethod
    def validate_create(data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate data for creating a new user with enhanced security"""
        if not isinstance(data, dict):
            raise ValueError("User data must be a dictionary")
        
        # Validate required fields
        email = UserSchema._validate_email(data.get('email', ''))
        name = UserSchema._validate_name(data.get('name', ''))
        
        # Validate optional fields
        avatar = UserSchema._validate_avatar_url(data.get('avatar', ''))
        role = data.get('role', 'user')
        
        # Validate role
        if not isinstance(role, str):
            role = 'user'
        else:
            role = role.strip().lower()
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
        """Validate data for updating user profile with enhanced security"""
        if not isinstance(data, dict):
            raise ValueError("User data must be a dictionary")
        
        update_fields = {}
        
        # Optional updatable fields with validation
        if 'name' in data:
            try:
                name = UserSchema._validate_name(data['name'])
                update_fields['name'] = name
            except ValueError as e:
                raise ValueError(f"Name validation failed: {str(e)}")
        
        if 'avatar' in data:
            try:
                avatar = UserSchema._validate_avatar_url(data['avatar'])
                update_fields['avatar'] = avatar
            except ValueError as e:
                raise ValueError(f"Avatar validation failed: {str(e)}")
        
        if 'role' in data:
            role = data.get('role', '')
            if not isinstance(role, str):
                raise ValueError("Role must be a string")
            
            role = role.strip().lower()
            if role in ['user', 'admin']:
                update_fields['role'] = role
            else:
                raise ValueError("Role must be 'user' or 'admin'")
        
        return update_fields

# Aliases for convenience
CreateUserSchema = UserSchema
UpdateUserSchema = UserSchema