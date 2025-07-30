#!/usr/bin/env python3
"""
Snippets Test: Authentication Requirements
Tests that personal snippet endpoints properly require authentication
"""

import asyncio
import aiohttp
import sys
import os

# Add shared modules to path
sys.path.append('../../shared')
sys.path.append('../../schemas')

# Test configuration
SNIPPETS_URL = "http://localhost:8083"

async def test_authentication_required():
    """Test that personal endpoints require proper authentication"""
    print("🧪 Testing authentication requirements...")
    
    session = None
    try:
        session = aiohttp.ClientSession()
        
        # Test endpoints without token
        endpoints_to_test = [
            ("GET", f"{SNIPPETS_URL}/personal"),
            ("POST", f"{SNIPPETS_URL}/personal"),
            ("PUT", f"{SNIPPETS_URL}/personal/507f1f77bcf86cd799439011"),
            ("DELETE", f"{SNIPPETS_URL}/personal/507f1f77bcf86cd799439011")
        ]
        
        for method, url in endpoints_to_test:
            if method == "GET":
                async with session.get(url) as response:
                    if response.status != 401:
                        print(f"  ❌ {method} {url} should return 401, got {response.status}")
                        return False
            elif method == "POST":
                async with session.post(url, json={}) as response:
                    if response.status != 401:
                        print(f"  ❌ {method} {url} should return 401, got {response.status}")
                        return False
            elif method == "PUT":
                async with session.put(url, json={}) as response:
                    if response.status != 401:
                        print(f"  ❌ {method} {url} should return 401, got {response.status}")
                        return False
            elif method == "DELETE":
                async with session.delete(url) as response:
                    if response.status != 401:
                        print(f"  ❌ {method} {url} should return 401, got {response.status}")
                        return False
        
        print(f"  ✅ All personal endpoints properly require authentication")
        
        # Test with invalid token
        headers = {"Authorization": "Bearer invalid_token"}
        async with session.get(f"{SNIPPETS_URL}/personal", headers=headers) as response:
            if response.status != 401:
                print(f"  ❌ Invalid token should return 401, got {response.status}")
                return False
        
        print(f"  ✅ Invalid tokens properly rejected")
        
        # Test malformed Authorization header
        malformed_headers = [
            {"Authorization": "invalid_format"},
            {"Authorization": "Bearer"},
            {"Authorization": ""},
        ]
        
        for headers in malformed_headers:
            async with session.get(f"{SNIPPETS_URL}/personal", headers=headers) as response:
                if response.status != 401:
                    print(f"  ❌ Malformed auth header should return 401, got {response.status}")
                    return False
        
        print(f"  ✅ Malformed Authorization headers properly rejected")
        
        # Verify official endpoints don't require auth
        async with session.get(f"{SNIPPETS_URL}/official") as response:
            if response.status == 401:
                print(f"  ❌ Official endpoints should not require authentication")
                return False
        
        print(f"  ✅ Official endpoints accessible without authentication")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Exception: {str(e)}")
        return False
    finally:
        if session:
            await session.close()

if __name__ == "__main__":
    result = asyncio.run(test_authentication_required())
    exit(0 if result else 1)