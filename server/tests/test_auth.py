#!/usr/bin/env python3
"""
SyntaxMem Auth Testing Suite
Simple, Uniform, Consistent automated tests for Phase 2 features

Usage: python test_auth.py
"""

import asyncio
import aiohttp
import json
from datetime import datetime, timezone, timedelta
import sys
import os

# Add shared modules to path (relative to server root)
sys.path.append('../shared')
sys.path.append('../schemas')

from database import db
from auth_utils import AuthUtils

# Test configuration
AUTH_URL = "http://localhost:8081"
TEST_USER_EMAIL = "test@example.com"
TEST_USER_NAME = "Test User"

class AuthTester:
    def __init__(self):
        self.auth_utils = AuthUtils(os.getenv('JWT_SECRET', 'test-secret'))
        self.session = None
        self.test_results = []
    
    async def setup(self):
        """Setup test session"""
        self.session = aiohttp.ClientSession()
        await db.connect()
        print("🚀 Starting SyntaxMem Auth Tests\n")
    
    async def cleanup(self):
        """Cleanup test session"""
        if self.session:
            await self.session.close()
        # Clean up test data
        await self._clean_test_data()
        print("\n🧹 Test cleanup complete")
    
    async def _clean_test_data(self):
        """Remove test user and tokens"""
        try:
            users_collection = await db.get_users_collection()
            await users_collection.delete_many({"email": TEST_USER_EMAIL})
            
            tokens_collection = await db.get_refresh_tokens_collection()
            await tokens_collection.delete_many({"userId": {"$regex": "test"}})
        except Exception as e:
            print(f"⚠️  Cleanup warning: {e}")
    
    async def test_token_cleanup(self):
        """Test Phase 2 Priority 1: Token cleanup functionality"""
        print("🧪 Testing Token Cleanup...")
        
        try:
            # 1. Create a user with tokens
            user_tokens = await self._create_test_user_with_tokens()
            user_id = user_tokens['user_id']
            
            # 2. Manually expire some tokens
            tokens_collection = await db.get_refresh_tokens_collection()
            
            # Expire 2 out of 3 tokens (get first 2 and expire them)
            tokens_to_expire = await tokens_collection.find({"userId": user_id}).limit(2).to_list(length=2)
            if tokens_to_expire:
                token_ids = [token["_id"] for token in tokens_to_expire]
                await tokens_collection.update_many(
                    {"_id": {"$in": token_ids}},
                    {"$set": {"expiresAt": datetime.now(timezone.utc) - timedelta(days=1)}}
                )
            
            # 3. Trigger login (should cleanup expired tokens)
            login_data = {
                "email": TEST_USER_EMAIL,
                "name": TEST_USER_NAME,
                "avatar": "test-avatar.jpg"
            }
            
            async with self.session.post(f"{AUTH_URL}/google-auth", json=login_data) as resp:
                if resp.status == 200:
                    # 4. Check remaining tokens
                    remaining_tokens = await tokens_collection.count_documents({"userId": user_id})
                    
                    if remaining_tokens <= 2:  # Should have cleaned expired + applied 2-token limit
                        self._log_success("Token Cleanup", f"✅ Expired tokens cleaned. Remaining: {remaining_tokens}")
                        return True
                    else:
                        self._log_failure("Token Cleanup", f"❌ Too many tokens remaining: {remaining_tokens}")
                        return False
                else:
                    self._log_failure("Token Cleanup", f"❌ Login failed: {resp.status}")
                    return False
                    
        except Exception as e:
            self._log_failure("Token Cleanup", f"❌ Exception: {e}")
            return False
    
    async def test_logout_all_devices(self):
        """Test Phase 2 Priority 2: Logout all devices functionality"""
        print("🧪 Testing Logout All Devices...")
        
        try:
            # 1. Create user and get access token
            user_data = await self._create_test_user_with_tokens()
            access_token = user_data['access_token']
            user_id = user_data['user_id']
            
            # 2. Verify we have tokens before logout
            tokens_collection = await db.get_refresh_tokens_collection()
            tokens_before = await tokens_collection.count_documents({"userId": user_id})
            
            if tokens_before == 0:
                self._log_failure("Logout All", "❌ No tokens found before logout")
                return False
            
            # 3. Call logout-all endpoint
            headers = {"Authorization": f"Bearer {access_token}"}
            async with self.session.post(f"{AUTH_URL}/logout-all", headers=headers) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    
                    # 4. Verify all tokens are gone
                    tokens_after = await tokens_collection.count_documents({"userId": user_id})
                    
                    if tokens_after == 0:
                        revoked_count = result.get('data', {}).get('revokedTokens', 0)
                        self._log_success("Logout All", f"✅ All tokens revoked. Count: {revoked_count}")
                        return True
                    else:
                        self._log_failure("Logout All", f"❌ Tokens still exist: {tokens_after}")
                        return False
                else:
                    error_text = await resp.text()
                    self._log_failure("Logout All", f"❌ Request failed: {resp.status} - {error_text}")
                    return False
                    
        except Exception as e:
            self._log_failure("Logout All", f"❌ Exception: {e}")
            return False
    
    async def test_session_limits(self):
        """Test Phase 2 Priority 3: Session limits (2 token max)"""
        print("🧪 Testing Session Limits...")
        
        try:
            # 1. Login 5 times to exceed 2-token limit
            login_data = {
                "email": TEST_USER_EMAIL,
                "name": TEST_USER_NAME,
                "avatar": "test-avatar.jpg"
            }
            
            user_id = None
            for i in range(5):
                async with self.session.post(f"{AUTH_URL}/google-auth", json=login_data) as resp:
                    if resp.status == 200:
                        if not user_id:
                            result = await resp.json()
                            user_id = result.get('data', {}).get('user', {}).get('id')
                    else:
                        self._log_failure("Session Limits", f"❌ Login {i+1} failed: {resp.status}")
                        return False
            
            # 2. Check token count
            tokens_collection = await db.get_refresh_tokens_collection()
            final_token_count = await tokens_collection.count_documents({"userId": user_id})
            
            if final_token_count <= 2:
                self._log_success("Session Limits", f"✅ Token limit enforced. Final count: {final_token_count}")
                return True
            else:
                self._log_failure("Session Limits", f"❌ Too many tokens: {final_token_count}")
                return False
                
        except Exception as e:
            self._log_failure("Session Limits", f"❌ Exception: {e}")
            return False
    
    async def _create_test_user_with_tokens(self):
        """Helper: Create test user and return tokens"""
        login_data = {
            "email": TEST_USER_EMAIL,
            "name": TEST_USER_NAME,
            "avatar": "test-avatar.jpg"
        }
        
        async with self.session.post(f"{AUTH_URL}/google-auth", json=login_data) as resp:
            if resp.status == 200:
                result = await resp.json()
                data = result.get('data', {})
                return {
                    'user_id': data.get('user', {}).get('id'),
                    'access_token': data.get('token'),
                    'refresh_token': data.get('refreshToken')
                }
            else:
                raise Exception(f"Failed to create test user: {resp.status}")
    
    def _log_success(self, test_name, message):
        """Log successful test"""
        self.test_results.append((test_name, True, message))
        print(f"  {message}")
    
    def _log_failure(self, test_name, message):
        """Log failed test"""
        self.test_results.append((test_name, False, message))
        print(f"  {message}")
    
    async def run_all_tests(self):
        """Run all Phase 2 tests"""
        await self.setup()
        
        try:
            # Run tests
            test1 = await self.test_token_cleanup()
            test2 = await self.test_logout_all_devices()
            test3 = await self.test_session_limits()
            
            # Print summary
            print("\n" + "="*50)
            print("🎯 TEST RESULTS SUMMARY")
            print("="*50)
            
            passed = 0
            total = len(self.test_results)
            
            for test_name, success, message in self.test_results:
                status = "PASS" if success else "FAIL"
                print(f"{test_name:20} | {status}")
                if success:
                    passed += 1
            
            print(f"\nResults: {passed}/{total} tests passed")
            
            if passed == total:
                print("🎉 All Phase 2 features working correctly!")
                return True
            else:
                print("⚠️  Some tests failed. Check auth server logs.")
                return False
                
        finally:
            await self.cleanup()

async def main():
    """Main test runner"""
    # Load environment
    from dotenv import load_dotenv
    load_dotenv('../.env')
    
    if not os.getenv('JWT_SECRET'):
        print("❌ JWT_SECRET not found in environment")
        return
    
    if not os.getenv('MONGODB_URI'):
        print("❌ MONGODB_URI not found in environment")
        return
    
    tester = AuthTester()
    success = await tester.run_all_tests()
    
    return 0 if success else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)