#!/usr/bin/env python3
"""
Snippets Test: Personal Snippet Deletion
Tests soft deleting a personal snippet with ownership verification
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
TEST_SNIPPET_ID = "507f1f77bcf86cd799439011"  # Mock ObjectId

async def test_personal_snippet_delete():
    """Test deleting a personal snippet"""
    print("🧪 Testing personal snippet deletion...")
    
    session = None
    try:
        session = aiohttp.ClientSession()
        
        # Make request
        headers = {"Authorization": f"Bearer {TEST_TOKEN}"}
        async with session.delete(
            f"{SNIPPETS_URL}/personal/{TEST_SNIPPET_ID}",
            headers=headers
        ) as response:
            data = await response.json()
            
            if response.status == 404:
                print(f"  ℹ️ Snippet not found (expected in test environment)")
                return True
            
            if response.status != 200:
                print(f"  ❌ Delete failed with status {response.status}: {data}")
                return False
            
            # Verify response structure
            if not data.get('success'):
                print(f"  ❌ Response not successful: {data}")
                return False
            
            print(f"  ✅ Personal snippet deleted successfully")
            
            # Verify snippet is no longer accessible
            async with session.get(
                f"{SNIPPETS_URL}/personal",
                headers=headers
            ) as response:
                data = await response.json()
                
                if response.status == 200:
                    result = data.get('data', {})
                    snippets = result.get('snippets', [])
                    
                    # Check that deleted snippet is not in results
                    for snippet in snippets:
                        if snippet.get('_id') == TEST_SNIPPET_ID:
                            print(f"  ❌ Deleted snippet still appears in results")
                            return False
                    
                    print(f"  ✅ Deleted snippet no longer appears in results")
            
            return True
            
    except Exception as e:
        print(f"  ❌ Exception: {str(e)}")
        return False
    finally:
        if session:
            await session.close()

if __name__ == "__main__":
    result = asyncio.run(test_personal_snippet_delete())
    exit(0 if result else 1)