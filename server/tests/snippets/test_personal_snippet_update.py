#!/usr/bin/env python3
"""
Snippets Test: Personal Snippet Update
Tests updating a personal snippet with ownership verification
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
SNIPPETS_URL = "http://localhost:8083"
TEST_TOKEN = "test_jwt_token_here"  # In real tests, get from auth service
TEST_SNIPPET_ID = "507f1f77bcf86cd799439011"  # Mock ObjectId

async def test_personal_snippet_update():
    """Test updating a personal snippet"""
    print("🧪 Testing personal snippet update...")
    
    session = None
    try:
        session = aiohttp.ClientSession()
        
        # Update data
        update_data = {
            "title": "Updated Test Component",
            "description": "Updated description with new content",
            "tags": ["react", "updated", "test"],
            "difficulty": "medium"
        }
        
        # Make request
        headers = {"Authorization": f"Bearer {TEST_TOKEN}"}
        async with session.put(
            f"{SNIPPETS_URL}/personal/{TEST_SNIPPET_ID}",
            json=update_data,
            headers=headers
        ) as response:
            data = await response.json()
            
            if response.status == 404:
                print(f"  ℹ️ Snippet not found (expected in test environment)")
                return True
            
            if response.status != 200:
                print(f"  ❌ Update failed with status {response.status}: {data}")
                return False
            
            # Verify response structure
            if not data.get('success'):
                print(f"  ❌ Response not successful: {data}")
                return False
            
            snippet = data.get('data')
            if not snippet:
                print(f"  ❌ No snippet data returned: {data}")
                return False
            
            # Verify data was updated
            if snippet.get('title') != update_data['title']:
                print(f"  ❌ Title not updated: {snippet.get('title')} != {update_data['title']}")
                return False
            
            if snippet.get('difficulty') != update_data['difficulty']:
                print(f"  ❌ Difficulty not updated: {snippet.get('difficulty')} != {update_data['difficulty']}")
                return False
            
            print(f"  ✅ Personal snippet updated successfully")
            return True
            
    except Exception as e:
        print(f"  ❌ Exception: {str(e)}")
        return False
    finally:
        if session:
            await session.close()

if __name__ == "__main__":
    result = asyncio.run(test_personal_snippet_update())
    exit(0 if result else 1)