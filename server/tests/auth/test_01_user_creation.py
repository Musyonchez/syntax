#!/usr/bin/env python3
"""
Test 01: User Creation via Google OAuth
Tests the /google-auth endpoint for creating new users
"""

import requests
import json
from datetime import datetime

def test_user_creation():
    """Test creating a new user via Google OAuth endpoint"""
    print("🧪 Testing User Creation...")
    
    try:
        # Test data - simulating Google OAuth data
        test_user_data = {
            "email": f"test_user_{datetime.now().strftime('%Y%m%d_%H%M%S')}@example.com",
            "name": "Test User",
            "avatar": "https://example.com/avatar.jpg"
        }
        
        print(f"  📧 Testing with email: {test_user_data['email']}")
        
        # Make request to auth endpoint
        response = requests.post(
            'http://localhost:8081/google-auth',
            json=test_user_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"  📡 Response status: {response.status_code}")
        
        # Check response
        if response.status_code != 200:
            print(f"  ❌ Expected 200, got {response.status_code}")
            print(f"  📄 Response: {response.text}")
            return False
        
        # Parse response
        try:
            data = response.json()
        except json.JSONDecodeError:
            print("  ❌ Invalid JSON response")
            print(f"  📄 Response: {response.text}")
            return False
        
        # Validate response structure
        if not data.get('success'):
            print(f"  ❌ Request failed: {data.get('message', 'Unknown error')}")
            return False
        
        # Check required fields in response
        response_data = data.get('data', {})
        required_fields = ['token', 'refreshToken', 'user']
        
        for field in required_fields:
            if field not in response_data:
                print(f"  ❌ Missing required field: {field}")
                return False
        
        # Validate user object
        user = response_data.get('user', {})
        user_required_fields = ['id', 'email', 'name', 'avatar', 'role']
        
        for field in user_required_fields:
            if field not in user:
                print(f"  ❌ Missing user field: {field}")
                return False
        
        # Validate user data matches input
        if user['email'] != test_user_data['email']:
            print(f"  ❌ Email mismatch: expected {test_user_data['email']}, got {user['email']}")
            return False
        
        if user['name'] != test_user_data['name']:
            print(f"  ❌ Name mismatch: expected {test_user_data['name']}, got {user['name']}")
            return False
        
        # Validate tokens are strings and not empty
        if not isinstance(response_data['token'], str) or len(response_data['token']) < 10:
            print("  ❌ Invalid access token")
            return False
        
        if not isinstance(response_data['refreshToken'], str) or len(response_data['refreshToken']) < 10:
            print("  ❌ Invalid refresh token")
            return False
        
        # Validate default role
        if user['role'] != 'user':
            print(f"  ❌ Expected default role 'user', got '{user['role']}'")
            return False
        
        print("  ✅ User created successfully")
        print(f"  👤 User ID: {user['id']}")
        print(f"  📧 Email: {user['email']}")
        print(f"  👥 Role: {user['role']}")
        print("  🔑 Tokens generated successfully")
        
        # Store user data for other tests (if needed)
        # Note: Not cleaning up as per user request - development database
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("  ❌ Cannot connect to auth server")
        print("  💡 Make sure auth server is running: cd ../../auth && python main.py")
        return False
    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        return False

if __name__ == '__main__':
    success = test_user_creation()
    if success:
        print("🎉 Test passed!")
        exit(0)
    else:
        print("💥 Test failed!")
        exit(1)