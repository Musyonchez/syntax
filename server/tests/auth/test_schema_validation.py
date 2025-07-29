#!/usr/bin/env python3
"""
Auth Test: Schema Validation
Tests schema validation for invalid data rejection
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

async def test_schema_validation():
    """Test schema validation for all auth endpoints"""
    print("🧪 Testing Schema Validation...")
    
    session = None
    try:
        session = aiohttp.ClientSession()
        await db.connect()
        
        # Test 1: Google Auth - Missing Required Fields
        print("  → Testing google-auth with missing required fields...")
        
        test_cases = [
            {},  # Empty data
            {"email": "test@example.com"},  # Missing name
            {"name": "Test User"},  # Missing email
            {"email": "", "name": "Test User"},  # Empty email
            {"email": "test@example.com", "name": ""},  # Empty name
            {"email": "invalid-email", "name": "Test User"},  # Invalid email
        ]
        
        for i, invalid_data in enumerate(test_cases):
            async with session.post(f"{AUTH_URL}/google-auth", json=invalid_data) as resp:
                if resp.status == 200:
                    print(f"  ❌ Invalid data case {i+1} was accepted: {invalid_data}")
                    return False
                
                if resp.status != 400:
                    print(f"  ❌ Expected 400 for case {i+1}, got {resp.status}")
                    return False
        
        print("  ✅ Google auth schema validation working")
        
        # Test 2: Google Auth - Data Sanitization
        print("  → Testing google-auth data sanitization...")
        
        # Create user with data that needs sanitization
        sanitization_data = {
            "email": "  SANITIZE@EXAMPLE.COM  ",  # Should be lowercased and trimmed
            "name": "  Test User  ",  # Should be trimmed
            "avatar": "  http://example.com/avatar.jpg  "  # Should be trimmed
        }
        
        async with session.post(f"{AUTH_URL}/google-auth", json=sanitization_data) as resp:
            if resp.status != 200:
                print(f"  ❌ Sanitization test failed: {resp.status}")
                return False
            
            result = await resp.json()
            user = result.get('data', {}).get('user', {})
            
            # Check sanitization worked
            if user.get('email') != 'sanitize@example.com':
                print(f"  ❌ Email not sanitized: {user.get('email')}")
                return False
            
            if user.get('name') != 'Test User':
                print(f"  ❌ Name not sanitized: {user.get('name')}")
                return False
        
        print("  ✅ Data sanitization working")
        
        # Clean up test user
        users_collection = await db.get_users_collection()
        tokens_collection = await db.get_refresh_tokens_collection()
        await users_collection.delete_many({"email": "sanitize@example.com"})
        await tokens_collection.delete_many({"userId": {"$regex": "sanitize"}})
        
        # Test 3: Refresh Token - Missing/Invalid Data
        print("  → Testing refresh endpoint validation...")
        
        refresh_test_cases = [
            {},  # Empty data
            {"refreshToken": ""},  # Empty token
            {"refreshToken": None},  # Null token
            {"wrongField": "some-token"},  # Wrong field name
        ]
        
        for i, invalid_data in enumerate(refresh_test_cases):
            async with session.post(f"{AUTH_URL}/refresh", json=invalid_data) as resp:
                if resp.status == 200:
                    print(f"  ❌ Invalid refresh case {i+1} was accepted: {invalid_data}")
                    return False
                
                if resp.status != 400:
                    print(f"  ❌ Expected 400 for refresh case {i+1}, got {resp.status}")
                    return False
        
        print("  ✅ Refresh token validation working")
        
        # Test 4: Logout - Missing/Invalid Data
        print("  → Testing logout endpoint validation...")
        
        logout_test_cases = [
            {},  # Empty data
            {"refreshToken": ""},  # Empty token
            {"refreshToken": None},  # Null token
            {"wrongField": "some-token"},  # Wrong field name
        ]
        
        for i, invalid_data in enumerate(logout_test_cases):
            async with session.post(f"{AUTH_URL}/logout", json=invalid_data) as resp:
                if resp.status == 200:
                    print(f"  ❌ Invalid logout case {i+1} was accepted: {invalid_data}")
                    return False
                
                if resp.status != 400:
                    print(f"  ❌ Expected 400 for logout case {i+1}, got {resp.status}")
                    return False
        
        print("  ✅ Logout validation working")
        
        # Test 5: Logout All - Missing Authorization
        print("  → Testing logout-all authorization validation...")
        
        # No authorization header
        async with session.post(f"{AUTH_URL}/logout-all") as resp:
            if resp.status != 401:
                print(f"  ❌ Expected 401 for missing auth, got {resp.status}")
                return False
        
        # Invalid authorization header
        headers = {"Authorization": "Bearer invalid.jwt.token"}
        async with session.post(f"{AUTH_URL}/logout-all", headers=headers) as resp:
            if resp.status != 401:
                print(f"  ❌ Expected 401 for invalid auth, got {resp.status}")
                return False
        
        # Wrong authorization format
        headers = {"Authorization": "InvalidFormat token"}
        async with session.post(f"{AUTH_URL}/logout-all", headers=headers) as resp:
            if resp.status != 401:
                print(f"  ❌ Expected 401 for wrong auth format, got {resp.status}")
                return False
        
        print("  ✅ Logout-all authorization validation working")
        
        # Test 6: JSON Parsing Errors
        print("  → Testing JSON parsing error handling...")
        
        # Send invalid JSON
        headers = {"Content-Type": "application/json"}
        async with session.post(f"{AUTH_URL}/google-auth", data="invalid json", headers=headers) as resp:
            if resp.status == 200:
                print("  ❌ Invalid JSON was accepted")
                return False
            
            if resp.status != 400:
                print(f"  ❌ Expected 400 for invalid JSON, got {resp.status}")
                return False
        
        print("  ✅ JSON parsing error handling working")
        
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
    """Run schema validation tests"""
    from dotenv import load_dotenv
    load_dotenv('../../.env')
    
    success = await test_schema_validation()
    return 0 if success else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)