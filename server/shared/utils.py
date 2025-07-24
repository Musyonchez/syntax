"""
Utility functions for SyntaxMem Flask functions
"""
import uuid
from datetime import datetime, timezone
from typing import Any, Dict


def generate_id() -> str:
    """Generate a unique ID"""
    return str(uuid.uuid4()).replace('-', '')


def current_timestamp() -> datetime:
    """Get current UTC timestamp"""
    return datetime.now(timezone.utc)


def create_response(data: Any = None, message: str = "Success") -> Dict[str, Any]:
    """Create standardized API response"""
    return {
        "success": True,
        "message": message,
        "data": data or {}
    }


def create_error_response(message: str = "Error") -> Dict[str, Any]:
    """Create standardized error response"""
    return {
        "success": False,
        "message": message,
        "data": {}
    }