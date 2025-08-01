# Session Schema - Simple validation for practice sessions
# Simple, Uniform, Consistent

from datetime import datetime, timezone
from typing import Dict, Any, Optional

class SessionSchema:
    """Practice session data validation"""
    
    @staticmethod
    def validate_create(data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate data for creating a new practice session"""
        if not isinstance(data, dict):
            raise ValueError("Session data must be a dictionary")
        
        # Required fields with type validation
        user_id_raw = data.get('userId', '')
        if not isinstance(user_id_raw, str):
            raise ValueError("User ID must be a string")
        user_id = user_id_raw.strip()
        
        snippet_id_raw = data.get('snippetId', '')
        if not isinstance(snippet_id_raw, str):
            raise ValueError("Snippet ID must be a string")
        snippet_id = snippet_id_raw.strip()
        
        if not user_id:
            raise ValueError("User ID is required")
        
        if not snippet_id:
            raise ValueError("Snippet ID is required")
        
        # Optional fields with strict type validation
        duration = data.get('duration', 0)
        if not isinstance(duration, (int, float)):
            raise ValueError("Duration must be a number")
        if duration < 0:
            raise ValueError("Duration must be non-negative")
        
        score = data.get('score', 0)
        if not isinstance(score, (int, float)):
            raise ValueError("Score must be a number")
        if score < 0:
            raise ValueError("Score must be non-negative")
        
        completed = data.get('completed', False)
        if not isinstance(completed, bool):
            raise ValueError("Completed must be a boolean")
        
        now = datetime.now(timezone.utc)
        
        return {
            'userId': user_id,
            'snippetId': snippet_id,
            'duration': duration,
            'score': score,
            'completed': completed,
            'startedAt': now,
            'completedAt': now if completed else None,
            'createdAt': now
        }

# Aliases for convenience
CreateSessionSchema = SessionSchema