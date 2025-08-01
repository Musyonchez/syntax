#!/usr/bin/env python3
"""
Test 05: Enhanced Schema Validation
Tests robust input validation and data sanitization for auth endpoints
"""

import requests
import json
from datetime import datetime

def test_schema_validation():
    """Test enhanced schema validation for auth endpoints"""
    print("🧪 Testing Enhanced Schema Validation...")
    
    try:
        # Test 1: Missing required fields
        print("  📝 Step 1: Testing missing required fields...")
        
        # Missing email
        invalid_data_1 = {
            "name": "Test User",
            "avatar": "https://example.com/avatar.jpg"
        }
        
        response_1 = requests.post(
            'http://localhost:8081/google-auth',
            json=invalid_data_1,
            headers={'Content-Type': 'application/json'}
        )
        
        if response_1.status_code != 400:
            print(f"  ❌ Expected 400 for missing email, got {response_1.status_code}")
            return False
        
        print("  ✅ Missing email properly rejected")
        
        # Missing name
        invalid_data_2 = {
            "email": "test@example.com",
            "avatar": "https://example.com/avatar.jpg"
        }
        
        response_2 = requests.post(
            'http://localhost:8081/google-auth',
            json=invalid_data_2,
            headers={'Content-Type': 'application/json'}
        )
        
        if response_2.status_code != 400:
            print(f"  ❌ Expected 400 for missing name, got {response_2.status_code}")
            return False
        
        print("  ✅ Missing name properly rejected")
        
        # Test 2: Invalid email formats (with improved validation)
        print("  📝 Step 2: Testing invalid email formats...")
        
        invalid_emails = [
            "not-an-email",           # No @ symbol
            "missing@domain",         # No TLD
            "@missinguser.com",       # No local part
            "user@",                  # No domain
            "user@domain",            # No TLD
            "spaces in@domain.com",   # Spaces not allowed
            "",                       # Empty string
            "user..double@domain.com", # Consecutive dots
            ".user@domain.com",       # Starts with dot
            "user.@domain.com",       # Ends with dot
        ]
        
        for invalid_email in invalid_emails:
            invalid_email_data = {
                "email": invalid_email,
                "name": "Test User",
                "avatar": "https://example.com/avatar.jpg"
            }
            
            email_response = requests.post(
                'http://localhost:8081/google-auth',
                json=invalid_email_data,
                headers={'Content-Type': 'application/json'}
            )
            
            if email_response.status_code != 400:
                print(f"  ❌ Invalid email '{invalid_email}' should be rejected (got {email_response.status_code})")
                return False
        
        print("  ✅ Invalid email formats properly rejected")
        
        # Test 3: Valid email formats
        print("  📝 Step 3: Testing valid email formats...")
        
        valid_emails = [
            "user@domain.com",
            "test.user@example.org",
            "user+tag@domain.co.uk",
            "user123@domain123.com",
        ]
        
        for valid_email in valid_emails:
            valid_email_data = {
                "email": valid_email,
                "name": "Test User",
                "avatar": "https://example.com/avatar.jpg"
            }
            
            email_response = requests.post(
                'http://localhost:8081/google-auth',
                json=valid_email_data,
                headers={'Content-Type': 'application/json'}
            )
            
            if email_response.status_code != 200:
                print(f"  ❌ Valid email '{valid_email}' should be accepted (got {email_response.status_code})")
                return False
        
        print("  ✅ Valid email formats properly accepted")
        
        # Test 4: Invalid name formats
        print("  📝 Step 4: Testing invalid name formats...")
        
        invalid_names = [
            "",                    # Empty string
            "A",                   # Too short (< 2 chars)
            "A" * 101,            # Too long (> 100 chars)
            "User<script>",       # XSS attempt
            "User>alert",         # XSS attempt
            "User&amp;",          # HTML entity
            ["Not", "String"],    # Wrong type
            123,                  # Wrong type
        ]
        
        for invalid_name in invalid_names:
            invalid_name_data = {
                "email": f"test_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}@example.com",
                "name": invalid_name,
                "avatar": "https://example.com/avatar.jpg"
            }
            
            name_response = requests.post(
                'http://localhost:8081/google-auth',
                json=invalid_name_data,
                headers={'Content-Type': 'application/json'}
            )
            
            if name_response.status_code != 400:
                print(f"  ❌ Invalid name '{invalid_name}' should be rejected (got {name_response.status_code})")
                return False
        
        print("  ✅ Invalid name formats properly rejected")
        
        # Test 5: Invalid avatar URLs
        print("  📝 Step 5: Testing invalid avatar URLs...")
        
        invalid_avatars = [
            "not-a-url",                    # No protocol
            "ftp://example.com/image.jpg",  # Wrong protocol
            "https://example.com/image<script>", # XSS attempt
            "https://example.com/image\"", # Quote injection
            "https://example.com/image'",  # Quote injection
            "A" * 501,                     # Too long
            123,                           # Wrong type
        ]
        
        for invalid_avatar in invalid_avatars:
            invalid_avatar_data = {
                "email": f"test_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}@example.com",
                "name": "Test User",
                "avatar": invalid_avatar
            }
            
            avatar_response = requests.post(
                'http://localhost:8081/google-auth',
                json=invalid_avatar_data,
                headers={'Content-Type': 'application/json'}
            )
            
            if avatar_response.status_code != 400:
                print(f"  ❌ Invalid avatar '{invalid_avatar}' should be rejected (got {avatar_response.status_code})")
                return False
        
        print("  ✅ Invalid avatar URLs properly rejected")
        
        # Test 6: Valid avatar URLs (including empty)
        print("  📝 Step 6: Testing valid avatar URLs...")
        
        valid_avatars = [
            "",                                    # Empty (allowed)
            "https://example.com/avatar.jpg",      # HTTPS
            "http://example.com/avatar.png",       # HTTP
            "https://cdn.example.com/user/123.gif", # Complex URL
        ]
        
        for valid_avatar in valid_avatars:
            valid_avatar_data = {
                "email": f"test_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}@example.com",
                "name": "Test User",
                "avatar": valid_avatar
            }
            
            avatar_response = requests.post(
                'http://localhost:8081/google-auth',
                json=valid_avatar_data,
                headers={'Content-Type': 'application/json'}
            )
            
            if avatar_response.status_code != 200:
                print(f"  ❌ Valid avatar '{valid_avatar}' should be accepted (got {avatar_response.status_code})")
                return False
        
        print("  ✅ Valid avatar URLs properly accepted")
        
        # Test 7: Field length limits
        print("  📝 Step 7: Testing field length limits...")
        
        # Test maximum email length (254 chars)
        long_email = "a" * (254 - len("@example.com")) + "@example.com"
        too_long_email = "a" * (255 - len("@example.com")) + "@example.com"
        
        # Valid max length email
        max_email_data = {
            "email": long_email,
            "name": "Test User",
            "avatar": "https://example.com/avatar.jpg"
        }
        
        max_email_response = requests.post(
            'http://localhost:8081/google-auth',
            json=max_email_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if max_email_response.status_code != 200:
            print(f"  ❌ Max length email should be accepted (got {max_email_response.status_code})")
            return False
        
        # Too long email
        too_long_email_data = {
            "email": too_long_email,
            "name": "Test User",
            "avatar": "https://example.com/avatar.jpg"
        }
        
        too_long_response = requests.post(
            'http://localhost:8081/google-auth',
            json=too_long_email_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if too_long_response.status_code != 400:
            print(f"  ❌ Too long email should be rejected (got {too_long_response.status_code})")
            return False
        
        print("  ✅ Field length limits properly enforced")
        
        # Test 8: Data type validation  
        print("  📝 Step 8: Testing data type validation...")
        
        # Test various type validation scenarios
        type_validation_tests = [
            ({"email": 12345, "name": "Test User", "avatar": "https://example.com/avatar.jpg"}, "non-string email"),
            ({"email": "test@example.com", "name": 12345, "avatar": "https://example.com/avatar.jpg"}, "non-string name"),
            ({"email": "test@example.com", "name": "Test User", "avatar": 12345}, "non-string avatar"),
            ({"email": "test@example.com", "name": "Test User", "avatar": "https://example.com/avatar.jpg", "role": 12345}, "non-string role"),
            ({"email": "test@example.com", "name": "Test User", "avatar": "https://example.com/avatar.jpg", "role": ["admin"]}, "non-string role array"),
            ({"email": "test@example.com", "name": "Test User", "avatar": "https://example.com/avatar.jpg", "role": "invalid_role"}, "invalid role value"),
        ]
        
        for invalid_data, description in type_validation_tests:
            type_response = requests.post(
                'http://localhost:8081/google-auth',
                json=invalid_data,
                headers={'Content-Type': 'application/json'}
            )
            
            if type_response.status_code != 400:
                print(f"  ❌ Expected 400 for {description}, got {type_response.status_code}")
                print(f"  📄 Response: {type_response.text}")
                return False
        
        print("  ✅ Data type validation working (including strict role validation)")
        
        # Test 9: Refresh token validation
        print("  📝 Step 9: Testing refresh token validation...")
        
        # Missing refresh token
        missing_refresh = requests.post(
            'http://localhost:8081/refresh',
            json={},
            headers={'Content-Type': 'application/json'}
        )
        
        if missing_refresh.status_code != 400:
            print(f"  ❌ Missing refresh token should return 400 (got {missing_refresh.status_code})")
            return False
        
        print("  ✅ Refresh token validation working")
        
        # Test 10: Authorization header validation
        print("  📝 Step 10: Testing authorization header validation...")
        
        # Malformed authorization header
        malformed_auth = requests.post(
            'http://localhost:8081/logout-all',
            headers={
                'Authorization': 'NotBearer token',
                'Content-Type': 'application/json'
            }
        )
        
        if malformed_auth.status_code != 401:
            print(f"  ❌ Malformed auth header should return 401 (got {malformed_auth.status_code})")
            return False
        
        print("  ✅ Authorization header validation working")
        
        # Final test: Valid data still works after all validation
        print("  📝 Step 11: Testing valid data still works...")
        
        final_valid_data = {
            "email": f"test_final_{datetime.now().strftime('%Y%m%d_%H%M%S')}@example.com",
            "name": "Final Test User",
            "avatar": "https://example.com/final-avatar.jpg"
        }
        
        final_response = requests.post(
            'http://localhost:8081/google-auth',
            json=final_valid_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if final_response.status_code != 200:
            print(f"  ❌ Final valid data should work (got {final_response.status_code})")
            print(f"  📄 Response: {final_response.text}")
            return False
        
        print("  ✅ Valid data still works after all validation tests")
        
        # Test 12: Valid role values still work
        print("  📝 Step 12: Testing valid role values...")
        
        valid_role_tests = [
            ({"email": f"test_admin_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}@example.com", "name": "Admin User", "avatar": "https://example.com/avatar.jpg", "role": "admin"}, "admin role"),
            ({"email": f"test_user_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}@example.com", "name": "Regular User", "avatar": "https://example.com/avatar.jpg", "role": "user"}, "user role"),
            ({"email": f"test_default_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}@example.com", "name": "Default User", "avatar": "https://example.com/avatar.jpg"}, "default role (no role specified)"),
        ]
        
        for valid_data, description in valid_role_tests:
            role_response = requests.post(
                'http://localhost:8081/google-auth',
                json=valid_data,
                headers={'Content-Type': 'application/json'}
            )
            
            if role_response.status_code != 200:
                print(f"  ❌ Valid {description} should be accepted (got {role_response.status_code})")
                print(f"  📄 Response: {role_response.text}")
                return False
        
        print("  ✅ Valid role values properly accepted")
        
        # Test 13: Session schema validation (testing the third auth schema)
        print("  📝 Step 13: Testing session schema validation...")
        
        # Note: We can't directly test the session endpoints since they're not implemented yet,
        # but we can test the schema validation logic directly through unit testing.
        # For now, we'll focus on ensuring the existing auth endpoints work correctly.
        # Once the practice/session endpoints are implemented, we should add full session validation tests.
        
        print("  ⚠️  Session schema validation needs endpoint implementation for full testing")
        print("  ✅ Auth schema validation comprehensive (users and tokens fully tested)")
        
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
    success = test_schema_validation()
    if success:
        print("🎉 Test passed!")
        exit(0)
    else:
        print("💥 Test failed!")
        exit(1)