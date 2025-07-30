#!/usr/bin/env python3
"""
Simple Test: Get JWT from Refresh Token
Demonstrates converting a refresh token to a JWT access token
"""

import asyncio
import aiohttp
import sys
from datetime import datetime

# Test configuration
AUTH_URL = "http://localhost:8081"

async def test_jwt_from_refresh():
    """Test getting JWT access token from refresh token"""
    print("🧪 Testing JWT from Refresh Token...")
    
    # Your provided refresh token
    refresh_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjg4YTJmZTg0MmJhM2FjY2QzODAxY2E3IiwidHlwZSI6InJlZnJlc2giLCJleHAiOjE3NTY0Nzg2OTYsImlhdCI6MTc1Mzg4NjY5NiwianRpIjoiU2NGN3dwN2ZGcmRrYWJoZ2ROWmlQY1l3TFNNUFE2Nzc3V3V4eWdsNnNlRSJ9.XV4u0ZxVSZM9YgqAA7SM319npFmwGEFmEXMfH7pADWY"
    
    session = None
    try:
        session = aiohttp.ClientSession()
        
        print(f"  → Using refresh token: {refresh_token[:50]}...")
        
        # Call /refresh endpoint
        refresh_data = {"refreshToken": refresh_token}
        
        async with session.post(f"{AUTH_URL}/refresh", json=refresh_data) as resp:
            if resp.status != 200:
                error_text = await resp.text()
                print(f"  ❌ Refresh failed: {resp.status} - {error_text}")
                return False
            
            result = await resp.json()
            
            if not result.get('success'):
                print(f"  ❌ Response indicates failure: {result}")
                return False
            
            data = result.get('data', {})
            jwt_token = data.get('token')
            user_info = data.get('user', {})
            
            if not jwt_token:
                print(f"  ❌ No JWT token in response: {data}")
                return False
            
            print(f"  ✅ Successfully obtained JWT token")
            print(f"  📝 JWT: {jwt_token}")
            print(f"  👤 User: {user_info.get('email')} ({user_info.get('name')})")
            print(f"  🔑 User ID: {user_info.get('id')}")
            
            return True
            
    except Exception as e:
        print(f"  ❌ Exception: {e}")
        return False
    finally:
        if session:
            await session.close()

async def main():
    """Run the test"""
    success = await test_jwt_from_refresh()
    print(f"\n{'✅ SUCCESS' if success else '❌ FAILED'}")
    return 0 if success else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)