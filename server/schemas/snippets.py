# Snippet Schema - Simple validation for code snippets
# Simple, Uniform, Consistent

from datetime import datetime, timezone
from typing import Dict, Any, List

class SnippetSchema:
    """Code snippet data validation"""
    
    @staticmethod
    def validate_create(data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate data for creating a new snippet"""
        if not isinstance(data, dict):
            raise ValueError("Snippet data must be a dictionary")
        
        # Required fields
        title = data.get('title', '').strip()
        code = data.get('code', '').strip()
        language = data.get('language', '').strip().lower()
        
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
        created_by = data.get('createdBy', '').strip()
        
        # Validate difficulty
        if difficulty not in ['easy', 'medium', 'hard']:
            difficulty = 'medium'
        
        # Validate tags
        if not isinstance(tags, list):
            tags = []
        tags = [tag.strip().lower() for tag in tags if isinstance(tag, str) and tag.strip()]
        
        now = datetime.now(timezone.utc)
        
        return {
            'title': title,
            'description': description,
            'code': code,
            'language': language,
            'tags': tags,
            'difficulty': difficulty,
            'createdBy': created_by,
            'createdAt': now,
            'updatedAt': now,
            'isActive': True
        }

# Aliases for convenience
CreateSnippetSchema = SnippetSchema