#!/usr/bin/env python3
"""
Auth Test: Security Validation
Tests unauthorized access attempts and token injection scenarios
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

async def test_security_validation():
    """Test security measures against various attack scenarios"""
    print("🧪 Testing Security Validation...")
    
    session = None
    try:
        session = aiohttp.ClientSession()
        await db.connect()
        
        # Test 1: SQL Injection Attempts (even though we use MongoDB)
        print("  → Testing injection attack attempts...")
        
        injection_payloads = [
            {"email": "'; DROP TABLE users; --", "name": "Test User"},
            {"email": "test@example.com", "name": "'; DELETE * FROM users; --"},
            {"email": "$ne: null", "name": "Test User"},
            {"email": {"$gt": ""}, "name": "Test User"},
            {"email": "test@example.com", "name": {"$where": "this.name == 'admin'"}},
        ]
        
        for i, payload in enumerate(injection_payloads):
            async with session.post(f"{AUTH_URL}/google-auth", json=payload) as resp:
                # Should either reject with 400 (validation) or safely handle
                if resp.status == 200:
                    result = await resp.json()
                    # If accepted, data should be sanitized
                    user_data = result.get('data', {}).get('user', {})
                    if isinstance(user_data.get('email'), dict) or isinstance(user_data.get('name'), dict):
                        print(f"  ❌ Injection payload {i+1} not sanitized: {user_data}")
                        return False
        
        print("  ✅ Injection attacks properly handled")
        
        # Test 2: XSS Attempts
        print("  → Testing XSS payload handling...")
        
        xss_payloads = [
            {"email": "test@example.com", "name": "<script>alert('xss')</script>"},
            {"email": "test@example.com", "name": "javascript:alert('xss')"},
            {"email": "test@example.com", "avatar": "<img src=x onerror=alert('xss')>"},
            {"email": "test@example.com", "name": "Test<iframe>User</iframe>"},
        ]
        
        for i, payload in enumerate(xss_payloads):
            async with session.post(f"{AUTH_URL}/google-auth", json=payload) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    user_data = result.get('data', {}).get('user', {})
                    
                    # Check if dangerous tags/scripts are present
                    name = user_data.get('name', '')
                    avatar = user_data.get('avatar', '')
                    
                    dangerous_patterns = ['<script', 'javascript:', '<iframe', 'onerror=']
                    for pattern in dangerous_patterns:
                        if pattern in name.lower() or pattern in avatar.lower():
                            print(f"  ❌ XSS payload {i+1} not sanitized: {user_data}")
                            return False
        
        print("  ✅ XSS payloads properly sanitized")
        
        # Test 3: Token Manipulation Attempts
        print("  → Testing token manipulation attempts...")
        
        jwt_secret = os.getenv('JWT_SECRET', 'test-secret')
        
        # Create valid token
        valid_payload = {
            "user_id": "test-user-123",
            "email": "test@example.com",
            "role": "user",
            "exp": int((datetime.now(timezone.utc) + timedelta(hours=1)).timestamp()),
            "iat": int(datetime.now(timezone.utc).timestamp())
        }
        valid_token = jwt.encode(valid_payload, jwt_secret, algorithm='HS256')
        
        # Attempt 1: Role escalation
        escalated_payload = valid_payload.copy()
        escalated_payload["role"] = "admin"
        escalated_token = jwt.encode(escalated_payload, jwt_secret, algorithm='HS256')
        
        headers = {"Authorization": f"Bearer {escalated_token}"}
        async with session.post(f"{AUTH_URL}/logout-all", headers=headers) as resp:
            # Should accept the token but role escalation shouldn't matter for this endpoint
            if resp.status != 200:
                print(f"  ❌ Valid token with role change rejected: {resp.status}")
                return False
        
        # Attempt 2: User ID manipulation
        manipulated_payload = valid_payload.copy()
        manipulated_payload["user_id"] = "different-user-id"
        manipulated_token = jwt.encode(manipulated_payload, jwt_secret, algorithm='HS256')
        
        headers = {"Authorization": f"Bearer {manipulated_token}"}
        async with session.post(f"{AUTH_URL}/logout-all", headers=headers) as resp:
            # Should accept token but operate on the manipulated user_id
            if resp.status != 200:
                print(f"  ❌ Token with manipulated user_id rejected: {resp.status}")
                return False
        
        print("  ✅ Token manipulation handled securely")
        
        # Test 4: Rate Limiting Behavior (basic test)
        print("  → Testing rapid request handling...")
        
        # Send many rapid requests
        rapid_requests = []
        for i in range(20):
            request = session.post(f"{AUTH_URL}/google-auth", json={
                "email": f"rapid{i}@example.com",
                "name": f"Rapid User {i}"
            })
            rapid_requests.append(request)
        
        responses = await asyncio.gather(*rapid_requests, return_exceptions=True)
        
        successful_count = 0
        for i, response in enumerate(responses):
            if isinstance(response, Exception):
                print(f"  ❌ Rapid request {i+1} failed with exception: {response}")
                return False
            
            if response.status == 200:
                successful_count += 1
            
            response.close()
        
        # Should handle all requests (no rate limiting implemented yet, but no crashes)
        if successful_count < 15:  # Allow some failures, but most should succeed
            print(f"  ❌ Too many rapid requests failed: {successful_count}/20")
            return False
        
        print("  ✅ Rapid requests handled without crashes")
        
        # Test 5: Large Payload Attacks
        print("  → Testing large payload handling...")
        
        # Very large strings
        large_payloads = [
            {"email": "test@example.com", "name": "A" * 10000},  # 10KB name
            {"email": "test@example.com", "avatar": "http://example.com/" + "x" * 5000},  # Large URL
            {"email": "x" * 1000 + "@example.com", "name": "Test User"},  # Large email
        ]
        
        for i, payload in enumerate(large_payloads):
            async with session.post(f"{AUTH_URL}/google-auth", json=payload) as resp:
                # Should either reject or handle gracefully
                if resp.status == 200:
                    result = await resp.json()
                    # If accepted, check data is reasonably sized
                    user_data = result.get('data', {}).get('user', {})
                    if len(str(user_data)) > 50000:  # Sanity check
                        print(f"  ❌ Large payload {i+1} not properly limited")
                        return False
                elif resp.status not in [400, 413]:  # 400 Bad Request or 413 Payload Too Large
                    print(f"  ❌ Large payload {i+1} returned unexpected status: {resp.status}")
                    return False
        
        print("  ✅ Large payloads handled securely")
        
        # Test 6: Authorization Header Manipulation
        print("  → Testing authorization header manipulation...")
        
        # Various malformed authorization headers
        malformed_headers = [
            {"Authorization": "Bearer"},  # Missing token
            {"Authorization": "Bearer "},  # Empty token
            {"Authorization": "Basic dGVzdDp0ZXN0"},  # Wrong auth type
            {"Authorization": f"Bearer {valid_token} extra-data"},  # Extra data
            {"X-Authorization": f"Bearer {valid_token}"},  # Wrong header name
            {"authorization": f"Bearer {valid_token}"},  # Lowercase (should work)
        ]
        
        for i, headers in enumerate(malformed_headers):
            async with session.post(f"{AUTH_URL}/logout-all", headers=headers) as resp:
                # Only lowercase authorization should work
                if i == len(malformed_headers) - 1:  # Last one (lowercase)
                    if resp.status != 200:
                        print(f"  ❌ Lowercase authorization header rejected: {resp.status}")
                        return False
                else:
                    if resp.status == 200:
                        print(f"  ❌ Malformed auth header {i+1} was accepted: {headers}")
                        return False
        
        print("  ✅ Authorization header manipulation properly handled")
        
        # Test 7: Content-Type Attack
        print("  → Testing content-type manipulation...")
        
        # Send JSON data with wrong content-type
        wrong_content_types = [
            {"Content-Type": "text/plain"},
            {"Content-Type": "application/xml"},
            {"Content-Type": "multipart/form-data"},
        ]
        
        valid_data = {"email": "test@example.com", "name": "Test User"}
        
        for i, headers in enumerate(wrong_content_types):
            async with session.post(f"{AUTH_URL}/google-auth", json=valid_data, headers=headers) as resp:
                # Should either reject or handle gracefully
                if resp.status == 200:
                    # If accepted, should still parse JSON correctly
                    result = await resp.json()
                    if not result.get('data', {}).get('user'):
                        print(f"  ❌ Wrong content-type {i+1} caused parsing issues")
                        return False
        
        print("  ✅ Content-type manipulation handled securely")
        
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
    """Run security validation tests"""
    from dotenv import load_dotenv
    load_dotenv('../../.env')
    
    success = await test_security_validation()
    return 0 if success else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)