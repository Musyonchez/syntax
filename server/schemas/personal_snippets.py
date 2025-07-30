# Personal Snippets Schema - User-created snippets for personal practice
# Simple, Uniform, Consistent

from datetime import datetime, timezone
from typing import Dict, Any, List

class PersonalSnippetSchema:
    """Personal snippet data validation"""
    
    @staticmethod
    def validate_create(data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate data for creating a new personal snippet"""
        if not isinstance(data, dict):
            raise ValueError("Personal snippet data must be a dictionary")
        
        # Required fields
        user_id = data.get('userId', '').strip()
        title = data.get('title', '').strip()
        code = data.get('code', '').strip()
        language = data.get('language', '').strip().lower()
        
        if not user_id:
            raise ValueError("User ID is required")
        
        if not title:
            raise ValueError("Title is required")
        
        if not code:
            raise ValueError("Code is required")
        
        if not language:
            raise ValueError("Language is required")
        
        # Optional fields with defaults
        description = data.get('description', '').strip()
        tags = data.get('tags', [])
        difficulty = data.get('difficulty', 'medium').strip().lower()
        is_private = data.get('isPrivate', True)
        
        # Validate difficulty
        if difficulty not in ['easy', 'medium', 'hard']:
            difficulty = 'medium'
        
        # Validate tags
        if not isinstance(tags, list):
            tags = []
        tags = [tag.strip().lower() for tag in tags if isinstance(tag, str) and tag.strip()]
        
        # Validate privacy setting
        if not isinstance(is_private, bool):
            is_private = True
        
        now = datetime.now(timezone.utc)
        
        return {
            'userId': user_id,
            'title': title,
            'description': description,
            'code': code,
            'language': language,
            'tags': tags,
            'difficulty': difficulty,
            'isPrivate': is_private,
            'usageCount': 0,
            'lastUsed': None,
            'isActive': True,
            'createdAt': now,
            'updatedAt': now
        }
    
    @staticmethod
    def validate_update(data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate data for updating existing personal snippet"""
        if not isinstance(data, dict):
            raise ValueError("Update data must be a dictionary")
        
        update_fields = {}
        
        # Optional updatable fields
        if 'title' in data:
            title = data['title'].strip()
            if not title:
                raise ValueError("Title cannot be empty")
            update_fields['title'] = title
        
        if 'description' in data:
            update_fields['description'] = data['description'].strip()
        
        if 'code' in data:
            code = data['code'].strip()
            if not code:
                raise ValueError("Code cannot be empty")
            update_fields['code'] = code
        
        if 'language' in data:
            language = data['language'].strip().lower()
            if not language:
                raise ValueError("Language cannot be empty")
            update_fields['language'] = language
        
        if 'tags' in data:
            tags = data['tags']
            if not isinstance(tags, list):
                tags = []
            tags = [tag.strip().lower() for tag in tags if isinstance(tag, str) and tag.strip()]
            update_fields['tags'] = tags
        
        if 'difficulty' in data:
            difficulty = data['difficulty'].strip().lower()
            if difficulty not in ['easy', 'medium', 'hard']:
                difficulty = 'medium'
            update_fields['difficulty'] = difficulty
        
        if 'isPrivate' in data:
            if isinstance(data['isPrivate'], bool):
                update_fields['isPrivate'] = data['isPrivate']
        
        if 'usageCount' in data:
            if isinstance(data['usageCount'], int) and data['usageCount'] >= 0:
                update_fields['usageCount'] = data['usageCount']
        
        if 'lastUsed' in data:
            if data['lastUsed'] is None or isinstance(data['lastUsed'], datetime):
                update_fields['lastUsed'] = data['lastUsed']
        
        if 'isActive' in data:
            if isinstance(data['isActive'], bool):
                update_fields['isActive'] = data['isActive']
        
        # Add updatedAt if there are changes
        if update_fields:
            update_fields['updatedAt'] = datetime.now(timezone.utc)
        
        return update_fields

# Aliases for convenience
CreatePersonalSnippetSchema = PersonalSnippetSchema
UpdatePersonalSnippetSchema = PersonalSnippetSchema