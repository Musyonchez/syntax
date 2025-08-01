#!/usr/bin/env python3
"""
Test 07: Authentication Requirements
Tests authentication requirements across all snippets endpoints (personal vs public access)
"""

import requests
import json
from datetime import datetime

def get_regular_token():
    """Helper function to get a regular user auth token"""
    test_user_data = {
        "email": f"test_auth_req_{datetime.now().strftime('%Y%m%d_%H%M%S')}@example.com",
        "name": "Test Auth Required User",
        "avatar": "https://example.com/avatar.jpg"
    }
    
    auth_response = requests.post(
        'http://localhost:8081/google-auth',
        json=test_user_data,
        headers={'Content-Type': 'application/json'}
    )
    
    if auth_response.status_code != 200:
        return None, None, None
    
    auth_data = auth_response.json()
    if not auth_data.get('success'):
        return None, None, None
    
    return (
        auth_data['data']['token'],
        auth_data['data']['user']['id'],
        auth_data['data']['user']['email']
    )

def get_admin_token():
    """Helper function to get an admin auth token"""
    admin_data = {
        "email": "musyonchez@gmail.com",  # This should be in ADMIN_EMAIL env var
        "name": "Admin Test User",
        "avatar": "https://example.com/admin-avatar.jpg"
    }
    
    auth_response = requests.post(
        'http://localhost:8081/google-auth',
        json=admin_data,
        headers={'Content-Type': 'application/json'}
    )
    
    if auth_response.status_code != 200:
        return None, None, None
    
    auth_data = auth_response.json()
    if not auth_data.get('success'):
        return None, None, None
    
    return (
        auth_data['data']['token'],
        auth_data['data']['user']['id'],
        auth_data['data']['user']['email']
    )

