# Async Handler Utilities
# Simple, Uniform, Consistent
# 
# CRITICAL: This preserves the MANDATORY async/sync integration pattern
# that powers 14/14 tests passing and production reliability.
# 
# DO NOT modify this pattern - it prevents "Event loop is closed" errors.

import asyncio
import functools
from typing import Callable, Any
from database import db


def run_async_handler(async_func: Callable, *args, **kwargs) -> Any:
    """
    MANDATORY PATTERN implementation for async/sync integration.
    
    This is the exact pattern that powers production reliability:
    1. Create new event loop for each request
    2. CRITICAL: Reset database connection (db.client = None; db.db = None)  
    3. Run async handler
    4. Always close loop in finally block
    5. Re-raise async errors for Flask route handling
    
    Usage (preserves existing Flask route structure):
    @app.route('/endpoint', methods=['POST'])
    def sync_flask_route():
        try:
            # Validate input synchronously
            data = request.get_json()
            validated_data = SomeSchema.validate_create(data)
            
            # Use the MANDATORY PATTERN
            return run_async_handler(_handle_async_operation, validated_data)
            
        except Exception as e:
            return create_error_response(f'Operation failed: {str(e)}', 500)
    
    async def _handle_async_operation(validated_data):
        # All database operations go here
        collection = await db.get_collection()
        result = await collection.insert_one(validated_data)
        return create_response({'_id': str(result.inserted_id)}, 'Success')
    """
    
    # 1. Create new event loop for async operations
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        # 2. CRITICAL: Reset database connection (shared utility requirement)
        db.client = None
        db.db = None
        
        # 3. Run async handler
        result = loop.run_until_complete(async_func(*args, **kwargs))
        return result
        
    except Exception as async_error:
        # 4. Re-raise async errors to be handled by Flask route
        raise async_error
    finally:
        # 5. ALWAYS close the loop
        loop.close()


# Additional utility for common auth pattern
def run_with_auth_validation(async_func: Callable, auth_header: str, *args, **kwargs) -> Any:
    """
    Helper for protected endpoints that need auth validation.
    
    Usage:
    @app.route('/protected', methods=['GET'])
    def protected_route():
        try:
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return create_error_response('Authorization token required', 401)
            
            return run_with_auth_validation(_handle_protected_operation, auth_header, additional_params)
            
        except Exception as e:
            return create_error_response(f'Operation failed: {str(e)}', 500)
    """
    from auth_utils import AuthUtils
    import os
    
    # Validate auth token synchronously (in Flask route context)
    token = auth_header.split(' ')[1]
    auth_utils = AuthUtils(os.getenv('JWT_SECRET'))
    token_data = auth_utils.verify_token(token, 'access')
    
    if not token_data:
        from response_utils import create_error_response
        return create_error_response('Invalid or expired token', 401)
    
    # Use the MANDATORY PATTERN with validated token data
    return run_async_handler(async_func, token_data, *args, **kwargs)


# Template function showing the exact pattern
def template_flask_route():
    """
    Template showing the MANDATORY PATTERN for all Flask routes.
    
    This is the pattern that MUST be preserved in all services.
    Copy this structure for new endpoints.
    """
    from flask import request
    from response_utils import create_error_response
    
    try:
        # 1. Validate input synchronously (in Flask route context)
        data = request.get_json()
        # validated_data = SomeSchema.validate_create(data)
        
        # 2. Use helper function that implements MANDATORY PATTERN
        return run_async_handler(_template_async_handler, data)
        
    except Exception as e:
        # 3. Consistent error handling at Flask route level
        return create_error_response(f'Operation failed: {str(e)}', 500)

async def _template_async_handler(validated_data):
    """
    Template async handler - ALL database operations go here.
    
    This runs inside the MANDATORY PATTERN's async context.
    """
    from response_utils import create_response, create_error_response
    
    try:
        # All async database operations
        collection = await db.get_some_collection()
        result = await collection.insert_one(validated_data)
        
        return create_response({'_id': str(result.inserted_id)}, 'Success')
        
    except Exception as e:
        return create_error_response(f'Database error: {str(e)}', 500)