#!/usr/bin/env python3
"""
Auth Test: Session Limits
Tests Phase 2 Priority 3 - Session limits (2 token max)
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
TEST_USER_EMAIL = "limits-test@example.com"
TEST_USER_NAME = "Session Limits Test User"

async def test_session_limits():
    """Test session limits (2 token maximum)"""
    print("🧪 Testing Session Limits...")
    
    session = None
    try:
        session = aiohttp.ClientSession()
        await db.connect()
        
        # Clean any existing test data
        users_collection = await db.get_users_collection()
        tokens_collection = await db.get_refresh_tokens_collection()
        await users_collection.delete_many({"email": TEST_USER_EMAIL})
        await tokens_collection.delete_many({"userId": {"$regex": "limits-test"}})
        
        # 1. Login 5 times to exceed 2-token limit
        login_data = {
            "email": TEST_USER_EMAIL,
            "name": TEST_USER_NAME,
            "avatar": "test-avatar.jpg"
        }
        
        user_id = None
        for i in range(5):
            async with session.post(f"{AUTH_URL}/google-auth", json=login_data) as resp:
                if resp.status == 200:
                    if not user_id:
                        result = await resp.json()
                        user_id = result.get('data', {}).get('user', {}).get('id')
                else:
                    print(f"  ❌ Login {i+1} failed: {resp.status}")
                    return False
        
        # 2. Check token count
        final_token_count = await tokens_collection.count_documents({"userId": user_id})
        
        if final_token_count <= 2:
            print(f"  ✅ Token limit enforced. Final count: {final_token_count}")
            return True
        else:
            print(f"  ❌ Too many tokens: {final_token_count}")
            return False
            
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
    """Run session limits test"""
    from dotenv import load_dotenv
    load_dotenv('../../.env')
    
    success = await test_session_limits()
    return 0 if success else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)