#!/usr/bin/env python3
"""
Auth Test: Token Cleanup
Tests Phase 2 Priority 1 - Automatic expired token cleanup
"""

import asyncio
import aiohttp
import sys
import os
from datetime import datetime, timezone, timedelta

# Add shared modules to path
sys.path.append('../../shared')
sys.path.append('../../schemas')

from database import db

# Test configuration
AUTH_URL = "http://localhost:8081"
TEST_USER_EMAIL = "cleanup-test@example.com"
TEST_USER_NAME = "Token Cleanup Test User"

async def test_token_cleanup():
    """Test automatic cleanup of expired refresh tokens"""
    print("🧪 Testing Token Cleanup...")
    
    session = None
    try:
        session = aiohttp.ClientSession()
        await db.connect()
        
        # Clean any existing test data
        users_collection = await db.get_users_collection()
        tokens_collection = await db.get_refresh_tokens_collection()
        await tokens_collection.delete_many({"userId": {"$regex": "cleanup-test"}})
        
        # 1. Create a user with tokens
        login_data = {
            "email": TEST_USER_EMAIL,
            "name": TEST_USER_NAME,
            "avatar": "test-avatar.jpg"
        }
        
        user_id = None
        async with session.post(f"{AUTH_URL}/google-auth", json=login_data) as resp:
            if resp.status == 200:
                result = await resp.json()
                user_id = result.get('data', {}).get('user', {}).get('id')
            else:
                print(f"  ❌ Failed to create test user: {resp.status}")
                return False
        
        # 2. Create more tokens by logging in multiple times
        for i in range(3):
            async with session.post(f"{AUTH_URL}/google-auth", json=login_data) as resp:
                if resp.status != 200:
                    print(f"  ❌ Failed to create additional tokens: {resp.status}")
                    return False
        
        # 3. Manually expire some tokens
        tokens_to_expire = await tokens_collection.find({"userId": user_id}).limit(2).to_list(length=2)
        if tokens_to_expire:
            token_ids = [token["_id"] for token in tokens_to_expire]
            await tokens_collection.update_many(
                {"_id": {"$in": token_ids}},
                {"$set": {"expiresAt": datetime.now(timezone.utc) - timedelta(days=1)}}
            )
        
        # 4. Trigger login (should cleanup expired tokens)
        async with session.post(f"{AUTH_URL}/google-auth", json=login_data) as resp:
            if resp.status == 200:
                # 5. Check remaining tokens
                remaining_tokens = await tokens_collection.count_documents({"userId": user_id})
                
                if remaining_tokens <= 2:  # Should have cleaned expired + applied 2-token limit
                    print(f"  ✅ Expired tokens cleaned. Remaining: {remaining_tokens}")
                    return True
                else:
                    print(f"  ❌ Too many tokens remaining: {remaining_tokens}")
                    return False
            else:
                print(f"  ❌ Cleanup trigger login failed: {resp.status}")
                return False
                
    except Exception as e:
        print(f"  ❌ Exception: {e}")
        return False
    finally:
        if session:
            await session.close()

async def main():
    """Run token cleanup test"""
    from dotenv import load_dotenv
    load_dotenv('../../.env')
    
    success = await test_token_cleanup()
    return 0 if success else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)