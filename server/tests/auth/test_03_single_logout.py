#!/usr/bin/env python3
"""
Test 03: Single Device Logout
Tests the /logout endpoint for logging out from current device
"""

import requests
import json
from datetime import datetime

def test_single_logout():
    """Test single device logout using refresh token"""
    print("🧪 Testing Single Device Logout...")
    
    try:
        # First, create a user to get tokens
        print("  📝 Step 1: Creating user to get tokens...")
        test_user_data = {
            "email": f"test_logout_{datetime.now().strftime('%Y%m%d_%H%M%S')}@example.com",
            "name": "Test Logout User",
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
        user_id = auth_data['data']['user']['id']
        
        print(f"  ✅ User created with ID: {user_id}")
        print("  🔑 Got refresh token for testing")
        
        # Verify refresh token works before logout
        print("  📝 Step 2: Verifying refresh token works...")
        
        refresh_response = requests.post(
            'http://localhost:8081/refresh',
            json={"refreshToken": refresh_token},
            headers={'Content-Type': 'application/json'}
        )
        
        if refresh_response.status_code != 200:
            print(f"  ❌ Refresh token not working initially: {refresh_response.status_code}")
            return False
        
        print("  ✅ Refresh token working before logout")
        
        # Now test single device logout
        print("  📝 Step 3: Testing single device logout...")
        
        logout_request_data = {
            "refreshToken": refresh_token
        }
        
        logout_response = requests.post(
            'http://localhost:8081/logout',
            json=logout_request_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"  📡 Logout response status: {logout_response.status_code}")
        
        # Check response status
        if logout_response.status_code != 200:
            print(f"  ❌ Expected 200, got {logout_response.status_code}")
            print(f"  📄 Response: {logout_response.text}")
            return False
        
        # Parse response
        try:
            logout_data = logout_response.json()
        except json.JSONDecodeError:
            print("  ❌ Invalid JSON response")
            print(f"  📄 Response: {logout_response.text}")
            return False
        
        # Validate response structure
        if not logout_data.get('success'):
            print(f"  ❌ Logout failed: {logout_data.get('message', 'Unknown error')}")
            return False
        
        # Check response data
        response_data = logout_data.get('data', {})
        if 'revokedToken' not in response_data:
            print("  ❌ Missing revokedToken field in response")
            return False
        
        print("  ✅ Logout successful")
        print(f"  🔑 Token revoked: {response_data.get('revokedToken')}")
        
        # Verify refresh token no longer works after logout
        print("  📝 Step 4: Verifying refresh token no longer works...")
        
        post_logout_refresh = requests.post(
            'http://localhost:8081/refresh',
            json={"refreshToken": refresh_token},
            headers={'Content-Type': 'application/json'}
        )
        
        # Should return 401 since token was revoked
        if post_logout_refresh.status_code != 401:
            print(f"  ❌ Expected 401 for revoked token, got {post_logout_refresh.status_code}")
            return False
        
        post_logout_data = post_logout_refresh.json()
        if post_logout_data.get('success'):
            print("  ❌ Revoked token should not work for refresh")
            return False
        
        print("  ✅ Refresh token properly revoked after logout")
        
        # Test logout with already revoked token (should still succeed gracefully)
        print("  📝 Step 5: Testing logout with already revoked token...")
        
        second_logout_response = requests.post(
            'http://localhost:8081/logout',
            json={"refreshToken": refresh_token},
            headers={'Content-Type': 'application/json'}
        )
        
        # Should still return 200 (graceful handling)
        if second_logout_response.status_code != 200:
            print(f"  ❌ Expected graceful 200 for already revoked token, got {second_logout_response.status_code}")
            return False
        
        second_logout_data = second_logout_response.json()
        if not second_logout_data.get('success'):
            print("  ❌ Second logout should succeed gracefully")
            return False
        
        print("  ✅ Already revoked token handled gracefully")
        
        # Test logout with invalid token
        print("  📝 Step 6: Testing logout with invalid token...")
        
        invalid_logout_response = requests.post(
            'http://localhost:8081/logout',
            json={"refreshToken": "invalid.token.here"},
            headers={'Content-Type': 'application/json'}
        )
        
        # Should still return 200 (graceful handling)
        if invalid_logout_response.status_code != 200:
            print(f"  ❌ Expected graceful 200 for invalid token, got {invalid_logout_response.status_code}")
            return False
        
        print("  ✅ Invalid token handled gracefully")
        
        # Test logout with missing token
        print("  📝 Step 7: Testing logout with missing token...")
        
        missing_token_response = requests.post(
            'http://localhost:8081/logout',
            json={},
            headers={'Content-Type': 'application/json'}
        )
        
        # Should return 400 for missing token
        if missing_token_response.status_code != 400:
            print(f"  ❌ Expected 400 for missing token, got {missing_token_response.status_code}")
            return False
        
        print("  ✅ Missing token properly rejected")
        
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
    success = test_single_logout()
    if success:
        print("🎉 Test passed!")
        exit(0)
    else:
        print("💥 Test failed!")
        exit(1)