#!/usr/bin/env python3
"""
Auth Test: Token Refresh Flow  
Tests the /refresh endpoint for access token renewal
"""

import asyncio
import aiohttp
import sys
import os
import jwt
from datetime import datetime, timezone, timedelta

# Add shared modules to path
sys.path.append('../../shared')
sys.path.append('../../schemas')

from database import db

# Test configuration
AUTH_URL = "http://localhost:8081"
TEST_USER_EMAIL = "token-refresh-test@example.com"
TEST_USER_NAME = "Token Refresh Test User"

async def test_token_refresh_flow():
    """Test complete token refresh flow with /refresh endpoint"""
    print("🧪 Testing Token Refresh Flow...")
    
    session = None
    try:
        session = aiohttp.ClientSession()
        await db.connect()
        
        # Clean any existing test data
        users_collection = await db.get_users_collection()
        tokens_collection = await db.get_refresh_tokens_collection()
        await users_collection.delete_many({"email": TEST_USER_EMAIL})
        await tokens_collection.delete_many({"userId": {"$regex": "token-refresh-test"}})
        
        # Step 1: Create user and get initial tokens
        print("  → Creating user and getting initial tokens...")
        login_data = {
            "email": TEST_USER_EMAIL,
            "name": TEST_USER_NAME,
            "avatar": "test-avatar.jpg"
        }
        
        initial_access_token = None
        refresh_token = None
        user_id = None
        
        async with session.post(f"{AUTH_URL}/google-auth", json=login_data) as resp:
            if resp.status != 200:
                print(f"  ❌ Initial login failed: {resp.status}")
                return False
            
            result = await resp.json()
            data = result.get('data', {})
            initial_access_token = data['token']
            refresh_token = data['refreshToken']
            user_id = data['user']['id']
        
        if not all([initial_access_token, refresh_token, user_id]):
            print("  ❌ Missing initial tokens or user ID")
            return False
        
        print("  ✅ Initial tokens obtained")
        
        # Step 2: Test successful token refresh
        print("  → Testing successful token refresh...")
        refresh_data = {"refreshToken": refresh_token}
        
        new_access_token = None
        async with session.post(f"{AUTH_URL}/refresh", json=refresh_data) as resp:
            if resp.status != 200:
                error_text = await resp.text()
                print(f"  ❌ Token refresh failed: {resp.status} - {error_text}")
                return False
            
            result = await resp.json()
            data = result.get('data', {})
            new_access_token = data.get('token')
            
            if not new_access_token:
                print(f"  ❌ No new access token in response: {data}")
                return False
            
            # Verify it's a different token
            if new_access_token == initial_access_token:
                print("  ❌ New token is same as old token")
                return False
        
        print("  ✅ Token refresh successful")
        
        # Step 3: Validate new token structure
        print("  → Validating new token structure...")
        
        try:
            # Decode without verification to check structure
            decoded = jwt.decode(new_access_token, options={"verify_signature": False})
            
            # Check required fields
            required_fields = ['user_id', 'email', 'role', 'exp', 'iat']
            if not all(field in decoded for field in required_fields):
                print(f"  ❌ Missing required fields in token: {decoded}")
                return False
            
            # Check user ID matches
            if decoded['user_id'] != user_id:
                print(f"  ❌ Token user_id mismatch: {decoded['user_id']} vs {user_id}")
                return False
        
        except Exception as e:
            print(f"  ❌ Token decode failed: {e}")
            return False
        
        print("  ✅ New token structure valid")
        
        # Step 4: Test invalid refresh token
        print("  → Testing invalid refresh token...")
        
        invalid_refresh_data = {"refreshToken": "invalid.refresh.token"}
        async with session.post(f"{AUTH_URL}/refresh", json=invalid_refresh_data) as resp:
            if resp.status == 200:
                print("  ❌ Invalid refresh token was accepted")
                return False
            
            # Should return 401 Unauthorized
            if resp.status != 401:
                print(f"  ❌ Expected 401, got {resp.status}")
                return False
        
        print("  ✅ Invalid refresh token properly rejected")
        
        # Step 5: Test missing refresh token
        print("  → Testing missing refresh token...")
        
        async with session.post(f"{AUTH_URL}/refresh", json={}) as resp:
            if resp.status != 400:
                print(f"  ❌ Expected 400 for missing token, got {resp.status}")
                return False
        
        print("  ✅ Missing refresh token properly rejected")
        
        # Step 6: Test refresh token after logout
        print("  → Testing refresh token after logout...")
        
        # Logout (remove refresh token)
        logout_data = {"refreshToken": refresh_token}
        async with session.post(f"{AUTH_URL}/logout", json=logout_data) as resp:
            if resp.status != 200:
                print(f"  ❌ Logout failed: {resp.status}")
                return False
        
        # Try to use refresh token after logout
        async with session.post(f"{AUTH_URL}/refresh", json=refresh_data) as resp:
            if resp.status == 200:
                print("  ❌ Refresh token worked after logout")
                return False
            
            if resp.status != 401:
                print(f"  ❌ Expected 401 after logout, got {resp.status}")
                return False
        
        print("  ✅ Refresh token properly invalidated after logout")
        
        # Step 7: Test global token cleanup during refresh
        print("  → Testing global token cleanup during refresh...")
        
        # Create new session with tokens
        async with session.post(f"{AUTH_URL}/google-auth", json=login_data) as resp:
            if resp.status != 200:
                print(f"  ❌ Failed to create new session: {resp.status}")
                return False
            
            result = await resp.json()
            data = result.get('data', {})
            new_refresh_token = data['refreshToken']
        
        # Manually create expired token in database
        expired_token_data = {
            "userId": "fake-user-id",
            "token": "fake.expired.token",
            "createdAt": datetime.now(timezone.utc) - timedelta(days=40),
            "expiresAt": datetime.now(timezone.utc) - timedelta(days=10)  # Expired
        }
        await tokens_collection.insert_one(expired_token_data)
        
        # Count tokens before refresh
        tokens_before = await tokens_collection.count_documents({})
        
        # Do refresh (should trigger cleanup)
        refresh_data = {"refreshToken": new_refresh_token}
        async with session.post(f"{AUTH_URL}/refresh", json=refresh_data) as resp:
            if resp.status != 200:
                print(f"  ❌ Refresh failed: {resp.status}")
                return False
        
        # Count tokens after refresh
        tokens_after = await tokens_collection.count_documents({})
        
        # Should have cleaned up expired token
        if tokens_after >= tokens_before:
            print(f"  ❌ Token cleanup didn't work. Before: {tokens_before}, After: {tokens_after}")
            return False
        
        print("  ✅ Global token cleanup during refresh successful")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Exception: {e}")
        return False
    finally:
        if session:
            await session.close()
        # Cleanup test data
        try:
            await users_collection.delete_many({"email": TEST_USER_EMAIL})
            await tokens_collection.delete_many({"userId": user_id}) if user_id else None
            await tokens_collection.delete_many({"userId": "fake-user-id"})
        except:
            pass

async def main():
    """Run token refresh flow test"""
    from dotenv import load_dotenv
    load_dotenv('../../.env')
    
    success = await test_token_refresh_flow()
    return 0 if success else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)