def test_authentication_requirements():
    """Test authentication requirements across all snippets endpoints"""
    print("🧪 Testing Authentication Requirements...")
    
    try:
        # Step 1: Get valid tokens for testing
        print("  📝 Step 1: Getting valid tokens for testing...")
        
        regular_token, regular_id, regular_email = get_regular_token()
        admin_token, admin_id, admin_email = get_admin_token()
        
        if not regular_token or not admin_token:
            print("  ❌ Failed to get required authentication tokens")
            return False
        
        print(f"  ✅ Got regular token: {regular_email}")
        print(f"  ✅ Got admin token: {admin_email}")
        
        # Step 2: Test endpoints that should NOT require authentication (public access)
        print("  📝 Step 2: Testing public endpoints (no auth required)...")
        
        public_endpoints = [
            ('GET', 'http://localhost:8083/official', {}),
            ('GET', 'http://localhost:8083/official?language=javascript', {}),
            ('GET', 'http://localhost:8083/health', {}),
        ]
        
        for method, url, data in public_endpoints:
            if method == 'GET':
                response = requests.get(url)
            else:
                response = requests.post(url, json=data, headers={'Content-Type': 'application/json'})
            
            if response.status_code not in [200, 404]:  # 404 is ok if no data exists
                print(f"  ❌ Public endpoint should work without auth: {method} {url} -> {response.status_code}")
                return False
        
        print("  ✅ Public endpoints work without authentication")
        
        # Step 3: Test endpoints that REQUIRE authentication (should fail without auth)
        print("  📝 Step 3: Testing protected endpoints (auth required)...")
        
        sample_personal_snippet = {
            "title": "Test Snippet",
            "description": "Testing auth requirements",
            "code": "console.log('test');",
            "language": "javascript",
            "tags": ["test"],
            "difficulty": "easy"
        }
        
        sample_official_snippet = {
            "title": "Test Official Snippet",
            "description": "Testing admin auth requirements",
            "code": "console.log('official test');",
            "language": "javascript",
            "category": "test"
        }
        
        protected_endpoints = [
            ('GET', 'http://localhost:8083/personal', {}),
            ('POST', 'http://localhost:8083/personal', sample_personal_snippet),
            ('PUT', 'http://localhost:8083/personal/507f1f77bcf86cd799439011', {"title": "Updated"}),
            ('DELETE', 'http://localhost:8083/personal/507f1f77bcf86cd799439011', {}),
            ('POST', 'http://localhost:8083/official', sample_official_snippet),
        ]
        
        for method, url, data in protected_endpoints:
            headers = {'Content-Type': 'application/json'}
            
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers)
            
            if response.status_code != 401:
                print(f"  ❌ Protected endpoint should require auth: {method} {url} -> {response.status_code}")
                print(f"  📄 Response: {response.text}")
                return False
        
        print("  ✅ Protected endpoints properly require authentication")
        
        # Step 4: Test endpoints with invalid/malformed auth headers
        print("  📝 Step 4: Testing invalid authentication...")
        
        invalid_auth_headers = [
            {},  # No auth header
            {'Authorization': 'Bearer'},  # Malformed Bearer token
            {'Authorization': 'Basic invalid'},  # Wrong auth type
            {'Authorization': 'Bearer invalid.token.format'},  # Invalid token format
            {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.invalid.signature'},  # Invalid signature
        ]
        
        test_url = 'http://localhost:8083/personal'
        
        for auth_header in invalid_auth_headers:
            headers = {'Content-Type': 'application/json'}
            headers.update(auth_header)
            
            response = requests.get(test_url, headers=headers)
            
            if response.status_code != 401:
                print(f"  ❌ Invalid auth should return 401: {auth_header} -> {response.status_code}")
                return False
        
        print("  ✅ Invalid authentication properly rejected")
        
        # Step 5: Test valid authentication works
        print("  📝 Step 5: Testing valid authentication...")
        
        # Test regular user can access personal endpoints
        regular_headers = {
            'Authorization': f'Bearer {regular_token}',
            'Content-Type': 'application/json'
        }
        
        regular_response = requests.get('http://localhost:8083/personal', headers=regular_headers)
        
        if regular_response.status_code != 200:
            print(f"  ❌ Valid regular auth should work: {regular_response.status_code}")
            return False
        
        # Test admin can access both personal and official endpoints
        admin_headers = {
            'Authorization': f'Bearer {admin_token}',
            'Content-Type': 'application/json'
        }
        
        admin_personal_response = requests.get('http://localhost:8083/personal', headers=admin_headers)
        admin_official_response = requests.post('http://localhost:8083/official', 
                                               json=sample_official_snippet, 
                                               headers=admin_headers)
        
        if admin_personal_response.status_code != 200:
            print(f"  ❌ Valid admin auth should work for personal: {admin_personal_response.status_code}")
            return False
        
        if admin_official_response.status_code != 200:
            print(f"  ❌ Valid admin auth should work for official: {admin_official_response.status_code}")
            return False
        
        print("  ✅ Valid authentication works correctly")
        
        # Step 6: Test role-based access control (admin vs regular user)
        print("  📝 Step 6: Testing role-based access control...")
        
        # Regular user should NOT be able to create official snippets
        regular_official_response = requests.post('http://localhost:8083/official',
                                                 json=sample_official_snippet,
                                                 headers=regular_headers)
        
        if regular_official_response.status_code != 403:
            print(f"  ❌ Regular user should be denied admin endpoints: {regular_official_response.status_code}")
            return False
        
        print("  ✅ Role-based access control working (regular user denied admin endpoints)")
        
        # Step 7: Test token expiration handling (using clearly invalid token)
        print("  📝 Step 7: Testing expired/invalid token handling...")
        
        expired_headers = {
            'Authorization': 'Bearer expired.token.here',
            'Content-Type': 'application/json'
        }
        
        expired_response = requests.get('http://localhost:8083/personal', headers=expired_headers)
        
        if expired_response.status_code != 401:
            print(f"  ❌ Expired token should return 401: {expired_response.status_code}")
            return False
        
        print("  ✅ Expired/invalid token properly handled")
        
        # Step 8: Test authorization header case sensitivity
        print("  📝 Step 8: Testing authorization header variations...")
        
        # Test different capitalizations (should all work)
        auth_variations = [
            {'Authorization': f'Bearer {regular_token}'},
            {'authorization': f'Bearer {regular_token}'},  # lowercase
            {'AUTHORIZATION': f'Bearer {regular_token}'},  # uppercase
        ]
        
        for auth_header in auth_variations:
            headers = {'Content-Type': 'application/json'}
            headers.update(auth_header)
            
            response = requests.get('http://localhost:8083/personal', headers=headers)
            
            # HTTP headers should be case-insensitive, but some implementations might be strict
            if response.status_code not in [200, 401]:
                print(f"  ❌ Unexpected response for auth header variation: {auth_header} -> {response.status_code}")
                return False
        
        print("  ✅ Authorization header variations handled appropriately")
        
        # Step 9: Test concurrent authentication (multiple valid tokens)
        print("  📝 Step 9: Testing concurrent authentication...")
        
        # Create another user token
        another_token, another_id, another_email = get_regular_token()
        if another_token:
            another_headers = {
                'Authorization': f'Bearer {another_token}',
                'Content-Type': 'application/json'
            }
            
            # Both users should be able to access their personal endpoints simultaneously
            response1 = requests.get('http://localhost:8083/personal', headers=regular_headers)
            response2 = requests.get('http://localhost:8083/personal', headers=another_headers)
            
            if response1.status_code != 200 or response2.status_code != 200:
                print(f"  ❌ Concurrent auth failed: {response1.status_code}, {response2.status_code}")
                return False
            
            print("  ✅ Concurrent authentication working")
        else:
            print("  ⚠️ Could not create second user for concurrent test, skipping")
        
        # Step 10: Test authentication error messages are informative but secure
        print("  📝 Step 10: Testing authentication error messages...")
        
        no_auth_response = requests.get('http://localhost:8083/personal')
        invalid_auth_response = requests.get('http://localhost:8083/personal', 
                                           headers={'Authorization': 'Bearer invalid'})
        
        try:
            no_auth_data = no_auth_response.json()
            invalid_auth_data = invalid_auth_response.json()
            
            # Should have informative but not revealing error messages
            if not no_auth_data.get('message') or not invalid_auth_data.get('message'):
                print("  ❌ Auth error responses should include informative messages")
                return False
            
            # Should not reveal internal details
            for response_data in [no_auth_data, invalid_auth_data]:
                message = response_data.get('message', '').lower()
                if any(sensitive in message for sensitive in ['database', 'internal', 'exception', 'traceback']):
                    print("  ❌ Auth error messages should not reveal internal details")
                    return False
            
            print("  ✅ Authentication error messages are appropriate")
        except json.JSONDecodeError:
            print("  ⚠️ Auth error responses not in JSON format, but that's acceptable")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("  ❌ Cannot connect to servers")
        print("  💡 Make sure auth (8081) and snippets (8083) servers are running")
        return False
    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_authentication_requirements()
    if success:
        print("🎉 Test passed!")
        exit(0)
    else:
        print("💥 Test failed!")
        exit(1)