#!/usr/bin/env python3
"""
Auth Test: Concurrent Login Handling
Tests multiple simultaneous login requests and race conditions
"""

import asyncio
import aiohttp
import sys
import os
from datetime import datetime, timezone

# Add shared modules to path
sys.path.append('../../shared')
sys.path.append('../../schemas')

from database import db

# Test configuration
AUTH_URL = "http://localhost:8081"
TEST_USER_EMAIL = "concurrent-test@example.com"
TEST_USER_NAME = "Concurrent Test User"

async def test_concurrent_login_handling():
    """Test concurrent login requests and race conditions"""
    print("🧪 Testing Concurrent Login Handling...")
    
    try:
        await db.connect()
        
        # Clean any existing test data
        users_collection = await db.get_users_collection()
        tokens_collection = await db.get_refresh_tokens_collection()
        await tokens_collection.delete_many({"userId": {"$regex": "concurrent-test"}})
        
        # Test 1: Concurrent New User Registration
        print("  → Testing concurrent new user registration...")
        
        login_data = {
            "email": TEST_USER_EMAIL,
            "name": TEST_USER_NAME,
            "avatar": "test-avatar.jpg"
        }
        
        # Create multiple concurrent sessions
        sessions = [aiohttp.ClientSession() for _ in range(5)]
        
        try:
            # Launch 5 concurrent registration requests
            tasks = []
            for session in sessions:
                task = session.post(f"{AUTH_URL}/google-auth", json=login_data)
                tasks.append(task)
            
            # Wait for all requests to complete
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            
            successful_responses = []
            for i, response in enumerate(responses):
                if isinstance(response, Exception):
                    print(f"  ❌ Request {i+1} failed with exception: {response}")
                    return False
                
                if response.status == 200:
                    result = await response.json()
                    successful_responses.append(result)
                    response.close()
                else:
                    print(f"  ❌ Request {i+1} failed with status: {response.status}")
                    response.close()
                    return False
            
            # All requests should succeed
            if len(successful_responses) != 5:
                print(f"  ❌ Expected 5 successful responses, got {len(successful_responses)}")
                return False
            
            # All should return the same user ID (same user created)
            user_ids = [resp.get('data', {}).get('user', {}).get('id') for resp in successful_responses]
            unique_user_ids = set(user_ids)
            
            if len(unique_user_ids) != 1:
                print(f"  ❌ Expected 1 unique user ID, got {len(unique_user_ids)}: {unique_user_ids}")
                return False
            
            print("  ✅ Concurrent new user registration handled correctly")
            
            # Check database consistency
            db_users = await users_collection.count_documents({"email": TEST_USER_EMAIL})
            if db_users != 1:
                print(f"  ❌ Expected 1 user in database, found {db_users}")
                return False
            
            print("  ✅ Database consistency maintained during concurrent registration")
            
        finally:
            # Close all sessions
            for session in sessions:
                await session.close()
        
        # Test 2: Concurrent Existing User Login
        print("  → Testing concurrent existing user login...")
        
        sessions = [aiohttp.ClientSession() for _ in range(5)]
        
        try:
            # Launch 5 concurrent login requests for existing user
            tasks = []
            for session in sessions:
                task = session.post(f"{AUTH_URL}/google-auth", json=login_data)
                tasks.append(task)
            
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            
            successful_responses = []
            for i, response in enumerate(responses):
                if isinstance(response, Exception):
                    print(f"  ❌ Login request {i+1} failed with exception: {response}")
                    return False
                
                if response.status == 200:
                    result = await response.json()
                    successful_responses.append(result)
                    response.close()
                else:
                    print(f"  ❌ Login request {i+1} failed with status: {response.status}")
                    response.close()
                    return False
            
            if len(successful_responses) != 5:
                print(f"  ❌ Expected 5 successful login responses, got {len(successful_responses)}")
                return False
            
            print("  ✅ Concurrent existing user login handled correctly")
            
        finally:
            for session in sessions:
                await session.close()
        
        # Test 3: Concurrent Profile Updates
        print("  → Testing concurrent profile updates...")
        
        # Different profile data for each request
        profile_updates = [
            {"email": TEST_USER_EMAIL, "name": f"Updated Name {i}", "avatar": f"avatar{i}.jpg"}
            for i in range(3)
        ]
        
        sessions = [aiohttp.ClientSession() for _ in range(3)]
        
        try:
            # Launch concurrent profile update requests
            tasks = []
            for i, session in enumerate(sessions):
                task = session.post(f"{AUTH_URL}/google-auth", json=profile_updates[i])
                tasks.append(task)
            
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            
            successful_count = 0
            for i, response in enumerate(responses):
                if isinstance(response, Exception):
                    print(f"  ❌ Profile update {i+1} failed with exception: {response}")
                    return False
                
                if response.status == 200:
                    successful_count += 1
                    response.close()
                else:
                    print(f"  ❌ Profile update {i+1} failed with status: {response.status}")
                    response.close()
                    return False
            
            if successful_count != 3:
                print(f"  ❌ Expected 3 successful profile updates, got {successful_count}")
                return False
            
            # Check final user state in database
            final_user = await users_collection.find_one({"email": TEST_USER_EMAIL})
            if not final_user:
                print("  ❌ User not found after profile updates")
                return False
            
            # One of the updates should have won
            final_name = final_user.get('name', '')
            expected_names = [f"Updated Name {i}" for i in range(3)]
            
            if final_name not in expected_names:
                print(f"  ❌ Unexpected final name: {final_name}")
                return False
            
            print("  ✅ Concurrent profile updates handled correctly")
            
        finally:
            for session in sessions:
                await session.close()
        
        # Test 4: Token Limit Under Concurrent Load
        print("  → Testing token limits under concurrent load...")
        
        # Create many concurrent sessions (more than 2-token limit)
        sessions = [aiohttp.ClientSession() for _ in range(10)]
        
        try:
            tasks = []
            for session in sessions:
                task = session.post(f"{AUTH_URL}/google-auth", json=login_data)
                tasks.append(task)
            
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            
            successful_count = 0
            for i, response in enumerate(responses):
                if isinstance(response, Exception):
                    print(f"  ❌ Concurrent token request {i+1} failed: {response}")
                    return False
                
                if response.status == 200:
                    successful_count += 1
                    response.close()
                else:
                    response.close()
                    return False
            
            if successful_count != 10:
                print(f"  ❌ Expected 10 successful token requests, got {successful_count}")
                return False
            
            # Check that token limit is still enforced
            user_id = (await users_collection.find_one({"email": TEST_USER_EMAIL}))["_id"]
            final_token_count = await tokens_collection.count_documents({"userId": str(user_id)})
            
            if final_token_count > 2:
                print(f"  ❌ Token limit violated: {final_token_count} tokens exist")
                return False
            
            print("  ✅ Token limits maintained under concurrent load")
            
        finally:
            for session in sessions:
                await session.close()
        
        return True
        
    except Exception as e:
        print(f"  ❌ Exception: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:

async def main():
    """Run concurrent login handling tests"""
    from dotenv import load_dotenv
    load_dotenv('../../.env')
    
    success = await test_concurrent_login_handling()
    return 0 if success else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)