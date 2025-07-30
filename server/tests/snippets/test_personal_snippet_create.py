#!/usr/bin/env python3
"""
Snippets Test: Personal Snippet Creation
Tests creating a new personal snippet with proper validation
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
TEST_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjg4YTJmZTg0MmJhM2FjY2QzODAxY2E3IiwiZW1haWwiOiJ0ZXN0LnVzZXIuMTA5NzI5LjgyNDcyMTQ2NUBleGFtcGxlLmNvbSIsInJvbGUiOiJ1c2VyIiwidHlwZSI6ImFjY2VzcyIsImV4cCI6MTc1Mzg5MTkxMCwiaWF0IjoxNzUzODg4MzEwfQ.WK4HgS0InfKbrYyypVIAZv0gEmaL6tnDQUnCIFq3ju4"

async def test_personal_snippet_create():
    """Test creating a personal snippet"""
    print("🧪 Testing personal snippet creation...")
    
    session = None
    try:
        session = aiohttp.ClientSession()
        
        # Test data
        snippet_data = {
            "title": "Test React Component",
            "description": "A simple React functional component",
            "code": "const TestComponent = () => { return <div>Hello World</div>; };",
            "language": "javascript",
            "tags": ["react", "component", "test"],
            "difficulty": "easy",
            "isPrivate": True
        }
        
        # Make request
        headers = {"Authorization": f"Bearer {TEST_TOKEN}"}
        async with session.post(
            f"{SNIPPETS_URL}/personal",
            json=snippet_data,
            headers=headers
        ) as response:
            data = await response.json()
            
            if response.status != 200:
                print(f"  ❌ Create failed with status {response.status}: {data}")
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
            if snippet['title'] != snippet_data['title']:
                print(f"  ❌ Title mismatch: {snippet['title']} != {snippet_data['title']}")
                return False
                
            if snippet['language'] != snippet_data['language']:
                print(f"  ❌ Language mismatch: {snippet['language']} != {snippet_data['language']}")
                return False
            
            print(f"  ✅ Personal snippet created with ID: {snippet['_id']}")
            return True
            
    except Exception as e:
        print(f"  ❌ Exception: {str(e)}")
        return False
    finally:
        if session:
            await session.close()

if __name__ == "__main__":
    result = asyncio.run(test_personal_snippet_create())
    exit(0 if result else 1)