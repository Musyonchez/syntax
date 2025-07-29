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
        
        # Required fields
        user_id = data.get('userId', '').strip()
        snippet_id = data.get('snippetId', '').strip()
        
        if not user_id:
            raise ValueError("User ID is required")
        
        if not snippet_id:
            raise ValueError("Snippet ID is required")
        
        # Optional fields with defaults
        duration = data.get('duration', 0)
        score = data.get('score', 0)
        completed = data.get('completed', False)
        
        # Validate numeric fields
        if not isinstance(duration, (int, float)) or duration < 0:
            duration = 0
        
        if not isinstance(score, (int, float)) or score < 0:
            score = 0
        
        if not isinstance(completed, bool):
            completed = False
        
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