"""
CORS handler utility for SyntaxMem Cloud Functions
Provides uniform CORS handling across all serverless functions
"""
import json
import asyncio
from werkzeug.wrappers import Response
from a2wsgi import ASGIMiddleware
from typing import Any


def handle_cors_preflight() -> Response:
    """Handle CORS preflight OPTIONS requests"""
    response = Response('')
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response


def add_cors_headers(response: Response) -> Response:
    """Add CORS headers to any response"""
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response


def create_cors_error_response(message: str, status_code: int = 500) -> Response:
    """Create error response with CORS headers"""
    error_response = {
        "status": "error",
        "message": message,
        "data": None
    }
    response = Response(
        json.dumps(error_response),
        status=status_code,
        content_type='application/json'
    )
    return add_cors_headers(response)


def handle_cors_request(app: Any, request: Any) -> Response:
    """
    Handle request with CORS support
    
    Args:
        app: FastAPI application instance
        request: Google Cloud Function request object
        
    Returns:
        Response with proper CORS headers
    """
    # Set up event loop
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        return handle_cors_preflight()
    
    try:
        # Use ASGIMiddleware to handle the request
        response = ASGIMiddleware(app)(request)
        
        # Add CORS headers to the response
        if hasattr(response, 'headers'):
            return add_cors_headers(response)
        
        return response
        
    except Exception as e:
        # Return error response with CORS headers
        return create_cors_error_response(f"Internal server error: {str(e)}")