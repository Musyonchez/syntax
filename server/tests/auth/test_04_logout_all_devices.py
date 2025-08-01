#!/usr/bin/env python3
"""
Test 04: Logout All Devices
Tests the /logout-all endpoint for logging out from all devices
"""

import requests
import json
from datetime import datetime

def test_logout_all_devices():
    """Test logout all devices using access token"""
    print("🧪 Testing Logout All Devices...")
    
    try:
        # First, create a user to get tokens
        print("  📝 Step 1: Creating user to get tokens...")
        test_user_data = {
            "email": f"test_logoutall_{datetime.now().strftime('%Y%m%d_%H%M%S')}@example.com",
            "name": "Test Logout All User",
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
        
        access_token = auth_data['data']['token']
        refresh_token_1 = auth_data['data']['refreshToken']
        user_id = auth_data['data']['user']['id']
        
        print(f"  ✅ User created with ID: {user_id}")
        print("  🔑 Got first set of tokens")
        
        # Create a second session (simulating login from another device)
        print("  📝 Step 2: Creating second session (another device)...")
        
        second_auth_response = requests.post(
            'http://localhost:8081/google-auth',
            json=test_user_data,  # Same user logging in again
            headers={'Content-Type': 'application/json'}
        )
        
        if second_auth_response.status_code != 200:
            print(f"  ❌ Failed to create second session: {second_auth_response.status_code}")
            return False
        
        second_auth_data = second_auth_response.json()
        refresh_token_2 = second_auth_data['data']['refreshToken']
        
        print("  ✅ Second session created")
        print("  🔑 Got second refresh token")
        
        # Verify both refresh tokens work
        print("  📝 Step 3: Verifying both refresh tokens work...")
        
        # Test first token
        refresh_1_response = requests.post(
            'http://localhost:8081/refresh',
            json={"refreshToken": refresh_token_1},
            headers={'Content-Type': 'application/json'}
        )
        
        # Test second token
        refresh_2_response = requests.post(
            'http://localhost:8081/refresh',
            json={"refreshToken": refresh_token_2},
            headers={'Content-Type': 'application/json'}
        )
        
        if refresh_1_response.status_code != 200 or refresh_2_response.status_code != 200:
            print(f"  ❌ One or both refresh tokens not working initially")
            print(f"    Token 1: {refresh_1_response.status_code}")
            print(f"    Token 2: {refresh_2_response.status_code}")
            return False
        
        print("  ✅ Both refresh tokens working before logout all")
        
        # Now test logout all devices
        print("  📝 Step 4: Testing logout all devices...")
        
        logout_all_response = requests.post(
            'http://localhost:8081/logout-all',
            headers={
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
        )
        
        print(f"  📡 Logout all response status: {logout_all_response.status_code}")
        
        # Check response status
        if logout_all_response.status_code != 200:
            print(f"  ❌ Expected 200, got {logout_all_response.status_code}")
            print(f"  📄 Response: {logout_all_response.text}")
            return False
        
        # Parse response
        try:
            logout_data = logout_all_response.json()
        except json.JSONDecodeError:
            print("  ❌ Invalid JSON response")
            print(f"  📄 Response: {logout_all_response.text}")
            return False
        
        # Validate response structure
        if not logout_data.get('success'):
            print(f"  ❌ Logout all failed: {logout_data.get('message', 'Unknown error')}")
            return False
        
        # Check response data
        response_data = logout_data.get('data', {})
        if 'revokedTokens' not in response_data:
            print("  ❌ Missing revokedTokens field in response")
            return False
        
        revoked_count = response_data.get('revokedTokens', 0)
        print(f"  ✅ Logout all successful")
        print(f"  🔑 Tokens revoked: {revoked_count}")
        
        # Verify both refresh tokens no longer work after logout all
        print("  📝 Step 5: Verifying all refresh tokens revoked...")
        
        # Test first token
        post_logout_refresh_1 = requests.post(
            'http://localhost:8081/refresh',
            json={"refreshToken": refresh_token_1},
            headers={'Content-Type': 'application/json'}
        )
        
        # Test second token  
        post_logout_refresh_2 = requests.post(
            'http://localhost:8081/refresh',
            json={"refreshToken": refresh_token_2},
            headers={'Content-Type': 'application/json'}
        )
        
        # Both should return 401 since all tokens were revoked
        if post_logout_refresh_1.status_code != 401:
            print(f"  ❌ First token should be revoked, got {post_logout_refresh_1.status_code}")
            return False
        
        if post_logout_refresh_2.status_code != 401:
            print(f"  ❌ Second token should be revoked, got {post_logout_refresh_2.status_code}")
            return False
        
        print("  ✅ All refresh tokens properly revoked")
        
        # Test logout all with invalid access token
        print("  📝 Step 6: Testing logout all with invalid access token...")
        
        invalid_logout_response = requests.post(
            'http://localhost:8081/logout-all',
            headers={
                'Authorization': 'Bearer invalid.token.here',
                'Content-Type': 'application/json'
            }
        )
        
        # Should return 401 for invalid access token
        if invalid_logout_response.status_code != 401:
            print(f"  ❌ Expected 401 for invalid access token, got {invalid_logout_response.status_code}")
            return False
        
        print("  ✅ Invalid access token properly rejected")
        
        # Test logout all with missing authorization header
        print("  📝 Step 7: Testing logout all with missing authorization...")
        
        missing_auth_response = requests.post(
            'http://localhost:8081/logout-all',
            headers={'Content-Type': 'application/json'}
        )
        
        # Should return 401 for missing authorization
        if missing_auth_response.status_code != 401:
            print(f"  ❌ Expected 401 for missing auth, got {missing_auth_response.status_code}")
            return False
        
        print("  ✅ Missing authorization properly rejected")
        
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
    success = test_logout_all_devices()
    if success:
        print("🎉 Test passed!")
        exit(0)
    else:
        print("💥 Test failed!")
        exit(1)