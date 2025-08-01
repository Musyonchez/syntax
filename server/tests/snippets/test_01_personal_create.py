#!/usr/bin/env python3
"""
Test 01: Personal Snippet Creation
Tests the POST /personal endpoint for creating personal snippets
"""

import requests
import json
from datetime import datetime

def get_auth_token():
    """Helper function to get a valid auth token"""
    test_user_data = {
        "email": f"test_snippets_{datetime.now().strftime('%Y%m%d_%H%M%S')}@example.com",
        "name": "Test Snippets User",
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

def test_personal_snippet_creation():
    """Test creating personal snippets with various scenarios"""
    print("🧪 Testing Personal Snippet Creation...")
    
    try:
        # Step 1: Get authentication token
        print("  📝 Step 1: Getting authentication token...")
        access_token, user_id, user_email = get_auth_token()
        
        if not access_token:
            print("  ❌ Failed to get authentication token")
            return False
        
        print(f"  ✅ Got auth token for user: {user_email}")
        
        # Step 2: Create a basic personal snippet
        print("  📝 Step 2: Creating basic personal snippet...")
        
        snippet_data = {
            "title": "Test React Component",
            "description": "A simple React functional component for testing",
            "code": "const TestComponent = () => {\n  return <div>Hello World</div>;\n};",
            "language": "javascript",
            "tags": ["react", "component", "test"],
            "difficulty": "easy"
        }
        
        response = requests.post(
            'http://localhost:8083/personal',
            json=snippet_data,
            headers={
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
        )
        
        print(f"  📡 Response status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"  ❌ Expected 200, got {response.status_code}")
            print(f"  📄 Response: {response.text}")
            return False
        
        # Parse and validate response
        try:
            data = response.json()
        except json.JSONDecodeError:
            print("  ❌ Invalid JSON response")
            return False
        
        if not data.get('success'):
            print(f"  ❌ Request failed: {data.get('message', 'Unknown error')}")
            return False
        
        # Validate response structure
        snippet = data.get('data', {})
        required_fields = ['_id', 'userId', 'title', 'description', 'code', 'language', 'tags', 'difficulty', 'createdAt', 'updatedAt']
        
        for field in required_fields:
            if field not in snippet:
                print(f"  ❌ Missing required field: {field}")
                return False
        
        # Validate data matches input
        if snippet['title'] != snippet_data['title']:
            print(f"  ❌ Title mismatch: expected {snippet_data['title']}, got {snippet['title']}")
            return False
        
        if snippet['code'] != snippet_data['code']:
            print(f"  ❌ Code mismatch")
            return False
        
        if snippet['language'] != snippet_data['language']:
            print(f"  ❌ Language mismatch: expected {snippet_data['language']}, got {snippet['language']}")
            return False
        
        if snippet['userId'] != user_id:
            print(f"  ❌ User ID mismatch: expected {user_id}, got {snippet['userId']}")
            return False
        
        # Validate default values
        if 'isActive' not in snippet or snippet['isActive'] != True:
            print(f"  ❌ isActive should default to True")
            return False
        
        if 'isPrivate' not in snippet or snippet['isPrivate'] != True:
            print(f"  ❌ isPrivate should default to True")
            return False
        
        print("  ✅ Basic personal snippet created successfully")
        print(f"  📝 Snippet ID: {snippet['_id']}")
        print(f"  📝 Title: {snippet['title']}")
        print(f"  📝 Language: {snippet['language']}")
        
        # Step 3: Test creating snippet without authentication
        print("  📝 Step 3: Testing without authentication...")
        
        unauth_response = requests.post(
            'http://localhost:8083/personal',
            json=snippet_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if unauth_response.status_code != 401:
            print(f"  ❌ Expected 401 for missing auth, got {unauth_response.status_code}")
            return False
        
        print("  ✅ Unauthenticated request properly rejected")
        
        # Step 4: Test creating snippet with invalid auth token
        print("  📝 Step 4: Testing with invalid auth token...")
        
        invalid_auth_response = requests.post(
            'http://localhost:8083/personal',
            json=snippet_data,
            headers={
                'Authorization': 'Bearer invalid.token.here',
                'Content-Type': 'application/json'
            }
        )
        
        if invalid_auth_response.status_code != 401:
            print(f"  ❌ Expected 401 for invalid token, got {invalid_auth_response.status_code}")
            return False
        
        print("  ✅ Invalid token properly rejected")
        
        # Step 5: Test creating snippet with missing required fields
        print("  📝 Step 5: Testing with missing required fields...")
        
        invalid_data_tests = [
            ({}, "empty data"),
            ({"title": "Test"}, "missing code and language"),
            ({"title": "Test", "code": "console.log('test')"}, "missing language"),
            ({"code": "console.log('test')", "language": "javascript"}, "missing title"),
            # Invalid data types
            ({"title": 123, "code": "print(1)", "language": "python"}, "title is int"),
            ({"title": ["array"], "code": "print(1)", "language": "python"}, "title is list"),
            ({"title": "Test", "code": None, "language": "python"}, "code is None"),
            ({"title": "Test", "code": 12345, "language": "python"}, "code is int"),
            ({"title": "Test", "code": "print(1)", "language": None}, "language is None"),
            ({"title": "Test", "code": "print(1)", "language": 123}, "language is int"),
            ({"title": "Test", "code": "print(1)", "language": "python", "tags": "notalist"}, "tags is string"),
            ({"title": "Test", "code": "print(1)", "language": "python", "tags": 123}, "tags is int"),
            ({"title": "Test", "code": "print(1)", "language": "python", "tags": {"not": "alist"}}, "tags is dict"),
        ]
        
        for invalid_data, description in invalid_data_tests:
            invalid_response = requests.post(
                'http://localhost:8083/personal',
                json=invalid_data,
                headers={
                    'Authorization': f'Bearer {access_token}',
                    'Content-Type': 'application/json'
                }
            )
            
            if invalid_response.status_code != 400:
                print(f"  ❌ Expected 400 for {description}, got {invalid_response.status_code}")
                return False
        
        print("  ✅ Missing required fields and invalid data types properly rejected")
        
        # Step 6: Test creating snippet with different languages and difficulties
        print("  📝 Step 6: Testing different languages and difficulties...")
        
        test_variations = [
            {
                "title": "Python Function",
                "description": "A simple Python function",
                "code": "def hello_world():\n    print('Hello, World!')",
                "language": "python",
                "difficulty": "medium"
            },
            {
                "title": "CSS Animation",
                "description": "Basic CSS keyframe animation",
                "code": "@keyframes fadeIn {\n  from { opacity: 0; }\n  to { opacity: 1; }\n}",
                "language": "css",
                "difficulty": "hard"
            }
        ]
        
        for variation in test_variations:
            var_response = requests.post(
                'http://localhost:8083/personal',
                json=variation,
                headers={
                    'Authorization': f'Bearer {access_token}',
                    'Content-Type': 'application/json'
                }
            )
            
            if var_response.status_code != 200:
                print(f"  ❌ Failed to create {variation['language']} snippet: {var_response.status_code}")
                return False
        
        print("  ✅ Different languages and difficulties working")
        
        # Step 7: Test with long content (no cleanup - development database)
        print("  📝 Step 7: Testing with longer content...")
        
        long_snippet = {
            "title": "Complex React Component with Hooks",
            "description": "A comprehensive React component demonstrating various hooks and patterns",
            "code": """import React, { useState, useEffect, useMemo, useCallback } from 'react';

const ComplexComponent = ({ data, onUpdate }) => {
  const [loading, setLoading] = useState(false);
  const [items, setItems] = useState([]);
  const [filter, setFilter] = useState('');

  useEffect(() => {
    setLoading(true);
    // Simulate API call
    setTimeout(() => {
      setItems(data || []);
      setLoading(false);
    }, 1000);
  }, [data]);

  const filteredItems = useMemo(() => {
    return items.filter(item => 
      item.name.toLowerCase().includes(filter.toLowerCase())
    );
  }, [items, filter]);

  const handleUpdate = useCallback((id, updates) => {
    setItems(prev => prev.map(item => 
      item.id === id ? { ...item, ...updates } : item
    ));
    onUpdate && onUpdate(id, updates);
  }, [onUpdate]);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="complex-component">
      <input
        type="text"
        placeholder="Filter items..."
        value={filter}
        onChange={(e) => setFilter(e.target.value)}
      />
      <ul>
        {filteredItems.map(item => (
          <li key={item.id}>
            {item.name}
            <button onClick={() => handleUpdate(item.id, { viewed: true })}>
              Mark Viewed
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ComplexComponent;""",
            "language": "javascript",
            "tags": ["react", "hooks", "complex", "component"],
            "difficulty": "hard"
        }
        
        long_response = requests.post(
            'http://localhost:8083/personal',
            json=long_snippet,
            headers={
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
        )
        
        if long_response.status_code != 200:
            print(f"  ❌ Failed to create long snippet: {long_response.status_code}")
            return False
        
        print("  ✅ Long content snippet created successfully")
        
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
    success = test_personal_snippet_creation()
    if success:
        print("🎉 Test passed!")
        exit(0)
    else:
        print("💥 Test failed!")
        exit(1)