#!/usr/bin/env python3
"""
Auth Test: Invalid Token Handling
Tests expired/malformed JWT tokens and proper error handling
"""

import asyncio
import aiohttp
import sys
import os
import jwt
from datetime import datetime, timezone, timedelta

# Add shared modules to path
sys.path.append('../../shared')
sys.path.append('../../schemas')

from database import db

# Test configuration
AUTH_URL = "http://localhost:8081"

async def test_invalid_token_handling():
    """Test handling of various invalid token scenarios"""
    print("🧪 Testing Invalid Token Handling...")
    
    session = None
    try:
        session = aiohttp.ClientSession()
        await db.connect()
        
        # Test 1: Malformed JWT Tokens
        print("  → Testing malformed JWT tokens...")
        
        malformed_tokens = [
            "not.a.jwt",  # Not enough parts
            "too.many.parts.here.invalid",  # Too many parts
            "invalid-base64.invalid-base64.invalid-base64",  # Invalid base64
            "",  # Empty token
            "Bearer token-without-bearer-prefix",  # Wrong format
        ]
        
        for i, bad_token in enumerate(malformed_tokens):
            headers = {"Authorization": f"Bearer {bad_token}"}
            async with session.post(f"{AUTH_URL}/logout-all", headers=headers) as resp:
                if resp.status == 200:
                    print(f"  ❌ Malformed token {i+1} was accepted: {bad_token}")
                    return False
                
                if resp.status != 401:
                    print(f"  ❌ Expected 401 for malformed token {i+1}, got {resp.status}")
                    return False
        
        print("  ✅ Malformed JWT tokens properly rejected")
        
        # Test 2: Expired JWT Tokens
        print("  → Testing expired JWT tokens...")
        
        # Create properly formatted but expired token
        jwt_secret = os.getenv('JWT_SECRET', 'test-secret')
        expired_payload = {
            "user_id": "test-user-123",
            "email": "test@example.com",
            "role": "user",
            "exp": int((datetime.now(timezone.utc) - timedelta(hours=1)).timestamp()),  # Expired 1 hour ago
            "iat": int((datetime.now(timezone.utc) - timedelta(hours=2)).timestamp())   # Issued 2 hours ago
        }
        
        expired_token = jwt.encode(expired_payload, jwt_secret, algorithm='HS256')
        headers = {"Authorization": f"Bearer {expired_token}"}
        
        async with session.post(f"{AUTH_URL}/logout-all", headers=headers) as resp:
            if resp.status == 200:
                print("  ❌ Expired token was accepted")
                return False
            
            if resp.status != 401:
                print(f"  ❌ Expected 401 for expired token, got {resp.status}")
                return False
        
        print("  ✅ Expired JWT tokens properly rejected")
        
        # Test 3: JWT with Wrong Secret
        print("  → Testing JWT with wrong secret...")
        
        wrong_secret_payload = {
            "user_id": "test-user-123",
            "email": "test@example.com", 
            "role": "user",
            "exp": int((datetime.now(timezone.utc) + timedelta(hours=1)).timestamp()),
            "iat": int(datetime.now(timezone.utc).timestamp())
        }
        
        wrong_secret_token = jwt.encode(wrong_secret_payload, "wrong-secret", algorithm='HS256')
        headers = {"Authorization": f"Bearer {wrong_secret_token}"}
        
        async with session.post(f"{AUTH_URL}/logout-all", headers=headers) as resp:
            if resp.status == 200:
                print("  ❌ Token with wrong secret was accepted")
                return False
            
            if resp.status != 401:
                print(f"  ❌ Expected 401 for wrong secret, got {resp.status}")
                return False
        
        print("  ✅ JWT with wrong secret properly rejected")
        
        # Test 4: JWT Missing Required Fields
        print("  → Testing JWT missing required fields...")
        
        incomplete_payloads = [
            {"email": "test@example.com", "role": "user"},  # Missing user_id
            {"user_id": "test-123", "role": "user"},        # Missing email
            {"user_id": "test-123", "email": "test@example.com"},  # Missing role
            {},  # Missing everything
        ]
        
        for i, payload in enumerate(incomplete_payloads):
            # Add exp and iat to make it valid JWT structure
            payload.update({
                "exp": int((datetime.now(timezone.utc) + timedelta(hours=1)).timestamp()),
                "iat": int(datetime.now(timezone.utc).timestamp())
            })
            
            incomplete_token = jwt.encode(payload, jwt_secret, algorithm='HS256')
            headers = {"Authorization": f"Bearer {incomplete_token}"}
            
            async with session.post(f"{AUTH_URL}/logout-all", headers=headers) as resp:
                if resp.status == 200:
                    print(f"  ❌ Incomplete token {i+1} was accepted: {payload}")
                    return False
                
                if resp.status != 401:
                    print(f"  ❌ Expected 401 for incomplete token {i+1}, got {resp.status}")
                    return False
        
        print("  ✅ JWT missing required fields properly rejected")
        
        # Test 5: Valid Token Structure but Non-existent User
        print("  → Testing valid token with non-existent user...")
        
        valid_structure_payload = {
            "user_id": "non-existent-user-id",
            "email": "nonexistent@example.com",
            "role": "user",
            "exp": int((datetime.now(timezone.utc) + timedelta(hours=1)).timestamp()),
            "iat": int(datetime.now(timezone.utc).timestamp())
        }
        
        valid_structure_token = jwt.encode(valid_structure_payload, jwt_secret, algorithm='HS256')
        headers = {"Authorization": f"Bearer {valid_structure_token}"}
        
        async with session.post(f"{AUTH_URL}/logout-all", headers=headers) as resp:
            # This should still work for logout-all since it doesn't check user existence
            # But should return 0 revoked tokens
            if resp.status != 200:
                print(f"  ❌ Valid token structure failed: {resp.status}")
                return False
            
            result = await resp.json()
            revoked_count = result.get('data', {}).get('revokedTokens', -1)
            
            if revoked_count != 0:
                print(f"  ❌ Expected 0 revoked tokens for non-existent user, got {revoked_count}")
                return False
        
        print("  ✅ Valid token with non-existent user handled correctly")
        
        # Test 6: Refresh Token Edge Cases
        print("  → Testing refresh token edge cases...")
        
        # Try to refresh with access token (wrong token type)
        valid_access_token = jwt.encode(valid_structure_payload, jwt_secret, algorithm='HS256')
        refresh_data = {"refreshToken": valid_access_token}
        
        async with session.post(f"{AUTH_URL}/refresh", json=refresh_data) as resp:
            if resp.status == 200:
                print("  ❌ Access token was accepted as refresh token")
                return False
            
            if resp.status != 401:
                print(f"  ❌ Expected 401 for wrong token type, got {resp.status}")
                return False
        
        print("  ✅ Wrong token type properly rejected for refresh")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Exception: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        if session:
            await session.close()

async def main():
    """Run invalid token handling tests"""
    from dotenv import load_dotenv
    load_dotenv('../../.env')
    
    success = await test_invalid_token_handling()
    return 0 if success else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)