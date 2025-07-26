"""
Utility functions for SyntaxMem Flask functions
"""
import re
import hashlib
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from bson import ObjectId


def generate_id() -> str:
    """Generate a new ObjectId as string"""
    return str(ObjectId())


def current_timestamp() -> datetime:
    """Get current UTC timestamp"""
    return datetime.now(timezone.utc)


def format_timestamp(dt: datetime) -> str:
    """Format datetime to ISO string"""
    return dt.isoformat()


def parse_timestamp(timestamp_str: str) -> datetime:
    """Parse ISO timestamp string to datetime"""
    return datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))


def sanitize_code(code: str) -> str:
    """Sanitize code content for storage"""
    if not code:
        return ""
    
    # Remove any potential script injections
    code = re.sub(r'<script[^>]*>.*?</script>', '', code, flags=re.IGNORECASE | re.DOTALL)
    
    # Normalize line endings
    code = code.replace('\r\n', '\n').replace('\r', '\n')
    
    # Limit length
    max_length = 10000  # 10KB limit
    if len(code) > max_length:
        code = code[:max_length]
    
    return code.strip()


def sanitize_text(text: str, max_length: int = 1000) -> str:
    """Sanitize text input (titles, comments, etc.)"""
    if not text:
        return ""
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Limit length
    if len(text) > max_length:
        text = text[:max_length].rsplit(' ', 1)[0] + '...'
    
    return text.strip()


def validate_language(language: str) -> bool:
    """Validate programming language"""
    supported_languages = ['python', 'javascript', 'js']
    return language.lower() in supported_languages


def normalize_language(language: str) -> str:
    """Normalize language name"""
    language = language.lower()
    if language == 'js':
        return 'javascript'
    return language


def calculate_difficulty_score(difficulty: int, base_score: float) -> float:
    """Calculate score multiplier based on difficulty"""
    if not 1 <= difficulty <= 10:
        difficulty = 5
    
    # Higher difficulty = higher score multiplier
    multiplier = 1 + (difficulty - 1) * 0.1  # 1.0 to 1.9 multiplier
    return base_score * multiplier


def paginate_results(results: List[Dict], page: int = 1, per_page: int = 20) -> Dict[str, Any]:
    """Paginate a list of results"""
    page = max(1, page)
    per_page = min(max(1, per_page), 100)  # Limit to 100 items per page
    
    total_count = len(results)
    total_pages = (total_count + per_page - 1) // per_page
    
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    
    paginated_results = results[start_idx:end_idx]
    
    return {
        "data": paginated_results,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total_count": total_count,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1
        }
    }


def create_response(data: Any = None, message: str = "Success", status: int = 200) -> tuple:
    """Create standardized API response with Flask jsonify and status"""
    from flask import jsonify
    response_data = {
        "success": status < 400,
        "message": message,
        "data": data or {}
    }
    return jsonify(response_data), status


def create_error_response(message: str = "Error", status: int = 400) -> tuple:
    """Create standardized error response with Flask jsonify and status"""
    from flask import jsonify
    response_data = {
        "success": False,
        "message": message,
        "data": {}
    }
    return jsonify(response_data), status


def hash_string(text: str) -> str:
    """Create SHA-256 hash of string"""
    return hashlib.sha256(text.encode()).hexdigest()


def generate_slug(title: str) -> str:
    """Generate URL-friendly slug from title"""
    # Convert to lowercase and replace spaces with hyphens
    slug = re.sub(r'[^\w\s-]', '', title.lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug.strip('-')


def extract_code_language(code: str) -> str:
    """Try to detect programming language from code content"""
    # Simple heuristics
    if 'def ' in code or 'import ' in code or 'print(' in code:
        return 'python'
    elif 'function ' in code or 'const ' in code or 'console.log' in code:
        return 'javascript'
    else:
        return 'python'  # Default to Python


def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def clean_user_input(data: Dict[str, Any]) -> Dict[str, Any]:
    """Clean and validate user input data"""
    cleaned = {}
    
    for key, value in data.items():
        if isinstance(value, str):
            # Sanitize string inputs
            if key in ['title', 'name', 'username']:
                cleaned[key] = sanitize_text(value, 100)
            elif key in ['content', 'code']:
                cleaned[key] = sanitize_code(value)
            elif key in ['comment', 'description']:
                cleaned[key] = sanitize_text(value, 500)
            else:
                cleaned[key] = sanitize_text(value)
        elif isinstance(value, (int, float, bool)):
            cleaned[key] = value
        elif isinstance(value, dict):
            cleaned[key] = clean_user_input(value)
        elif isinstance(value, list):
            cleaned[key] = [clean_user_input(item) if isinstance(item, dict) else item for item in value]
        else:
            cleaned[key] = value
    
    return cleaned


class Timer:
    """Simple timer for measuring execution time"""
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
    
    def start(self):
        self.start_time = datetime.now()
        return self
    
    def stop(self):
        self.end_time = datetime.now()
        return self
    
    def elapsed_seconds(self) -> float:
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0.0
    
    def __enter__(self):
        return self.start()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()