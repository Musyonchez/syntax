#!/usr/bin/env python3
"""
Snippets Test: Official Snippet Creation
Tests creating a new official snippet with admin permissions
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
SNIPPETS_URL = "http://localhost:8083"
TEST_ADMIN_EMAIL = "admin.test.official@example.com"
TEST_ADMIN_NAME = "Admin Test User"

async def test_official_snippet_create():
    """Test creating an official snippet with admin permissions"""
    print("🧪 Testing official snippet creation...")
    
    session = None
    admin_user_id = None
    try:
        session = aiohttp.ClientSession()
        await db.connect()
        
        # Clean any existing test data
        users_collection = await db.get_users_collection()
        tokens_collection = await db.get_refresh_tokens_collection()
        official_collection = await db.get_official_snippets_collection()
        
        await users_collection.delete_many({"email": TEST_ADMIN_EMAIL})
        await tokens_collection.delete_many({"userId": {"$regex": "admin-test"}})
        await official_collection.delete_many({"createdBy": {"$regex": "admin-test"}})
        
        # Step 1: Create admin user and get tokens
        print("  → Creating admin user and getting tokens...")
        admin_data = {
            "email": TEST_ADMIN_EMAIL,
            "name": TEST_ADMIN_NAME,
            "avatar": "admin-avatar.jpg",
            "role": "admin"  # Make this user an admin
        }
        
        admin_token = None
        async with session.post(f"{AUTH_URL}/google-auth", json=admin_data) as resp:
            if resp.status != 200:
                error_text = await resp.text()
                print(f"  ❌ Admin user creation failed: {resp.status} - {error_text}")
                return False
            
            result = await resp.json()
            data = result.get('data', {})
            admin_token = data['token']
            admin_user_id = data['user']['id']
            admin_role = data['user']['role']
            
            if admin_role != 'admin':
                print(f"  ❌ User role is {admin_role}, expected admin")
                return False
        
        print(f"  ✅ Admin user created with role: {admin_role}")
        
        # Step 2: Test creating official snippet with admin token
        print("  → Creating official snippet...")
        official_data = {
            "title": "Official Array Methods",
            "description": "Learn essential JavaScript array methods",
            "code": "const arr = [1, 2, 3];\nconst doubled = arr.map(x => x * 2);\nconsole.log(doubled);",
            "language": "javascript",
            "category": "arrays",
            "tags": ["javascript", "arrays", "map"],
            "difficulty": "medium",
            "learningObjectives": ["Understand map function", "Array transformation"],
            "hints": "The map method creates a new array",
            "solution": "Use map() to transform each element",
            "estimatedTime": 300
        }
        
        headers = {"Authorization": f"Bearer {admin_token}"}
        async with session.post(
            f"{SNIPPETS_URL}/official",
            json=official_data,
            headers=headers
        ) as response:
            data = await response.json()
            
            if response.status != 200:
                print(f"  ❌ Official snippet creation failed: {response.status} - {data}")
                return False
            
            # Verify response structure
            if not data.get('success'):
                print(f"  ❌ Response not successful: {data}")
                return False
            
            snippet = data.get('data')
            if not snippet or not snippet.get('_id'):
                print(f"  ❌ No snippet ID returned: {data}")
                return False
            
            # Verify data integrity
            if snippet['title'] != official_data['title']:
                print(f"  ❌ Title mismatch: {snippet['title']} != {official_data['title']}")
                return False
                
            if snippet['language'] != official_data['language']:
                print(f"  ❌ Language mismatch: {snippet['language']} != {official_data['language']}")
                return False
            
            if snippet['createdBy'] != admin_user_id:
                print(f"  ❌ Creator mismatch: {snippet['createdBy']} != {admin_user_id}")
                return False
            
            if snippet.get('isPublished') != False:  # Should default to False
                print(f"  ❌ Should default to unpublished: {snippet.get('isPublished')}")
                return False
            
            print(f"  ✅ Official snippet created with ID: {snippet['_id']}")
        
        # Step 3: Test that regular user cannot create official snippets
        print("  → Testing regular user access restriction...")
        
        # Create regular user
        regular_data = {
            "email": "regular.user@example.com",
            "name": "Regular User",
            "avatar": "regular-avatar.jpg"
            # No role specified - should default to 'user'
        }
        
        regular_token = None
        async with session.post(f"{AUTH_URL}/google-auth", json=regular_data) as resp:
            if resp.status != 200:
                print(f"  ❌ Regular user creation failed: {resp.status}")
                return False
            
            result = await resp.json()
            regular_token = result['data']['token']
            regular_role = result['data']['user']['role']
            
            if regular_role != 'user':
                print(f"  ❌ Expected 'user' role, got {regular_role}")
                return False
        
        # Try to create official snippet with regular user token
        headers = {"Authorization": f"Bearer {regular_token}"}
        async with session.post(
            f"{SNIPPETS_URL}/official",
            json=official_data,
            headers=headers
        ) as response:
            if response.status != 403:
                print(f"  ❌ Expected 403 Forbidden, got {response.status}")
                return False
            
            data = await response.json()
            if "Admin permissions required" not in data.get('message', ''):
                print(f"  ❌ Expected admin permission error, got: {data}")
                return False
        
        print("  ✅ Regular user properly denied access")
        
        # Step 4: Test unauthorized access
        print("  → Testing unauthorized access...")
        
        async with session.post(
            f"{SNIPPETS_URL}/official",
            json=official_data
        ) as response:
            if response.status != 401:
                print(f"  ❌ Expected 401 Unauthorized, got {response.status}")
                return False
        
        print("  ✅ Unauthorized access properly denied")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Exception: {str(e)}")
        return False
    finally:
        if session:
            await session.close()
        # Cleanup test data
        try:
            await users_collection.delete_many({"email": TEST_ADMIN_EMAIL})
            await users_collection.delete_many({"email": "regular.user@example.com"})
            await tokens_collection.delete_many({"userId": admin_user_id}) if admin_user_id else None
            await official_collection.delete_many({"createdBy": admin_user_id}) if admin_user_id else None
        except:
            pass

async def main():
    """Run official snippet creation test"""
    from dotenv import load_dotenv
    load_dotenv('../../.env')
    
    success = await test_official_snippet_create()
    return 0 if success else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)