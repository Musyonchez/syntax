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
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        async def fetch_snippets():
            collection = await db.get_personal_snippets_collection()
            cursor = collection.find(query).sort('updatedAt', -1)
            snippets = []
            async for snippet in cursor:
                snippet['_id'] = str(snippet['_id'])
                snippets.append(snippet)
            return snippets
        
        snippets = loop.run_until_complete(fetch_snippets())
        loop.close()
        
        return create_response({
            'snippets': snippets,
            'count': len(snippets)
        }, 'Personal snippets retrieved successfully')
        
    except Exception as e:
        return create_error_response(f'Failed to get personal snippets: {str(e)}', 500)

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
        
        # Get request data
        data = request.get_json()
        if not data:
            return create_error_response('Request body is required', 400)
        
        # Add user ID to data
        data['userId'] = user_id
        
        # Validate data
        try:
            clean_data = PersonalSnippetSchema.validate_create(data)
        except ValueError as e:
            return create_error_response(str(e), 400)
        
        # Save to database
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        async def save_snippet():
            collection = await db.get_personal_snippets_collection()
            result = await collection.insert_one(clean_data)
            clean_data['_id'] = str(result.inserted_id)
            return clean_data
        
        snippet = loop.run_until_complete(save_snippet())
        loop.close()
        
        return create_response(snippet, 'Personal snippet created successfully')
        
    except Exception as e:
        return create_error_response(f'Failed to create personal snippet: {str(e)}', 500)

@app.route('/personal/<snippet_id>', methods=['PUT'])
def update_personal_snippet(snippet_id):
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
        
        # Get request data
        data = request.get_json()
        if not data:
            return create_error_response('Request body is required', 400)
        
        # Validate update data
        try:
            update_data = PersonalSnippetSchema.validate_update(data)
        except ValueError as e:
            return create_error_response(str(e), 400)
        
        if not update_data:
            return create_error_response('No valid fields to update', 400)
        
        # Update in database
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        async def update_snippet():
            from bson import ObjectId
            collection = await db.get_personal_snippets_collection()
            
            # Verify ownership
            snippet = await collection.find_one({
                '_id': ObjectId(snippet_id), 
                'userId': user_id,
                'isActive': True
            })
            if not snippet:
                return None
            
            # Update snippet
            result = await collection.update_one(
                {'_id': ObjectId(snippet_id)},
                {'$set': update_data}
            )
            
            if result.modified_count > 0:
                updated_snippet = await collection.find_one({'_id': ObjectId(snippet_id)})
                updated_snippet['_id'] = str(updated_snippet['_id'])
                return updated_snippet
            return None
        
        snippet = loop.run_until_complete(update_snippet())
        loop.close()
        
        if not snippet:
            return create_error_response('Snippet not found or no changes made', 404)
        
        return create_response(snippet, 'Personal snippet updated successfully')
        
    except Exception as e:
        return create_error_response(f'Failed to update personal snippet: {str(e)}', 500)

@app.route('/personal/<snippet_id>', methods=['DELETE'])
def delete_personal_snippet(snippet_id):
    """Soft delete a personal snippet"""
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
        
        # Soft delete in database
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        async def delete_snippet():
            from bson import ObjectId
            collection = await db.get_personal_snippets_collection()
            
            result = await collection.update_one(
                {
                    '_id': ObjectId(snippet_id), 
                    'userId': user_id,
                    'isActive': True
                },
                {
                    '$set': {
                        'isActive': False,
                        'updatedAt': datetime.now(timezone.utc)
                    }
                }
            )
            return result.modified_count > 0
        
        deleted = loop.run_until_complete(delete_snippet())
        loop.close()
        
        if not deleted:
            return create_error_response('Snippet not found', 404)
        
        return create_response({}, 'Personal snippet deleted successfully')
        
    except Exception as e:
        return create_error_response(f'Failed to delete personal snippet: {str(e)}', 500)

# =============================================================================
# OFFICIAL SNIPPETS ENDPOINTS
# =============================================================================

@app.route('/official', methods=['GET'])
def get_official_snippets():
    """Get published official snippets with optional filtering"""
    try:
        # Get query parameters for filtering
        language = request.args.get('language')
        difficulty = request.args.get('difficulty')
        category = request.args.get('category')
        tag = request.args.get('tag')
        search = request.args.get('search')
        
        # Build query - only published snippets
        query = {'isPublished': True}
        
        if language:
            query['language'] = language.lower()
        if difficulty and difficulty in ['easy', 'medium', 'hard']:
            query['difficulty'] = difficulty.lower()
        if category:
            query['category'] = category.lower()
        if tag:
            query['tags'] = {'$in': [tag.lower()]}
        if search:
            query['$or'] = [
                {'title': {'$regex': search, '$options': 'i'}},
                {'description': {'$regex': search, '$options': 'i'}},
                {'learningObjectives': {'$elemMatch': {'$regex': search, '$options': 'i'}}}
            ]
        
        # Execute query
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        async def fetch_snippets():
            collection = await db.get_official_snippets_collection()
            cursor = collection.find(query).sort('createdAt', -1)
            snippets = []
            async for snippet in cursor:
                snippet['_id'] = str(snippet['_id'])
                snippets.append(snippet)
            return snippets
        
        snippets = loop.run_until_complete(fetch_snippets())
        loop.close()
        
        return create_response({
            'snippets': snippets,
            'count': len(snippets)
        }, 'Official snippets retrieved successfully')
        
    except Exception as e:
        return create_error_response(f'Failed to get official snippets: {str(e)}', 500)

@app.route('/official/<snippet_id>', methods=['GET'])
def get_official_snippet(snippet_id):
    """Get a specific official snippet by ID"""
    try:
        # Get snippet from database
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        async def fetch_snippet():
            from bson import ObjectId
            collection = await db.get_official_snippets_collection()
            snippet = await collection.find_one({
                '_id': ObjectId(snippet_id),
                'isPublished': True
            })
            if snippet:
                snippet['_id'] = str(snippet['_id'])
            return snippet
        
        snippet = loop.run_until_complete(fetch_snippet())
        loop.close()
        
        if not snippet:
            return create_error_response('Official snippet not found', 404)
        
        return create_response(snippet, 'Official snippet retrieved successfully')
        
    except Exception as e:
        return create_error_response(f'Failed to get official snippet: {str(e)}', 500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8083, debug=True)