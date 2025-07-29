"""
Database schemas and response formatters for SyntaxMem
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
from bson import ObjectId


def format_snippet_response(snippet: Dict[str, Any], snippet_type: str = None, include_content: bool = False) -> Dict[str, Any]:
    """
    Format a snippet document into standardized response format
    
    Args:
        snippet: Raw snippet document from MongoDB
        snippet_type: Override type ("official" | "personal") - if None, infers from collection
        include_content: Whether to include the originalCode in response
    
    Returns:
        Formatted snippet dictionary
    """
    
    # Determine snippet type
    if snippet_type is None:
        # Try to infer from document or use default
        snippet_type = snippet.get("type", "official")
    
    # Format created_at properly
    created_at = snippet.get("createdAt", "")
    if isinstance(created_at, datetime):
        created_at = created_at.isoformat()
    
    formatted_snippet = {
        "id": str(snippet["_id"]),
        "title": snippet.get("title", "Untitled"),
        "language": snippet.get("language", "python"),
        "difficulty": snippet.get("difficulty", 1),
        "type": snippet_type,
        "status": snippet.get("status", "active"),
        "solve_count": snippet.get("solveCount", 0),
        "avg_score": snippet.get("avgScore", 0.0),
        "created_at": created_at,
        "updated_at": snippet.get("updatedAt", created_at)
    }
    
    # Add content if requested
    if include_content:
        formatted_snippet["content"] = snippet.get("originalCode", "")
    else:
        formatted_snippet["content"] = None
    
    # Set author name based on type
    if snippet_type == "official":
        formatted_snippet["author_name"] = snippet.get("authorName", "SyntaxMem Team")
    else:  # personal
        formatted_snippet["author_name"] = "You"
    
    return formatted_snippet


def format_user_response(user: Dict[str, Any]) -> Dict[str, Any]:
    """Format a user document into standardized response format"""
    
    # Format timestamps
    created_at = user.get("createdAt", "")
    if isinstance(created_at, datetime):
        created_at = created_at.isoformat()
        
    last_active = user.get("lastActive", "")
    if isinstance(last_active, datetime):
        last_active = last_active.isoformat()
    
    return {
        "id": str(user["_id"]),
        "google_id": user.get("googleId", ""),
        "email": user.get("email", ""),
        "name": user.get("name", ""),
        "avatar": user.get("avatar", ""),
        "role": user.get("role", "user"),
        "preferences": user.get("preferences", {}),
        "stats": user.get("stats", {}),
        "created_at": created_at,
        "last_active": last_active
    }


def format_pagination_response(items: List[Dict], page: int, per_page: int, total_count: int) -> Dict[str, Any]:
    """Format pagination metadata for list responses"""
    
    total_pages = (total_count + per_page - 1) // per_page
    
    return {
        "snippets": items,  # Client expects "snippets" key
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total_count": total_count,
            "total_pages": total_pages,
            "has_next": page * per_page < total_count,
            "has_prev": page > 1
        }
    }


# Schema validation helpers
def validate_snippet_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate and sanitize snippet input data"""
    
    # Required fields
    title = data.get("title", "").strip()
    if not title:
        raise ValueError("Title is required")
    
    language = data.get("language", "").lower()
    if language not in ["python", "javascript"]:
        raise ValueError("Language must be 'python' or 'javascript'")
    
    try:
        difficulty = int(data.get("difficulty", 1))
        if not (1 <= difficulty <= 10):
            raise ValueError("Difficulty must be between 1 and 10")
    except (ValueError, TypeError):
        raise ValueError("Difficulty must be a number between 1 and 10")
    
    original_code = data.get("originalCode", "").strip()
    if not original_code:
        raise ValueError("Code content is required")
    
    return {
        "title": title[:100],  # Limit title length
        "language": language,
        "difficulty": difficulty,
        "originalCode": original_code[:10000],  # Limit code length
        "status": data.get("status", "private")
    }


def create_official_snippet_document(data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a complete official snippet document for insertion"""
    
    validated_data = validate_snippet_data(data)
    now = datetime.utcnow()
    
    return {
        **validated_data,
        "authorName": data.get("authorName", "SyntaxMem Team"),
        "solveCount": 0,
        "avgScore": 0.0,
        "status": "active",
        "createdAt": now,
        "updatedAt": now
    }


def create_personal_snippet_document(data: Dict[str, Any], user_id: str) -> Dict[str, Any]:
    """Create a complete personal snippet document for insertion"""
    
    validated_data = validate_snippet_data(data)
    now = datetime.utcnow()
    
    return {
        **validated_data,
        "userId": ObjectId(user_id),
        "solveCount": 0,
        "avgScore": 0.0,
        "status": validated_data.get("status", "private"),
        "createdAt": now,
        "updatedAt": now
    }