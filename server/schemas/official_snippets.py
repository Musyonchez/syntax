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
        
        # Required fields with type validation
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
        
        category_raw = data.get('category', '')
        if not isinstance(category_raw, str):
            raise ValueError("Category must be a string")
        category = category_raw.strip().lower()
        
        created_by_raw = data.get('createdBy', '')
        if not isinstance(created_by_raw, str):
            raise ValueError("Creator ID must be a string")
        created_by = created_by_raw.strip()
        
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
        
        learning_objectives_raw = data.get('learningObjectives', [])
        if not isinstance(learning_objectives_raw, list):
            raise ValueError("Learning objectives must be an array")
        learning_objectives = learning_objectives_raw
        
        hints_raw = data.get('hints', '')
        if not isinstance(hints_raw, str):
            raise ValueError("Hints must be a string")
        hints = hints_raw.strip()
        
        solution_raw = data.get('solution', '')
        if not isinstance(solution_raw, str):
            raise ValueError("Solution must be a string")
        solution = solution_raw.strip()
        
        approved_by_raw = data.get('approvedBy', '')
        if not isinstance(approved_by_raw, str):
            raise ValueError("Approved by must be a string")
        approved_by = approved_by_raw.strip()
        
        estimated_time_raw = data.get('estimatedTime', 0)
        if not isinstance(estimated_time_raw, (int, float)):
            raise ValueError("Estimated time must be a number")
        estimated_time = estimated_time_raw
        
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
            update_fields['language'] = language
        
        if 'category' in data:
            if not isinstance(data['category'], str):
                raise ValueError("Category must be a string")
            category = data['category'].strip().lower()
            if not category:
                raise ValueError("Category cannot be empty")
            update_fields['category'] = category
        
        if 'tags' in data:
            if not isinstance(data['tags'], list):
                raise ValueError("Tags must be an array")
            tags = [tag.strip().lower() for tag in data['tags'] if isinstance(tag, str) and tag.strip()]
            update_fields['tags'] = tags
        
        if 'difficulty' in data:
            if not isinstance(data['difficulty'], str):
                raise ValueError("Difficulty must be a string")
            difficulty = data['difficulty'].strip().lower()
            if difficulty not in ['easy', 'medium', 'hard']:
                difficulty = 'medium'
            update_fields['difficulty'] = difficulty
        
        if 'learningObjectives' in data:
            if not isinstance(data['learningObjectives'], list):
                raise ValueError("Learning objectives must be an array")
            learning_objectives = [obj.strip() for obj in data['learningObjectives'] if isinstance(obj, str) and obj.strip()]
            update_fields['learningObjectives'] = learning_objectives
        
        if 'hints' in data:
            if not isinstance(data['hints'], str):
                raise ValueError("Hints must be a string")
            update_fields['hints'] = data['hints'].strip()
        
        if 'solution' in data:
            if not isinstance(data['solution'], str):
                raise ValueError("Solution must be a string")
            update_fields['solution'] = data['solution'].strip()
        
        if 'approvedBy' in data:
            if not isinstance(data['approvedBy'], str):
                raise ValueError("Approved by must be a string")
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