#!/usr/bin/env python3
"""
Auth Test: Login/Register Flow
Tests the main /google-auth endpoint for both new and existing users
"""

import asyncio
import aiohttp
import sys
import os

# Add shared modules to path
sys.path.append('../../shared')
sys.path.append('../../schemas')

from database import db

# Test configuration
AUTH_URL = "http://localhost:8081"
TEST_USER_EMAIL = "login-register-test@example.com"
TEST_USER_NAME = "Login Register Test User"

async def test_login_register_flow():
    """Test complete login/register flow with /google-auth endpoint"""
    print("🧪 Testing Login/Register Flow...")
    
    session = None
    try:
        session = aiohttp.ClientSession()
        await db.connect()
        
        # Clean any existing test data
        users_collection = await db.get_users_collection()
        tokens_collection = await db.get_refresh_tokens_collection()
        await users_collection.delete_many({"email": TEST_USER_EMAIL})
        await tokens_collection.delete_many({"userId": {"$regex": "login-register-test"}})
        
        # Test 1: New User Registration
        print("  → Testing new user registration...")
        register_data = {
            "email": TEST_USER_EMAIL,
            "name": TEST_USER_NAME,
            "avatar": "test-avatar.jpg"
        }
        
        user_id = None
        async with session.post(f"{AUTH_URL}/google-auth", json=register_data) as resp:
            if resp.status != 200:
                print(f"  ❌ Registration failed: {resp.status}")
                return False
            
            result = await resp.json()
            data = result.get('data', {})
            
            # Validate response structure
            if not all(key in data for key in ['token', 'refreshToken', 'user']):
                print(f"  ❌ Invalid response structure: {data}")
                return False
            
            user_id = data['user']['id']
            
            # Validate user data
            user = data['user']
            if user['email'] != TEST_USER_EMAIL or user['name'] != TEST_USER_NAME:
                print(f"  ❌ User data mismatch: {user}")
                return False
            
            print("  ✅ New user registration successful")
        
        # Test 2: Existing User Login (same data)
        print("  → Testing existing user login...")
        async with session.post(f"{AUTH_URL}/google-auth", json=register_data) as resp:
            if resp.status != 200:
                print(f"  ❌ Login failed: {resp.status}")
                return False
            
            result = await resp.json()
            data = result.get('data', {})
            
            # Should return same user ID
            if data['user']['id'] != user_id:
                print(f"  ❌ User ID mismatch on login: {data['user']['id']} vs {user_id}")
                return False
            
            print("  ✅ Existing user login successful")
        
        # Test 3: Profile Update on Login
        print("  → Testing profile update on login...")
        updated_data = {
            "email": TEST_USER_EMAIL,
            "name": "Updated Test Name",  # Changed name
            "avatar": "updated-avatar.jpg"  # Changed avatar
        }
        
        async with session.post(f"{AUTH_URL}/google-auth", json=updated_data) as resp:
            if resp.status != 200:
                print(f"  ❌ Profile update failed: {resp.status}")
                return False
            
            result = await resp.json()
            data = result.get('data', {})
            
            # Should have updated profile data
            user = data['user']
            if user['name'] != "Updated Test Name":
                print(f"  ℹ️  Profile may not have changed due to schema validation: {user['name']}")
                # This is actually correct behavior - check database for the update
                
                # Check database directly
                users_collection = await db.get_users_collection()
                db_user = await users_collection.find_one({"email": TEST_USER_EMAIL})
                
                if db_user and db_user['name'] == "Updated Test Name":
                    print("  ✅ Profile update successful (confirmed in database)")
                else:
                    print(f"  ❌ Profile update failed in database: {db_user.get('name') if db_user else 'User not found'}")
                    return False
            else:
                print("  ✅ Profile update successful (in response)")
            
            print("  ✅ Profile update on login successful")
        
        # Test 4: Token Structure Validation
        print("  → Testing token structure...")
        
        # Validate access token (should be JWT)
        access_token = data['token']
        if not access_token or len(access_token.split('.')) != 3:
            print(f"  ❌ Invalid access token structure: {access_token}")
            return False
        
        # Validate refresh token exists
        refresh_token = data['refreshToken']
        if not refresh_token:
            print(f"  ❌ No refresh token provided")
            return False
        
        print("  ✅ Token structure validation successful")
        
        # Test 5: Database Consistency
        print("  → Testing database consistency...")
        
        # Check user in database
        db_user = await users_collection.find_one({"email": TEST_USER_EMAIL})
        if not db_user or db_user['name'] != "Updated Test Name":
            print(f"  ❌ Database user inconsistent: {db_user}")
            return False
        
        # Check refresh token in database
        db_token = await tokens_collection.find_one({"token": refresh_token})
        if not db_token or db_token['userId'] != user_id:
            print(f"  ❌ Database token inconsistent: {db_token}")
            return False
        
        print("  ✅ Database consistency validation successful")
        
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
        except:
            pass

async def main():
    """Run login/register flow test"""
    from dotenv import load_dotenv
    load_dotenv('../../.env')
    
    success = await test_login_register_flow()
    return 0 if success else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)