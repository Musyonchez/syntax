# Personal Snippets Schema - User-created snippets for personal practice
# Simple, Uniform, Consistent

from datetime import datetime, timezone
from typing import Dict, Any, List

class PersonalSnippetSchema:
    """Personal snippet data validation"""
    
    # Allowed programming languages
    ALLOWED_LANGUAGES = [
        'javascript', 'typescript', 'python', 'java', 'c', 'cpp', 'csharp',
        'php', 'ruby', 'go', 'rust', 'swift', 'kotlin', 'html', 'css',
        'scss', 'less', 'sql', 'bash', 'shell', 'json', 'xml', 'yaml',
        'markdown', 'plaintext'
    ]
    
    @staticmethod
    def validate_create(data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate data for creating a new personal snippet"""
        if not isinstance(data, dict):
            raise ValueError("Personal snippet data must be a dictionary")
        
        # Required fields with type validation
        user_id_raw = data.get('userId', '')
        if not isinstance(user_id_raw, str):
            raise ValueError("User ID must be a string")
        user_id = user_id_raw.strip()
        
        title_raw = data.get('title', '')
        if not isinstance(title_raw, str):
            raise ValueError("Title must be a string")
        title = title_raw.strip()
        
        code_raw = data.get('code', '')
        if not isinstance(code_raw, str):
            raise ValueError("Code must be a string")
        code = code_raw.strip()
        
        language_raw = data.get('language', '')
        if not isinstance(language_raw, str):
            raise ValueError("Language must be a string")
        language = language_raw.strip().lower()
        
        if not user_id:
            raise ValueError("User ID is required")
        
        if not title:
            raise ValueError("Title is required")
        
        if not code:
            raise ValueError("Code is required")
        
        if not language:
            raise ValueError("Language is required")
        
        if language not in PersonalSnippetSchema.ALLOWED_LANGUAGES:
            raise ValueError(f"Invalid language. Allowed languages: {', '.join(PersonalSnippetSchema.ALLOWED_LANGUAGES)}")
        
        # Optional fields with defaults and type validation
        description_raw = data.get('description', '')
        if not isinstance(description_raw, str):
            raise ValueError("Description must be a string")
        description = description_raw.strip()
        
        tags_raw = data.get('tags', [])
        if not isinstance(tags_raw, list):
            raise ValueError("Tags must be an array")
        tags = tags_raw
        
        difficulty_raw = data.get('difficulty', 'medium')
        if not isinstance(difficulty_raw, str):
            raise ValueError("Difficulty must be a string")
        difficulty = difficulty_raw.strip().lower()
        
        is_private_raw = data.get('isPrivate', True)
        if not isinstance(is_private_raw, bool):
            raise ValueError("isPrivate must be a boolean")
        is_private = is_private_raw
        
        # Validate difficulty
        if difficulty not in ['easy', 'medium', 'hard']:
            # If difficulty was explicitly provided and invalid, raise error
            if 'difficulty' in data and data.get('difficulty', '').strip():
                raise ValueError("Invalid difficulty. Allowed values: easy, medium, hard")
            # Otherwise use default
            difficulty = 'medium'
        
        # Validate and process tags
        tags = [tag.strip().lower() for tag in tags if isinstance(tag, str) and tag.strip()]
        
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
        
        # Optional updatable fields with type validation
        if 'title' in data:
            if not isinstance(data['title'], str):
                raise ValueError("Title must be a string")
            title = data['title'].strip()
            if not title:
                raise ValueError("Title cannot be empty")
            update_fields['title'] = title
        
        if 'description' in data:
            if not isinstance(data['description'], str):
                raise ValueError("Description must be a string")
            update_fields['description'] = data['description'].strip()
        
        if 'code' in data:
            if not isinstance(data['code'], str):
                raise ValueError("Code must be a string")
            code = data['code'].strip()
            if not code:
                raise ValueError("Code cannot be empty")
            update_fields['code'] = code
        
        if 'language' in data:
            if not isinstance(data['language'], str):
                raise ValueError("Language must be a string")
            language = data['language'].strip().lower()
            if not language:
                raise ValueError("Language cannot be empty")
            if language not in PersonalSnippetSchema.ALLOWED_LANGUAGES:
                raise ValueError(f"Invalid language. Allowed languages: {', '.join(PersonalSnippetSchema.ALLOWED_LANGUAGES)}")
            update_fields['language'] = language
        
        if 'tags' in data:
            tags = data['tags']
            if not isinstance(tags, list):
                raise ValueError("Tags must be an array")
            tags = [tag.strip().lower() for tag in tags if isinstance(tag, str) and tag.strip()]
            update_fields['tags'] = tags
        
        if 'difficulty' in data:
            if not isinstance(data['difficulty'], str):
                raise ValueError("Difficulty must be a string")
            difficulty = data['difficulty'].strip().lower()
            if difficulty not in ['easy', 'medium', 'hard']:
                raise ValueError("Invalid difficulty. Allowed values: easy, medium, hard")
            update_fields['difficulty'] = difficulty
        
        if 'isPrivate' in data:
            if not isinstance(data['isPrivate'], bool):
                raise ValueError("isPrivate must be a boolean")
            update_fields['isPrivate'] = data['isPrivate']
        
        if 'usageCount' in data:
            if not isinstance(data['usageCount'], int):
                raise ValueError("Usage count must be an integer")
            if data['usageCount'] < 0:
                raise ValueError("Usage count must be non-negative")
            update_fields['usageCount'] = data['usageCount']
        
        if 'lastUsed' in data:
            if data['lastUsed'] is not None and not isinstance(data['lastUsed'], datetime):
                raise ValueError("Last used must be a datetime or null")
            update_fields['lastUsed'] = data['lastUsed']
        
        if 'isActive' in data:
            if not isinstance(data['isActive'], bool):
                raise ValueError("isActive must be a boolean")
            update_fields['isActive'] = data['isActive']
        
        # Add updatedAt if there are changes
        if update_fields:
            update_fields['updatedAt'] = datetime.now(timezone.utc)
        
        return update_fields

# Aliases for convenience
CreatePersonalSnippetSchema = PersonalSnippetSchema
UpdatePersonalSnippetSchema = PersonalSnippetSchema