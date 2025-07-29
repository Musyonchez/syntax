# Auth Function - Google OAuth + JWT authentication
# Port: 8081

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
from users import UserSchema
from tokens import RefreshTokenSchema

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))

app = Flask(__name__)

# Configure CORS
allowed_origins = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')
CORS(app, origins=allowed_origins)

# Initialize auth utils
auth_utils = AuthUtils(os.getenv('JWT_SECRET'))

@app.route('/health')
def health():
    return create_response({'status': 'ok', 'service': 'auth'})

@app.route('/google-auth', methods=['POST'])
def google_auth():
    """Handle Google OAuth authentication"""
    try:
        print("=== DEBUG: /google-auth endpoint called ===")
        data = request.get_json()
        print(f"DEBUG: Received data: {data}")
        
        if not data:
            print("DEBUG: No JSON data received")
            return create_error_response("Invalid JSON data", 400)
        
        # Validate data using schema
        try:
            user_data = UserSchema.validate_create(data)
            print(f"DEBUG: Schema validated data - email: {user_data['email']}, name: {user_data['name']}")
        except ValueError as e:
            print(f"DEBUG: Schema validation failed: {e}")
            return create_error_response(f"Validation error: {str(e)}", 400)
        
        print("DEBUG: Starting async operations")
        # Reset database connection for new event loop
        db.client = None
        db.db = None
        
        # Run async operations
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(_handle_google_auth(user_data))
            print("DEBUG: Async operation completed successfully")
            print(f"DEBUG: Result type: {type(result)}")
            print(f"DEBUG: Result content: {result}")
            return result
        except Exception as async_error:
            print(f"DEBUG: Async operation failed: {async_error}")
            raise async_error
            
    except Exception as e:
        print(f"DEBUG: Main exception caught: {e}")
        import traceback
        traceback.print_exc()
        return create_error_response(f"Authentication failed: {str(e)}", 500)

