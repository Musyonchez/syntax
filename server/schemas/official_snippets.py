# Official Snippets Schema - Curated snippets for structured learning
# Simple, Uniform, Consistent

from datetime import datetime, timezone
from typing import Dict, Any, List

class OfficialSnippetSchema:
    """Official snippet data validation"""
    
    @staticmethod
    def validate_create(data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate data for creating a new official snippet"""
        if not isinstance(data, dict):
            raise ValueError("Official snippet data must be a dictionary")
        
        # Required fields
        title = data.get('title', '').strip()
        code = data.get('code', '').strip()
        language = data.get('language', '').strip().lower()
        category = data.get('category', '').strip().lower()
        created_by = data.get('createdBy', '').strip()
        
        if not title:
            raise ValueError("Title is required")
        
        if not code:
            raise ValueError("Code is required")
        
        if not language:
            raise ValueError("Language is required")
        
        if not category:
            raise ValueError("Category is required")
        
        if not created_by:
            raise ValueError("Creator ID is required")
        
        # Optional fields with defaults
        description = data.get('description', '').strip()
        tags = data.get('tags', [])
        difficulty = data.get('difficulty', 'medium').strip().lower()
        learning_objectives = data.get('learningObjectives', [])
        hints = data.get('hints', '').strip()
        solution = data.get('solution', '').strip()
        approved_by = data.get('approvedBy', '').strip()
        estimated_time = data.get('estimatedTime', 0)
        
        # Validate difficulty
        if difficulty not in ['easy', 'medium', 'hard']:
            difficulty = 'medium'
        
        # Validate tags
        if not isinstance(tags, list):
            tags = []
        tags = [tag.strip().lower() for tag in tags if isinstance(tag, str) and tag.strip()]
        
        # Validate learning objectives
        if not isinstance(learning_objectives, list):
            learning_objectives = []
        learning_objectives = [obj.strip() for obj in learning_objectives if isinstance(obj, str) and obj.strip()]
        
        # Validate estimated time
        if not isinstance(estimated_time, (int, float)) or estimated_time < 0:
            estimated_time = 0
        
        now = datetime.now(timezone.utc)
        
        return {
            'title': title,
            'description': description,
            'code': code,
            'language': language,
            'category': category,
            'tags': tags,
            'difficulty': difficulty,
            'learningObjectives': learning_objectives,
            'hints': hints,
            'solution': solution,
            'createdBy': created_by,
            'approvedBy': approved_by,
            'estimatedTime': estimated_time,
            'isPublished': True,
            'isActive': True,
            'practiceCount': 0,
            'averageScore': 0.0,
            'createdAt': now,
            'updatedAt': now
        }
    
    @staticmethod
    def validate_update(data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate data for updating existing official snippet"""
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
        
        if 'category' in data:
            category = data['category'].strip().lower()
            if not category:
                raise ValueError("Category cannot be empty")
            update_fields['category'] = category
        
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
        
        if 'learningObjectives' in data:
            learning_objectives = data['learningObjectives']
            if not isinstance(learning_objectives, list):
                learning_objectives = []
            learning_objectives = [obj.strip() for obj in learning_objectives if isinstance(obj, str) and obj.strip()]
            update_fields['learningObjectives'] = learning_objectives
        
        if 'hints' in data:
            update_fields['hints'] = data['hints'].strip()
        
        if 'solution' in data:
            update_fields['solution'] = data['solution'].strip()
        
        if 'approvedBy' in data:
            update_fields['approvedBy'] = data['approvedBy'].strip()
        
        if 'estimatedTime' in data:
            estimated_time = data['estimatedTime']
            if isinstance(estimated_time, (int, float)) and estimated_time >= 0:
                update_fields['estimatedTime'] = estimated_time
        
        if 'isPublished' in data:
            if isinstance(data['isPublished'], bool):
                update_fields['isPublished'] = data['isPublished']
        
        if 'practiceCount' in data:
            if isinstance(data['practiceCount'], int) and data['practiceCount'] >= 0:
                update_fields['practiceCount'] = data['practiceCount']
        
        if 'averageScore' in data:
            if isinstance(data['averageScore'], (int, float)) and 0 <= data['averageScore'] <= 100:
                update_fields['averageScore'] = float(data['averageScore'])
        
        # Add updatedAt if there are changes
        if update_fields:
            update_fields['updatedAt'] = datetime.now(timezone.utc)
        
        return update_fields

# Aliases for convenience
CreateOfficialSnippetSchema = OfficialSnippetSchema
UpdateOfficialSnippetSchema = OfficialSnippetSchema