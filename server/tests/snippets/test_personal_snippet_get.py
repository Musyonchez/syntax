#!/usr/bin/env python3
"""
Snippets Test: Personal Snippet Retrieval
Tests getting user's personal snippets with filtering
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

async def test_personal_snippet_get():
    """Test retrieving personal snippets"""
    print("🧪 Testing personal snippets retrieval...")
    
    session = None
    try:
        session = aiohttp.ClientSession()
        
        # Test basic retrieval
        headers = {"Authorization": f"Bearer {TEST_TOKEN}"}
        async with session.get(
            f"{SNIPPETS_URL}/personal",
            headers=headers
        ) as response:
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
            
            print(f"  ✅ Retrieved {count} personal snippets")
            
            # Test filtering by language
            async with session.get(
                f"{SNIPPETS_URL}/personal?language=javascript",
                headers=headers
            ) as response:
                data = await response.json()
                
                if response.status != 200:
                    print(f"  ❌ Filter failed with status {response.status}: {data}")
                    return False
                
                result = data.get('data')
                print(f"  ✅ Filter by language returned {result.get('count', 0)} snippets")
            
            return True
            
    except Exception as e:
        print(f"  ❌ Exception: {str(e)}")
        return False
    finally:
        if session:
            await session.close()

if __name__ == "__main__":
    result = asyncio.run(test_personal_snippet_get())
    exit(0 if result else 1)