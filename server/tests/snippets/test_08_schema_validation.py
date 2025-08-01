#!/usr/bin/env python3
"""
Test 08: Schema Validation
Tests comprehensive schema validation for both personal and official snippets
"""

import requests
import json
from datetime import datetime

def get_regular_token():
    """Helper function to get a regular user auth token"""
    test_user_data = {
        "email": f"test_schema_validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}@example.com",
        "name": "Test Schema Validation User",
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

def test_schema_validation():
    """Test comprehensive schema validation for personal and official snippets"""
    print("🧪 Testing Schema Validation...")
    
    try:
        # Step 1: Get authentication tokens
        print("  📝 Step 1: Getting authentication tokens...")
        
        regular_token, regular_id, regular_email = get_regular_token()
        admin_token, admin_id, admin_email = get_admin_token()
        
        if not regular_token or not admin_token:
            print("  ❌ Failed to get required authentication tokens")
            return False
        
        print(f"  ✅ Got tokens for validation testing")
        
        # Step 2: Test personal snippet required fields validation
        print("  📝 Step 2: Testing personal snippet required fields...")
        
        regular_headers = {
            'Authorization': f'Bearer {regular_token}',
            'Content-Type': 'application/json'
        }
        
        # Test missing required fields
        required_field_tests = [
            ({}, "empty data"),
            ({"title": "Test"}, "missing code and language"),
            ({"code": "test"}, "missing title and language"),
            ({"language": "javascript"}, "missing title and code"),
            ({"title": "Test", "code": ""}, "empty code"),
            ({"title": "", "code": "test", "language": "js"}, "empty title"),
            ({"title": "Test", "code": "test", "language": ""}, "empty language"),
        ]
        
        for invalid_data, description in required_field_tests:
            response = requests.post(
                'http://localhost:8083/personal',
                json=invalid_data,
                headers=regular_headers
            )
            
            if response.status_code not in [400, 422]:
                print(f"  ❌ Expected 400/422 for {description}, got {response.status_code}")
                print(f"  📄 Response: {response.text}")
                return False
        
        print("  ✅ Personal snippet required fields validation working")
        
        # Step 3: Test personal snippet data type validation
        print("  📝 Step 3: Testing personal snippet data types...")
        
        type_validation_tests = [
            ({"title": 123, "code": "test", "language": "js"}, "non-string title"),
            ({"title": "Test", "code": 456, "language": "js"}, "non-string code"),
            ({"title": "Test", "code": "test", "language": 789}, "non-string language"),
            ({"title": "Test", "code": "test", "language": "js", "tags": "should_be_array"}, "non-array tags"),
            ({"title": "Test", "code": "test", "language": "js", "difficulty": 123}, "non-string difficulty"),
        ]
        
        for invalid_data, description in type_validation_tests:
            response = requests.post(
                'http://localhost:8083/personal',
                json=invalid_data,
                headers=regular_headers
            )
            
            if response.status_code not in [400, 422]:
                print(f"  ❌ Expected 400/422 for {description}, got {response.status_code}")
                return False
        
        print("  ✅ Personal snippet data type validation working")
        
        # Step 4: Test personal snippet value validation
        print("  📝 Step 4: Testing personal snippet value validation...")
        
        value_validation_tests = [
            ({"title": "Test", "code": "test", "language": "invalid_language"}, "invalid language"),
            ({"title": "Test", "code": "test", "language": "javascript", "difficulty": "invalid_difficulty"}, "invalid difficulty"),
        ]
        
        for invalid_data, description in value_validation_tests:
            response = requests.post(
                'http://localhost:8083/personal',
                json=invalid_data,
                headers=regular_headers
            )
            
            if response.status_code not in [400, 422]:
                print(f"  ❌ Expected 400/422 for {description}, got {response.status_code}")
                return False
        
        print("  ✅ Personal snippet value validation working")
        
        # Step 5: Test personal snippet valid data
        print("  📝 Step 5: Testing personal snippet valid data...")
        
        valid_personal_snippets = [
            {
                "title": "Valid Minimal Snippet",
                "code": "console.log('valid');",
                "language": "javascript"
            },
            {
                "title": "Valid Complete Snippet",
                "description": "A complete valid snippet",
                "code": "const valid = true;\nconsole.log(valid);",
                "language": "javascript",
                "tags": ["valid", "test", "complete"],
                "difficulty": "easy"
            },
            {
                "title": "Valid Python Snippet",
                "description": "Testing other languages",
                "code": "print('valid python')",
                "language": "python",
                "tags": ["python"],
                "difficulty": "medium"
            }
        ]
        
        created_personal_ids = []
        for valid_data in valid_personal_snippets:
            response = requests.post(
                'http://localhost:8083/personal',
                json=valid_data,
                headers=regular_headers
            )
            
            if response.status_code != 200:
                print(f"  ❌ Valid personal snippet should succeed: {response.status_code}")
                print(f"  📄 Data: {valid_data}")
                return False
            
            created_data = response.json()['data']
            created_personal_ids.append(created_data['_id'])
        
        print(f"  ✅ Valid personal snippets created successfully ({len(created_personal_ids)} snippets)")
        
        # Step 6: Test personal snippet update validation
        print("  📝 Step 6: Testing personal snippet update validation...")
        
        if created_personal_ids:
            snippet_id = created_personal_ids[0]
            
            update_validation_tests = [
                ({"title": ""}, "empty title in update"),
                ({"code": ""}, "empty code in update"),
                ({"language": ""}, "empty language in update"),
                ({"language": "invalid_lang"}, "invalid language in update"),
                ({"difficulty": "invalid_diff"}, "invalid difficulty in update"),
                ({"tags": "not_array"}, "invalid tags format in update"),
            ]
            
            for invalid_data, description in update_validation_tests:
                response = requests.put(
                    f'http://localhost:8083/personal/{snippet_id}',
                    json=invalid_data,
                    headers=regular_headers
                )
                
                if response.status_code not in [400, 422]:
                    print(f"  ❌ Expected 400/422 for {description}, got {response.status_code}")
                    return False
            
            # Test valid update
            valid_update = {
                "title": "Updated Valid Title",
                "description": "Updated description",
                "difficulty": "hard"
            }
            
            response = requests.put(
                f'http://localhost:8083/personal/{snippet_id}',
                json=valid_update,
                headers=regular_headers
            )
            
            if response.status_code != 200:
                print(f"  ❌ Valid update should succeed: {response.status_code}")
                return False
            
            print("  ✅ Personal snippet update validation working")
        else:
            print("  ⚠️ No personal snippets created for update testing")
        
        # Step 7: Test official snippet required fields validation
        print("  📝 Step 7: Testing official snippet required fields...")
        
        admin_headers = {
            'Authorization': f'Bearer {admin_token}',
            'Content-Type': 'application/json'
        }
        
        # Official snippets have additional required fields
        official_required_tests = [
            ({}, "empty data"),
            ({"title": "Test"}, "missing code, language, category"),
            ({"title": "Test", "code": "test"}, "missing language and category"),
            ({"title": "Test", "code": "test", "language": "js"}, "missing category"),
            ({"title": "", "code": "test", "language": "js", "category": "test"}, "empty title"),
            ({"title": "Test", "code": "", "language": "js", "category": "test"}, "empty code"),
            ({"title": "Test", "code": "test", "language": "", "category": "test"}, "empty language"),
            ({"title": "Test", "code": "test", "language": "js", "category": ""}, "empty category"),
        ]
        
        for invalid_data, description in official_required_tests:
            response = requests.post(
                'http://localhost:8083/official',
                json=invalid_data,
                headers=admin_headers
            )
            
            if response.status_code not in [400, 422]:
                print(f"  ❌ Expected 400/422 for official {description}, got {response.status_code}")
                return False
        
        print("  ✅ Official snippet required fields validation working")
        
        # Step 8: Test official snippet data type validation
        print("  📝 Step 8: Testing official snippet data types...")
        
        official_type_tests = [
            ({"title": 123, "code": "test", "language": "js", "category": "test"}, "non-string title"),
            ({"title": "Test", "code": 456, "language": "js", "category": "test"}, "non-string code"),
            ({"title": "Test", "code": "test", "language": 789, "category": "test"}, "non-string language"),
            ({"title": "Test", "code": "test", "language": "js", "category": 101}, "non-string category"),
            ({"title": "Test", "code": "test", "language": "js", "category": "test", "tags": "not_array"}, "non-array tags"),
            ({"title": "Test", "code": "test", "language": "js", "category": "test", "learningObjectives": "not_array"}, "non-array learning objectives"),
            ({"title": "Test", "code": "test", "language": "js", "category": "test", "estimatedTime": "not_number"}, "non-number estimated time"),
        ]
        
        for invalid_data, description in official_type_tests:
            response = requests.post(
                'http://localhost:8083/official',
                json=invalid_data,
                headers=admin_headers
            )
            
            if response.status_code not in [400, 422]:
                print(f"  ❌ Expected 400/422 for official {description}, got {response.status_code}")
                return False
        
        print("  ✅ Official snippet data type validation working")
        
        # Step 9: Test official snippet valid data
        print("  📝 Step 9: Testing official snippet valid data...")
        
        valid_official_snippets = [
            {
                "title": "Valid Minimal Official",
                "code": "console.log('official');",
                "language": "javascript",
                "category": "basics"
            },
            {
                "title": "Valid Complete Official",
                "description": "A complete official snippet",
                "code": "const official = true;\nconsole.log(official);",
                "language": "javascript",
                "category": "advanced",
                "tags": ["official", "complete"],
                "difficulty": "medium",
                "learningObjectives": ["Learn basics", "Understand concepts"],
                "hints": "Remember to use const",
                "solution": "Use const for immutable values",
                "estimatedTime": 15
            }
        ]
        
        created_official_ids = []
        for valid_data in valid_official_snippets:
            response = requests.post(
                'http://localhost:8083/official',
                json=valid_data,
                headers=admin_headers
            )
            
            if response.status_code != 200:
                print(f"  ❌ Valid official snippet should succeed: {response.status_code}")
                print(f"  📄 Data: {valid_data}")
                return False
            
            created_data = response.json()['data']
            created_official_ids.append(created_data['_id'])
        
        print(f"  ✅ Valid official snippets created successfully ({len(created_official_ids)} snippets)")
        
        # Step 10: Test edge cases and boundary values
        print("  📝 Step 10: Testing edge cases and boundary values...")
        
        # Test very long strings (should be handled gracefully)
        long_title = "A" * 1000
        long_code = "console.log('test');\n" * 100
        
        edge_case_snippet = {
            "title": long_title,
            "description": "Testing long content",
            "code": long_code,
            "language": "javascript"
        }
        
        response = requests.post(
            'http://localhost:8083/personal',
            json=edge_case_snippet,
            headers=regular_headers
        )
        
        # Should either succeed or fail gracefully with 400, not crash
        if response.status_code not in [200, 400, 422]:
            print(f"  ❌ Edge case should be handled gracefully: {response.status_code}")
            return False
        
        # Test special characters
        special_char_snippet = {
            "title": "Special Characters: éñ中文🎉",
            "description": "Testing unicode and special chars",
            "code": "// Comments with émojis 🚀\nconsole.log('héllo wörld');",
            "language": "javascript",
            "tags": ["unicode", "special-chars", "émojis"]
        }
        
        response = requests.post(
            'http://localhost:8083/personal',
            json=special_char_snippet,
            headers=regular_headers
        )
        
        if response.status_code != 200:
            print(f"  ❌ Special characters should be handled: {response.status_code}")
            return False
        
        # Test empty optional fields
        minimal_snippet = {
            "title": "Minimal with Empties",
            "description": "",  # Empty but provided
            "code": "console.log('minimal');",
            "language": "javascript",
            "tags": [],  # Empty array
            "difficulty": "easy"
        }
        
        response = requests.post(
            'http://localhost:8083/personal',
            json=minimal_snippet,
            headers=regular_headers
        )
        
        if response.status_code != 200:
            print(f"  ❌ Empty optional fields should be valid: {response.status_code}")
            return False
        
        print("  ✅ Edge cases and boundary values handled correctly")
        
        # Step 11: Test schema consistency between create and update
        print("  📝 Step 11: Testing schema consistency...")
        
        if created_personal_ids:
            snippet_id = created_personal_ids[0]
            
            # Test that update follows same validation rules as create
            consistency_tests = [
                ({"language": "invalid_lang"}, "invalid language consistency"),
                ({"difficulty": "invalid_diff"}, "invalid difficulty consistency"),
                ({"tags": "not_array"}, "invalid tags format consistency"),
            ]
            
            for invalid_data, description in consistency_tests:
                response = requests.put(
                    f'http://localhost:8083/personal/{snippet_id}',
                    json=invalid_data,
                    headers=regular_headers
                )
                
                if response.status_code not in [400, 422]:
                    print(f"  ❌ Update validation should match create for {description}: {response.status_code}")
                    return False
            
            print("  ✅ Schema consistency between create and update maintained")
        
        # Step 12: Test response format validation
        print("  📝 Step 12: Testing response format validation...")
        
        # Test that successful responses have consistent structure
        valid_snippet = {
            "title": "Response Format Test",
            "code": "console.log('format test');",
            "language": "javascript"
        }
        
        response = requests.post(
            'http://localhost:8083/personal',
            json=valid_snippet,
            headers=regular_headers
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Check response structure
            if not data.get('success'):
                print("  ❌ Successful response should have success: true")
                return False
            
            if not data.get('message'):
                print("  ❌ Response should include a message")
                return False
            
            snippet_data = data.get('data', {})
            required_response_fields = ['_id', 'title', 'code', 'language', 'userId', 'createdAt', 'updatedAt']
            
            for field in required_response_fields:
                if field not in snippet_data:
                    print(f"  ❌ Response missing required field: {field}")
                    return False
            
            print("  ✅ Response format validation correct")
        
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
    success = test_schema_validation()
    if success:
        print("🎉 Test passed!")
        exit(0)
    else:
        print("💥 Test failed!")
        exit(1)