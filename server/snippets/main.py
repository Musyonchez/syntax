# Snippets Function - Personal and Official snippet management
# Port: 8083

import os
import asyncio
from datetime import datetime, timezone
from flask import Flask, request
from flask_cors import CORS
from dotenv import load_dotenv

# Import shared utilities
import sys
sys.path.append('../shared')
sys.path.append('../schemas')
from auth_utils import AuthUtils
from database import db
from response_utils import create_response, create_error_response
from personal_snippets import PersonalSnippetSchema
from official_snippets import OfficialSnippetSchema

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))

app = Flask(__name__)

# Configure CORS
allowed_origins = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')
CORS(app, origins=allowed_origins)

# Initialize auth utils
JWT_SECRET = os.getenv('JWT_SECRET')
if not JWT_SECRET:
    raise ValueError("JWT_SECRET environment variable not set")

auth_utils = AuthUtils(JWT_SECRET)

@app.route('/health')
def health():
    """Health check endpoint"""
    return create_response({'status': 'ok', 'service': 'snippets'}, 'Snippets service is healthy')

# =============================================================================
# PERSONAL SNIPPETS ENDPOINTS
# =============================================================================

@app.route('/personal', methods=['GET'])
def get_personal_snippets():
    """Get user's personal snippets with optional filtering"""
    try:
        # Get auth token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return create_error_response('Authorization token required', 401)
        
        token = auth_header.split(' ')[1]
        token_data = auth_utils.verify_token(token, 'access')
        if not token_data:
            return create_error_response('Invalid or expired token', 401)
        
        user_id = token_data.get('user_id')
        
        # Get query parameters for filtering
        language = request.args.get('language')
        difficulty = request.args.get('difficulty')
        tag = request.args.get('tag')
        search = request.args.get('search')
        
        # Run async operations using auth pattern
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            # Reset database connection for new event loop
            db.client = None
            db.db = None
            result = loop.run_until_complete(_handle_get_personal_snippets(user_id, language, difficulty, tag, search))
            return result
        except Exception as async_error:
            raise async_error
        finally:
            loop.close()
            
    except Exception as e:
        return create_error_response(f'Failed to get personal snippets: {str(e)}', 500)

async def _handle_get_personal_snippets(user_id: str, language: str, difficulty: str, tag: str, search: str):
    """Async handler for getting personal snippets"""
    try:
        # Build query
        query = {'userId': user_id, 'isActive': True}
        
        if language:
            query['language'] = language.lower()
        if difficulty and difficulty in ['easy', 'medium', 'hard']:
            query['difficulty'] = difficulty.lower()
        if tag:
            query['tags'] = {'$in': [tag.lower()]}
        if search:
            query['$or'] = [
                {'title': {'$regex': search, '$options': 'i'}},
                {'description': {'$regex': search, '$options': 'i'}}
            ]
        
        # Execute query
        collection = await db.get_personal_snippets_collection()
        cursor = collection.find(query).sort('updatedAt', -1)
        snippets = []
        async for snippet in cursor:
            snippet['_id'] = str(snippet['_id'])
            snippets.append(snippet)
        
        return create_response({
            'snippets': snippets,
            'count': len(snippets)
        }, 'Personal snippets retrieved successfully')
        
    except Exception as e:
        return create_error_response(f'Database error: {str(e)}', 500)

@app.route('/personal', methods=['POST'])
def create_personal_snippet():
    """Create a new personal snippet"""
    try:
        # Get auth token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return create_error_response('Authorization token required', 401)
        
        token = auth_header.split(' ')[1]
        token_data = auth_utils.verify_token(token, 'access')
        if not token_data:
            return create_error_response('Invalid or expired token', 401)
        
        user_id = token_data.get('user_id')
        
        # Get and validate data
        data = request.get_json()
        if not data:
            return create_error_response('Invalid JSON data', 400)
        
        # Run async operations using auth pattern
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            # Reset database connection for new event loop
            db.client = None
            db.db = None
            result = loop.run_until_complete(_handle_create_personal_snippet(user_id, data))
            return result
        except Exception as async_error:
            raise async_error
        finally:
            loop.close()
            
    except Exception as e:
        return create_error_response(f'Failed to create personal snippet: {str(e)}', 500)

async def _handle_create_personal_snippet(user_id: str, data: dict):
    """Async handler for creating personal snippet"""
    try:
        # Add user_id to data and validate using schema
        data['userId'] = user_id
        try:
            validated_data = PersonalSnippetSchema.validate_create(data)
        except ValueError as e:
            return create_error_response(f'Validation error: {str(e)}', 400)
        
        # Insert into database
        collection = await db.get_personal_snippets_collection()
        result = await collection.insert_one(validated_data)
        validated_data['_id'] = str(result.inserted_id)
        
        return create_response(validated_data, 'Personal snippet created successfully')
        
    except Exception as e:
        return create_error_response(f'Database error: {str(e)}', 500)

@app.route('/personal/<snippet_id>', methods=['PUT'])
def update_personal_snippet(snippet_id: str):
    """Update a personal snippet"""
    try:
        # Get auth token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return create_error_response('Authorization token required', 401)
        
        token = auth_header.split(' ')[1]
        token_data = auth_utils.verify_token(token, 'access')
        if not token_data:
            return create_error_response('Invalid or expired token', 401)
        
        user_id = token_data.get('user_id')
        
        # Get and validate data
        data = request.get_json()
        if not data:
            return create_error_response('Invalid JSON data', 400)
        
        # Run async operations using auth pattern
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            # Reset database connection for new event loop
            db.client = None
            db.db = None
            result = loop.run_until_complete(_handle_update_personal_snippet(user_id, snippet_id, data))
            return result
        except Exception as async_error:
            raise async_error
        finally:
            loop.close()
            
    except Exception as e:
        return create_error_response(f'Failed to update personal snippet: {str(e)}', 500)

