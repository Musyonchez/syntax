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
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        return handle_cors_preflight()
    
    try:
        # Use ASGIMiddleware to handle the request properly
        asgi_app = ASGIMiddleware(app)
        
        # Create a mock start_response to capture the response
        response_data = {}
        
        def start_response(status, headers, exc_info=None):
            response_data['status'] = status
            response_data['headers'] = dict(headers)
            return lambda x: None
        
        # Call the ASGI app with proper WSGI interface
        result = asgi_app(request.environ, start_response)
        
        # Convert the result to a proper response
        body = b''.join(result) if result else b''
        status_code = int(response_data.get('status', '200 OK').split()[0])
        headers = response_data.get('headers', {})
        
        # Create response with the body and headers
        response = Response(
            body.decode('utf-8') if body else '',
            status=status_code,
            content_type=headers.get('content-type', 'application/json')
        )
        
        # Add existing headers from ASGI response
        for key, value in headers.items():
            if key.lower() not in ['content-type', 'content-length']:
                response.headers[key] = value
        
        # Add CORS headers
        return add_cors_headers(response)
        
    except Exception as e:
        # Return error response with CORS headers
        return create_cors_error_response(f"Internal server error: {str(e)}")