#!/usr/bin/env python3
"""
Test 02: Token Refresh
Tests the /refresh endpoint for refreshing access tokens
"""

import requests
import json
from datetime import datetime

def test_token_refresh():
    """Test refreshing access token using refresh token"""
    print("🧪 Testing Token Refresh...")
    
    try:
        # First, create a user to get a refresh token
        print("  📝 Step 1: Creating user to get refresh token...")
        test_user_data = {
            "email": f"test_refresh_{datetime.now().strftime('%Y%m%d_%H%M%S')}@example.com",
            "name": "Test Refresh User",
            "avatar": "https://example.com/avatar.jpg"
        }
        
        auth_response = requests.post(
            'http://localhost:8081/google-auth',
            json=test_user_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if auth_response.status_code != 200:
            print(f"  ❌ Failed to create test user: {auth_response.status_code}")
            return False
        
        auth_data = auth_response.json()
        if not auth_data.get('success'):
            print(f"  ❌ Auth failed: {auth_data.get('message')}")
            return False
        
        refresh_token = auth_data['data']['refreshToken']
        original_access_token = auth_data['data']['token']
        user_id = auth_data['data']['user']['id']
        
        print(f"  ✅ User created with ID: {user_id}")
        print("  🔑 Got refresh token for testing")
        
        # Now test token refresh
        print("  📝 Step 2: Testing token refresh...")
        
        refresh_request_data = {
            "refreshToken": refresh_token
        }
        
        refresh_response = requests.post(
            'http://localhost:8081/refresh',
            json=refresh_request_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"  📡 Refresh response status: {refresh_response.status_code}")
        
        # Check response status
        if refresh_response.status_code != 200:
            print(f"  ❌ Expected 200, got {refresh_response.status_code}")
            print(f"  📄 Response: {refresh_response.text}")
            return False
        
        # Parse response
        try:
            refresh_data = refresh_response.json()
        except json.JSONDecodeError:
            print("  ❌ Invalid JSON response")
            print(f"  📄 Response: {refresh_response.text}")
            return False
        
        # Validate response structure
        if not refresh_data.get('success'):
            print(f"  ❌ Refresh failed: {refresh_data.get('message', 'Unknown error')}")
            return False
        
        # Check required fields in response
        response_data = refresh_data.get('data', {})
        required_fields = ['token', 'user']
        
        for field in required_fields:
            if field not in response_data:
                print(f"  ❌ Missing required field: {field}")
                return False
        
        # Validate new access token
        new_access_token = response_data['token']
        if not isinstance(new_access_token, str) or len(new_access_token) < 10:
            print("  ❌ Invalid new access token")
            return False
        
        # Ensure new token is different from original
        if new_access_token == original_access_token:
            print("  ❌ New access token should be different from original")
            return False
        
        # Validate user data in refresh response
        user = response_data.get('user', {})
        user_required_fields = ['id', 'email', 'name', 'avatar', 'role']
        
        for field in user_required_fields:
            if field not in user:
                print(f"  ❌ Missing user field: {field}")
                return False
        
        # Validate user data consistency
        if user['id'] != user_id:
            print(f"  ❌ User ID mismatch: expected {user_id}, got {user['id']}")
            return False
        
        if user['email'] != test_user_data['email']:
            print(f"  ❌ Email mismatch in refresh response")
            return False
        
        print("  ✅ Token refresh successful")
        print("  🔑 New access token generated")
        print(f"  👤 User data consistent: {user['email']}")
        
        # Test with invalid refresh token
        print("  📝 Step 3: Testing with invalid refresh token...")
        
        invalid_refresh_data = {
            "refreshToken": "invalid.token.here"
        }
        
        invalid_response = requests.post(
            'http://localhost:8081/refresh',
            json=invalid_refresh_data,
            headers={'Content-Type': 'application/json'}
        )
        
        # Should return 401 for invalid token
        if invalid_response.status_code != 401:
            print(f"  ❌ Expected 401 for invalid token, got {invalid_response.status_code}")
            return False
        
        invalid_data = invalid_response.json()
        if invalid_data.get('success'):
            print("  ❌ Invalid token should not succeed")
            return False
        
        print("  ✅ Invalid token properly rejected")
        
        # Test with missing refresh token
        print("  📝 Step 4: Testing with missing refresh token...")
        
        missing_token_response = requests.post(
            'http://localhost:8081/refresh',
            json={},
            headers={'Content-Type': 'application/json'}
        )
        
        # Should return 400 for missing token
        if missing_token_response.status_code != 400:
            print(f"  ❌ Expected 400 for missing token, got {missing_token_response.status_code}")
            return False
        
        print("  ✅ Missing token properly rejected")

        # Test with malformed (non-string) refresh token: integer
        print("  📝 Step 5: Testing with integer refresh token...")
        int_token_response = requests.post(
            'http://localhost:8081/refresh',
            json={'refreshToken': 12345},
            headers={'Content-Type': 'application/json'}
        )
        if int_token_response.status_code != 400:
            print(f"  ❌ Expected 400 for integer token, got {int_token_response.status_code}")
            return False
        print("  ✅ Integer token properly rejected")

        # Test with malformed (non-string) refresh token: null
        print("  📝 Step 6: Testing with null refresh token...")
        null_token_response = requests.post(
            'http://localhost:8081/refresh',
            json={'refreshToken': None},
            headers={'Content-Type': 'application/json'}
        )
        if null_token_response.status_code != 400:
            print(f"  ❌ Expected 400 for null token, got {null_token_response.status_code}")
            return False
        print("  ✅ Null token properly rejected")

        return True
        
    except requests.exceptions.ConnectionError:
        print("  ❌ Cannot connect to auth server")
        print("  💡 Make sure auth server is running: cd ../../auth && python main.py")
        return False
    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_token_refresh()
    if success:
        print("🎉 Test passed!")
        exit(0)
    else:
        print("💥 Test failed!")
        exit(1)