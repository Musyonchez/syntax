#!/usr/bin/env python3
"""
Test 05: Admin Create Official Snippets
Tests the POST /official endpoint for creating official snippets with admin authentication
"""

import requests
import json
from datetime import datetime

def get_admin_token():
    """Helper function to get an admin auth token"""
    # Use the configured admin email to get admin role
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
    
    # Verify we got admin role
    if auth_data['data']['user']['role'] != 'admin':
        return None, None, None
    
    return (
        auth_data['data']['token'],
        auth_data['data']['user']['id'],
        auth_data['data']['user']['email']
    )

def get_regular_token():
    """Helper function to get a regular user auth token"""
    test_user_data = {
        "email": f"test_regular_user_{datetime.now().strftime('%Y%m%d_%H%M%S')}@example.com",
        "name": "Regular Test User",
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

def test_admin_create_official_snippets():
    """Test creating official snippets with admin authentication and validation"""
    print("🧪 Testing Admin Create Official Snippets...")
    
    try:
        # Step 1: Get admin authentication token
        print("  📝 Step 1: Getting admin authentication token...")
        admin_token, admin_id, admin_email = get_admin_token()
        
        if not admin_token:
            print("  ❌ Failed to get admin authentication token")
            return False
        
        print(f"  ✅ Got admin token for: {admin_email}")
        
        # Step 2: Test successful official snippet creation
        print("  📝 Step 2: Testing successful official snippet creation...")
        
        official_snippet = {
            "title": "Array Map Method - Official Tutorial",
            "description": "Learn how to transform arrays using the map method",
            "code": "const numbers = [1, 2, 3, 4, 5];\nconst doubled = numbers.map(x => x * 2);\nconsole.log(doubled); // [2, 4, 6, 8, 10]",
            "language": "javascript",
            "category": "array-methods",
            "tags": ["array", "map", "transformation", "functional"],
            "difficulty": "medium",
            "learningObjectives": ["Understand array.map()", "Transform data", "Functional programming"],
            "hints": "Remember that map returns a new array without modifying the original",
            "solution": "Use x => x * 2 to double each element",
            "estimatedTime": 15
        }
        
        create_response = requests.post(
            'http://localhost:8083/official',
            json=official_snippet,
            headers={
                'Authorization': f'Bearer {admin_token}',
                'Content-Type': 'application/json'
            }
        )
        
        print(f"  📡 Create response status: {create_response.status_code}")
        
        if create_response.status_code != 200:
            print(f"  ❌ Expected 200, got {create_response.status_code}")
            print(f"  📄 Response: {create_response.text}")
            return False
        
        # Parse and validate response
        try:
            data = create_response.json()
        except json.JSONDecodeError:
            print("  ❌ Invalid JSON response")
            return False
        
        if not data.get('success'):
            print(f"  ❌ Creation failed: {data.get('message', 'Unknown error')}")
            return False
        
        created_snippet = data.get('data', {})
        
        # Validate created snippet structure
        required_fields = ['_id', 'title', 'description', 'code', 'language', 'category', 'createdBy']
        for field in required_fields:
            if field not in created_snippet:
                print(f"  ❌ Missing required field: {field}")
                return False
        
        if created_snippet['createdBy'] != admin_id:
            print(f"  ❌ Creator ID mismatch: expected {admin_id}, got {created_snippet['createdBy']}")
            return False
        
        snippet_id = created_snippet['_id']
        print(f"  ✅ Official snippet created successfully with ID: {snippet_id}")
        
        # Step 3: Test validation errors
        print("  📝 Step 3: Testing validation errors...")
        
        invalid_snippets = [
            ({}, "empty data"),
            ({"title": "Missing required fields"}, "missing code"),
            ({"title": "", "code": "test", "language": "js", "category": "test"}, "empty title"),
            ({"title": "Test", "code": "", "language": "js", "category": "test"}, "empty code"),
            ({"title": "Test", "code": "test", "language": "", "category": "test"}, "empty language"),
            ({"title": "Test", "code": "test", "language": "js", "category": ""}, "empty category"),
        ]
        
        for invalid_data, description in invalid_snippets:
            invalid_response = requests.post(
                'http://localhost:8083/official',
                json=invalid_data,
                headers={
                    'Authorization': f'Bearer {admin_token}',
                    'Content-Type': 'application/json'
                }
            )
            
            if invalid_response.status_code != 400:
                print(f"  ❌ Expected 400 for {description}, got {invalid_response.status_code}")
                return False
        
        print("  ✅ Validation errors properly handled")
        
        # Step 4: Test permission denied for regular users
        print("  📝 Step 4: Testing permission denied for regular users...")
        
        regular_token, regular_id, regular_email = get_regular_token()
        if not regular_token:
            print("  ⚠️ Could not create regular user, skipping permission test")
        else:
            permission_response = requests.post(
                'http://localhost:8083/official',
                json={
                    "title": "Unauthorized Attempt",
                    "description": "This should fail",
                    "code": "console.log('unauthorized');",
                    "language": "javascript",
                    "category": "test"
                },
                headers={
                    'Authorization': f'Bearer {regular_token}',
                    'Content-Type': 'application/json'
                }
            )
            
            if permission_response.status_code != 403:
                print(f"  ❌ Expected 403 for regular user, got {permission_response.status_code}")
                return False
            
            print(f"  ✅ Regular user properly denied access")
        
        # Step 5: Test without authentication
        print("  📝 Step 5: Testing without authentication...")
        
        unauth_response = requests.post(
            'http://localhost:8083/official',
            json={
                "title": "No Auth Test",
                "description": "Should fail",
                "code": "console.log('no auth');",
                "language": "javascript",
                "category": "test"
            },
            headers={'Content-Type': 'application/json'}
        )
        
        if unauth_response.status_code != 401:
            print(f"  ❌ Expected 401 for missing auth, got {unauth_response.status_code}")
            return False
        
        print("  ✅ Unauthenticated request properly rejected")
        
        # Step 6: Test with invalid auth token
        print("  📝 Step 6: Testing with invalid auth token...")
        
        invalid_auth_response = requests.post(
            'http://localhost:8083/official',
            json={
                "title": "Invalid Token Test",
                "description": "Should fail",
                "code": "console.log('invalid token');",
                "language": "javascript",
                "category": "test"
            },
            headers={
                'Authorization': 'Bearer invalid.token.here',
                'Content-Type': 'application/json'
            }
        )
        
        if invalid_auth_response.status_code != 401:
            print(f"  ❌ Expected 401 for invalid token, got {invalid_auth_response.status_code}")
            return False
        
        print("  ✅ Invalid token properly rejected")
        
        # Step 7: Test optional fields handling
        print("  📝 Step 7: Testing optional fields handling...")
        
        minimal_snippet = {
            "title": "Minimal Official Snippet",
            "description": "Testing with minimal required fields",
            "code": "console.log('minimal');",
            "language": "javascript",
            "category": "basics"
        }
        
        minimal_response = requests.post(
            'http://localhost:8083/official',
            json=minimal_snippet,
            headers={
                'Authorization': f'Bearer {admin_token}',
                'Content-Type': 'application/json'
            }
        )
        
        if minimal_response.status_code != 200:
            print(f"  ❌ Minimal snippet creation failed: {minimal_response.status_code}")
            return False
        
        minimal_data = minimal_response.json()
        minimal_created = minimal_data['data']
        
        # Check default values are applied
        if minimal_created.get('difficulty') != 'medium':
            print(f"  ❌ Default difficulty not applied: got {minimal_created.get('difficulty')}")
            return False
        
        if not isinstance(minimal_created.get('tags'), list):
            print("  ❌ Tags should default to empty list")
            return False
        
        print("  ✅ Optional fields and defaults working correctly")
        
        # Step 8: Test comprehensive snippet with all fields
        print("  📝 Step 8: Testing comprehensive snippet with all fields...")
        
        comprehensive_snippet = {
            "title": "Comprehensive React Hook Example",
            "description": "Complete example demonstrating useState and useEffect",
            "code": "import React, { useState, useEffect } from 'react';\n\nfunction Counter() {\n  const [count, setCount] = useState(0);\n  \n  useEffect(() => {\n    document.title = `Count: ${count}`;\n  }, [count]);\n  \n  return (\n    <div>\n      <p>Count: {count}</p>\n      <button onClick={() => setCount(count + 1)}>+</button>\n    </div>\n  );\n}",
            "language": "javascript",
            "category": "react-hooks",
            "tags": ["react", "hooks", "useState", "useEffect", "components"],
            "difficulty": "hard",
            "learningObjectives": [
                "Understand useState hook",
                "Learn useEffect for side effects",
                "Practice component state management"
            ],
            "hints": "Remember that useEffect runs after every render by default",
            "solution": "Use dependency array [count] to optimize useEffect",
            "estimatedTime": 30
        }
        
        comp_response = requests.post(
            'http://localhost:8083/official',
            json=comprehensive_snippet,
            headers={
                'Authorization': f'Bearer {admin_token}',
                'Content-Type': 'application/json'
            }
        )
        
        if comp_response.status_code != 200:
            print(f"  ❌ Comprehensive snippet creation failed: {comp_response.status_code}")
            return False
        
        comp_data = comp_response.json()
        comp_created = comp_data['data']
        
        # Validate all fields are preserved
        if comp_created['difficulty'] != 'hard':
            print(f"  ❌ Difficulty not preserved: expected 'hard', got {comp_created['difficulty']}")
            return False
        
        if len(comp_created['tags']) != 5:
            print(f"  ❌ Tags not preserved: expected 5, got {len(comp_created['tags'])}")
            return False
        
        if comp_created['estimatedTime'] != 30:
            print(f"  ❌ Estimated time not preserved: expected 30, got {comp_created['estimatedTime']}")
            return False
        
        print("  ✅ Comprehensive snippet with all fields working correctly")
        
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
    success = test_admin_create_official_snippets()
    if success:
        print("🎉 Test passed!")
        exit(0)
    else:
        print("💥 Test failed!")
        exit(1)