async def _handle_google_auth(validated_data: dict):
    """Async handler for Google authentication"""
    try:
        print("DEBUG: Getting users collection")
        users_collection = await db.get_users_collection()
        print("DEBUG: Users collection obtained")
        
        # Find or create user (use email as primary lookup)
        user = await users_collection.find_one({"email": validated_data["email"]})
        print(f"DEBUG: User lookup by email: {user}")
        
        if not user:
            # Create new user using validated data
            result = await users_collection.insert_one(validated_data)
            validated_data["_id"] = str(result.inserted_id)
            user = validated_data
            print("DEBUG: Created new user")
        else:
            # Use schema to validate update data
            update_data = {
                "name": validated_data["name"],
                "avatar": validated_data["avatar"]
            }
            
            try:
                updatable_fields = UserSchema.validate_update(update_data)
            except ValueError as e:
                print(f"DEBUG: Update validation failed: {e}")
                updatable_fields = {}
            
            # Always update lastLoginAt
            update_fields = {
                "lastLoginAt": datetime.now(timezone.utc)
            }
            
            # Check if any updatable field actually changed
            profile_changed = any(
                user.get(field) != new_value 
                for field, new_value in updatable_fields.items()
            )
            
            # Only update profile data and updatedAt if something actually changed
            if profile_changed:
                update_fields.update(updatable_fields)  # Add all updatable fields
                update_fields["updatedAt"] = datetime.now(timezone.utc)
                changed_fields = [
                    field for field, new_value in updatable_fields.items() 
                    if user.get(field) != new_value
                ]
                print(f"DEBUG: Profile data changed ({', '.join(changed_fields)}), updating user profile")
            else:
                print("DEBUG: Profile unchanged, only updating lastLoginAt")
            
            await users_collection.update_one(
                {"_id": user["_id"]},
                {"$set": update_fields}
            )
            user["_id"] = str(user["_id"])
        
        # Create tokens
        access_token = auth_utils.create_access_token(user)
        refresh_token = auth_utils.create_refresh_token(user["_id"])
        
        # Store refresh token (limit to 2 tokens per user)
        refresh_tokens_collection = await db.get_refresh_tokens_collection()
        
        # Clean expired tokens for this user first
        expired_result = await refresh_tokens_collection.delete_many({
            "userId": user["_id"],
            "expiresAt": {"$lt": datetime.now(timezone.utc)}
        })
        if expired_result.deleted_count > 0:
            print(f"DEBUG: Cleaned {expired_result.deleted_count} expired tokens for user {user['_id']}")
        
        # Check current token count for user (after cleanup)
        current_token_count = await refresh_tokens_collection.count_documents({"userId": user["_id"]})
        
        # If user already has 2 or more tokens, remove excess tokens (keep only 1, so we can add 1 more)
        if current_token_count >= 2:
            # Find all tokens for user, sorted by creation date (oldest first)
            existing_tokens = await refresh_tokens_collection.find(
                {"userId": user["_id"]},
                sort=[("createdAt", 1)]
            ).to_list(length=None)
            
            # Remove all but the newest token (keep only 1, so total will be 2 after insert)
            tokens_to_remove = existing_tokens[:-1]  # All except the last (newest) one
            
            if tokens_to_remove:
                token_ids_to_remove = [token["_id"] for token in tokens_to_remove]
                result = await refresh_tokens_collection.delete_many({"_id": {"$in": token_ids_to_remove}})
                print(f"DEBUG: Removed {result.deleted_count} old refresh tokens for user {user['_id']}")
        
        # Insert new refresh token using schema
        try:
            token_data = RefreshTokenSchema.validate_create(
                user["_id"], 
                refresh_token, 
                auth_utils.refresh_token_expiry.days
            )
            await refresh_tokens_collection.insert_one(token_data)
        except ValueError as e:
            print(f"DEBUG: Token validation failed: {e}")
            return create_error_response(f"Token creation failed: {str(e)}", 500)
        
        # Return user data and tokens
        response_data = {
            "token": access_token,
            "refreshToken": refresh_token,
            "user": {
                "id": user["_id"],
                "email": user["email"],
                "name": user["name"],
                "avatar": user["avatar"],
                "role": user["role"]
            }
        }
        
        print(f"DEBUG: Response data structure: {response_data}")
        
        response = create_response(response_data, "Authentication successful")
        print(f"DEBUG: Final response type: {type(response)}")
        print(f"DEBUG: Final response content: {response}")
        return response
        
    except Exception as e:
        print(f"DEBUG: Database error: {e}")
        import traceback
        traceback.print_exc()
        return create_error_response(f"Database error: {str(e)}", 500)

@app.route('/refresh', methods=['POST'])
def refresh_token():
    """Refresh access token using refresh token"""
    try:
        data = request.get_json()
        if not data or not data.get('refreshToken'):
            return create_error_response("Refresh token required", 400)
        
        refresh_token = data.get('refreshToken')
        
        # Run async operations
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(_handle_refresh_token(refresh_token))
            return result
        finally:
            loop.close()
            
    except Exception as e:
        return create_error_response(f"Token refresh failed: {str(e)}", 500)

async def _handle_refresh_token(refresh_token: str):
    """Async handler for token refresh"""
    try:
        # Verify refresh token
        payload = auth_utils.verify_token(refresh_token, "refresh")
        if not payload:
            return create_error_response("Invalid refresh token", 401)
        
        user_id = payload.get("user_id")
        
        # Check if refresh token exists in database
        refresh_tokens_collection = await db.get_refresh_tokens_collection()
        
        # Clean expired tokens globally (small batch to keep database clean)
        expired_cleanup = await refresh_tokens_collection.delete_many({
            "expiresAt": {"$lt": datetime.now(timezone.utc)}
        })
        if expired_cleanup.deleted_count > 0:
            print(f"DEBUG: Global cleanup removed {expired_cleanup.deleted_count} expired tokens")
        
        stored_token = await refresh_tokens_collection.find_one({
            "userId": user_id,
            "token": refresh_token
        })
        
        if not stored_token:
            return create_error_response("Refresh token not found", 401)
        
        # Get user data
        users_collection = await db.get_users_collection()
        user = await users_collection.find_one({"_id": user_id})
        
        if not user:
            return create_error_response("User not found", 401)
        
        user["_id"] = str(user["_id"])
        
        # Create new access token
        new_access_token = auth_utils.create_access_token(user)
        
        return create_response({
            "token": new_access_token,
            "user": {
                "id": user["_id"],
                "email": user["email"],
                "name": user["name"],
                "avatar": user["avatar"],
                "role": user["role"]
            }
        }, "Token refreshed successfully")
        
    except Exception as e:
        return create_error_response(f"Database error: {str(e)}", 500)

