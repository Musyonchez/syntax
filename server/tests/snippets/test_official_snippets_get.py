#!/usr/bin/env python3
"""
Snippets Test: Official Snippets Retrieval
Tests getting published official snippets with filtering (no auth required)
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

async def test_official_snippets_get():
    """Test retrieving official snippets"""
    print("🧪 Testing official snippets retrieval...")
    
    session = None
    try:
        session = aiohttp.ClientSession()
        
        # Test basic retrieval (no auth required)
        async with session.get(f"{SNIPPETS_URL}/official") as response:
            data = await response.json()
            
            if response.status != 200:
                print(f"  ❌ Get failed with status {response.status}: {data}")
                return False
            
            # Verify response structure
            if not data.get('success'):
                print(f"  ❌ Response not successful: {data}")
                return False
            
            result = data.get('data')
            if 'snippets' not in result or 'count' not in result:
                print(f"  ❌ Missing snippets or count in response: {data}")
                return False
            
            snippets = result['snippets']
            count = result['count']
            
            if len(snippets) != count:
                print(f"  ❌ Count mismatch: {len(snippets)} != {count}")
                return False
            
            # Verify all snippets are published
            for snippet in snippets:
                if not snippet.get('isPublished', False):
                    print(f"  ❌ Unpublished snippet returned: {snippet.get('_id')}")
                    return False
            
            print(f"  ✅ Retrieved {count} official snippets (all published)")
            
            # Test filtering by language
            async with session.get(f"{SNIPPETS_URL}/official?language=javascript") as response:
                data = await response.json()
                
                if response.status == 200:
                    result = data.get('data', {})
                    js_count = result.get('count', 0)
                    print(f"  ✅ Filter by JavaScript returned {js_count} snippets")
            
            # Test filtering by difficulty
            async with session.get(f"{SNIPPETS_URL}/official?difficulty=easy") as response:
                data = await response.json()
                
                if response.status == 200:
                    result = data.get('data', {})
                    easy_count = result.get('count', 0)
                    print(f"  ✅ Filter by easy difficulty returned {easy_count} snippets")
            
            # Test search functionality
            async with session.get(f"{SNIPPETS_URL}/official?search=array") as response:
                data = await response.json()
                
                if response.status == 200:
                    result = data.get('data', {})
                    search_count = result.get('count', 0)
                    print(f"  ✅ Search for 'array' returned {search_count} snippets")
            
            return True
            
    except Exception as e:
        print(f"  ❌ Exception: {str(e)}")
        return False
    finally:
        if session:
            await session.close()

if __name__ == "__main__":
    result = asyncio.run(test_official_snippets_get())
    exit(0 if result else 1)