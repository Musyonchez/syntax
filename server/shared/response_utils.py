from flask import jsonify
from typing import Any, Dict, Optional

def create_response(data: Any = None, message: str = "Success", status_code: int = 200):
    """Create standardized success response"""
    response_data = {
        "success": True,
        "message": message,
        "data": data
    }
    return jsonify(response_data), status_code

def create_error_response(message: str = "Error", status_code: int = 400, error_code: Optional[str] = None):
    """Create standardized error response"""
    response_data = {
        "success": False,
        "message": message,
        "error": error_code or "GENERIC_ERROR"
    }
    return jsonify(response_data), status_code