@app.route('/logout-all', methods=['POST'])
def logout_all():
    """Revoke all refresh tokens for a user (sign out all devices)"""
    try:
        # Get authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return create_error_response("Authorization token required", 401)
        
        access_token = auth_header.split(' ')[1]
        
        # Verify access token
        payload = auth_utils.verify_token(access_token, "access")
        if not payload:
            return create_error_response("Invalid access token", 401)
        
        user_id = payload.get("user_id")
        if not user_id:
            return create_error_response("Invalid token payload", 401)
        
        # Reset database connection for new event loop
        db.client = None
        db.db = None
        
        # Run async operations
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(_handle_logout_all(user_id))
            return result
        except Exception as async_error:
            print(f"DEBUG: Logout all async operation failed: {async_error}")
            raise async_error
            
    except Exception as e:
        print(f"DEBUG: Logout all exception: {e}")
        return create_error_response(f"Logout all failed: {str(e)}", 500)

async def _handle_logout_all(user_id: str):
    """Async handler for logging out all devices"""
    try:
        print(f"DEBUG: Logging out all devices for user {user_id}")
        
        # Get refresh tokens collection
        refresh_tokens_collection = await db.get_refresh_tokens_collection()
        
        # Delete all refresh tokens for this user
        result = await refresh_tokens_collection.delete_many({"userId": user_id})
        
        print(f"DEBUG: Revoked {result.deleted_count} refresh tokens for user {user_id}")
        
        return create_response({
            "revokedTokens": result.deleted_count
        }, "Successfully signed out of all devices")
        
    except Exception as e:
        print(f"DEBUG: Logout all database error: {e}")
        return create_error_response(f"Database error: {str(e)}", 500)

@app.route('/logout', methods=['POST'])
def logout():
    """Logout from current device (revoke single refresh token)"""
    try:
        data = request.get_json()
        if not data or not data.get('refreshToken'):
            return create_error_response("Refresh token required", 400)
        
        refresh_token = data.get('refreshToken')
        
        # Reset database connection for new event loop
        db.client = None
        db.db = None
        
        # Run async operations
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(_handle_logout(refresh_token))
            return result
        except Exception as async_error:
            print(f"DEBUG: Logout async operation failed: {async_error}")
            raise async_error
            
    except Exception as e:
        print(f"DEBUG: Logout exception: {e}")
        return create_error_response(f"Logout failed: {str(e)}", 500)

async def _handle_logout(refresh_token: str):
    """Async handler for single device logout"""
    try:
        print(f"DEBUG: Processing logout for refresh token")
        
        # Get refresh tokens collection
        refresh_tokens_collection = await db.get_refresh_tokens_collection()
        
        # Find and delete the specific refresh token
        result = await refresh_tokens_collection.delete_one({"token": refresh_token})
        
        if result.deleted_count > 0:
            print(f"DEBUG: Successfully revoked refresh token")
            return create_response({
                "revokedToken": True
            }, "Successfully logged out")
        else:
            print(f"DEBUG: Refresh token not found in database")
            # Still return success - token might have already expired/been cleaned
            return create_response({
                "revokedToken": False
            }, "Logout completed (token not found)")
        
    except Exception as e:
        print(f"DEBUG: Logout database error: {e}")
        return create_error_response(f"Database error: {str(e)}", 500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)