async def _handle_update_personal_snippet(user_id: str, snippet_id: str, data: dict):
    """Async handler for updating personal snippet"""
    try:
        from bson import ObjectId
        
        # Validate ObjectId
        try:
            obj_id = ObjectId(snippet_id)
        except:
            return create_error_response('Invalid snippet ID format', 400)
        
        # Validate data using schema
        try:
            update_data = PersonalSnippetSchema.validate_update(data)
        except ValueError as e:
            return create_error_response(f'Validation error: {str(e)}', 400)
        
        # Check ownership and update
        collection = await db.get_personal_snippets_collection()
        
        # First check if snippet exists and user owns it
        existing = await collection.find_one({'_id': obj_id, 'userId': user_id, 'isActive': True})
        if not existing:
            return create_error_response('Snippet not found or access denied', 404)
        
        # Update the snippet
        update_data['updatedAt'] = datetime.now(timezone.utc)
        result = await collection.update_one(
            {'_id': obj_id, 'userId': user_id}, 
            {'$set': update_data}
        )
        
        if result.modified_count == 0:
            return create_error_response('No changes made to snippet', 400)
        
        # Get updated snippet
        updated_snippet = await collection.find_one({'_id': obj_id})
        updated_snippet['_id'] = str(updated_snippet['_id'])
        
        return create_response(updated_snippet, 'Personal snippet updated successfully')
        
    except Exception as e:
        return create_error_response(f'Database error: {str(e)}', 500)

@app.route('/personal/<snippet_id>', methods=['DELETE'])
def delete_personal_snippet(snippet_id: str):
    """Delete (soft delete) a personal snippet"""
    try:
        # Get auth token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return create_error_response('Authorization token required', 401)
        
        token = auth_header.split(' ')[1]
        token_data = auth_utils.verify_token(token, 'access')
        if not token_data:
            return create_error_response('Invalid or expired token', 401)
        
        user_id = token_data.get('user_id')
        
        # Run async operations using auth pattern
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            # Reset database connection for new event loop
            db.client = None
            db.db = None
            result = loop.run_until_complete(_handle_delete_personal_snippet(user_id, snippet_id))
            return result
        except Exception as async_error:
            raise async_error
        finally:
            loop.close()
            
    except Exception as e:
        return create_error_response(f'Failed to delete personal snippet: {str(e)}', 500)

async def _handle_delete_personal_snippet(user_id: str, snippet_id: str):
    """Async handler for deleting personal snippet"""
    try:
        from bson import ObjectId
        
        # Validate ObjectId
        try:
            obj_id = ObjectId(snippet_id)
        except:
            return create_error_response('Invalid snippet ID format', 400)
        
        # Soft delete (set isActive to False)
        collection = await db.get_personal_snippets_collection()
        result = await collection.update_one(
            {'_id': obj_id, 'userId': user_id, 'isActive': True},
            {'$set': {'isActive': False, 'updatedAt': datetime.now(timezone.utc)}}
        )
        
        if result.matched_count == 0:
            return create_error_response('Snippet not found or access denied', 404)
        
        return create_response({'deleted': True}, 'Personal snippet deleted successfully')
        
    except Exception as e:
        return create_error_response(f'Database error: {str(e)}', 500)

# =============================================================================
# OFFICIAL SNIPPETS ENDPOINTS
# =============================================================================

@app.route('/official', methods=['GET'])
def get_official_snippets():
    """Get official snippets (no auth required for browsing)"""
    try:
        # Get query parameters for filtering
        language = request.args.get('language')
        difficulty = request.args.get('difficulty')
        tag = request.args.get('tag')
        search = request.args.get('search')
        
        # Run async operations using auth pattern
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            # Reset database connection for new event loop
            db.client = None
            db.db = None
            result = loop.run_until_complete(_handle_get_official_snippets(language, difficulty, tag, search))
            return result
        except Exception as async_error:
            raise async_error
        finally:
            loop.close()
            
    except Exception as e:
        return create_error_response(f'Failed to get official snippets: {str(e)}', 500)

async def _handle_get_official_snippets(language: str, difficulty: str, tag: str, search: str):
    """Async handler for getting official snippets"""
    try:
        # Build query
        query = {'isActive': True}
        
        if language:
            query['language'] = language.lower()
        if difficulty and difficulty in ['easy', 'medium', 'hard']:
            query['difficulty'] = difficulty.lower()
        if tag:
            query['tags'] = {'$in': [tag.lower()]}
        if search:
            query['$or'] = [
                {'title': {'$regex': search, '$options': 'i'}},
                {'description': {'$regex': search, '$options': 'i'}}
            ]
        
        # Execute query
        collection = await db.get_official_snippets_collection()
        cursor = collection.find(query).sort('createdAt', -1)
        snippets = []
        async for snippet in cursor:
            snippet['_id'] = str(snippet['_id'])
            snippets.append(snippet)
        
        return create_response({
            'snippets': snippets,
            'count': len(snippets)
        }, 'Official snippets retrieved successfully')
        
    except Exception as e:
        return create_error_response(f'Database error: {str(e)}', 500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8083, debug=True)