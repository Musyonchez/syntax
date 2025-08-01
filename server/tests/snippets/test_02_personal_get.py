#!/usr/bin/env python3
"""
Test 02: Personal Snippet Retrieval
Tests the GET /personal endpoint for retrieving personal snippets with filtering
"""

import requests
import json
from datetime import datetime

def get_auth_token():
    """Helper function to get a valid auth token"""
    test_user_data = {
        "email": f"test_get_snippets_{datetime.now().strftime('%Y%m%d_%H%M%S')}@example.com",
        "name": "Test Get Snippets User",
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

def create_test_snippet(access_token, snippet_data):
    """Helper function to create a test snippet"""
    response = requests.post(
        'http://localhost:8083/personal',
        json=snippet_data,
        headers={
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
    )
    
    if response.status_code != 200:
        return None
    
    data = response.json()
    if not data.get('success'):
        return None
    
    return data.get('data', {})

def test_personal_snippet_retrieval():
    """Test retrieving personal snippets with various filtering options"""
    print("🧪 Testing Personal Snippet Retrieval...")
    
    try:
        # Step 1: Get authentication token
        print("  📝 Step 1: Getting authentication token...")
        access_token, user_id, user_email = get_auth_token()
        
        if not access_token:
            print("  ❌ Failed to get authentication token")
            return False
        
        print(f"  ✅ Got auth token for user: {user_email}")
        
        # Step 2: Create test snippets for filtering
        print("  📝 Step 2: Creating test snippets...")
        
        test_snippets = [
            {
                "title": "React useState Hook",
                "description": "Basic useState example",
                "code": "const [count, setCount] = useState(0);",
                "language": "javascript",
                "tags": ["react", "hooks", "state"],
                "difficulty": "easy"
            },
            {
                "title": "Python List Comprehension",
                "description": "Filter and transform data",
                "code": "squares = [x**2 for x in range(10) if x % 2 == 0]",
                "language": "python",
                "tags": ["list", "comprehension", "functional"],
                "difficulty": "medium"
            },
            {
                "title": "CSS Grid Layout",
                "description": "Basic grid container setup",
                "code": ".container {\n  display: grid;\n  grid-template-columns: repeat(3, 1fr);\n}",
                "language": "css",
                "tags": ["grid", "layout", "responsive"],
                "difficulty": "medium"
            },
            {
                "title": "JavaScript Array Methods",
                "description": "Chaining array methods",
                "code": "const result = arr.filter(x => x > 5).map(x => x * 2).reduce((a, b) => a + b, 0);",
                "language": "javascript",
                "tags": ["array", "functional", "methods"],
                "difficulty": "hard"
            }
        ]
        
        created_snippets = []
        for snippet_data in test_snippets:
            snippet = create_test_snippet(access_token, snippet_data)
            if snippet:
                created_snippets.append(snippet)
            else:
                print(f"  ⚠️ Failed to create test snippet: {snippet_data['title']}")
        
        if len(created_snippets) < 3:
            print(f"  ❌ Could only create {len(created_snippets)} test snippets, need at least 3")
            return False
        
        print(f"  ✅ Created {len(created_snippets)} test snippets")
        
        # Step 3: Test basic retrieval (no filters)
        print("  📝 Step 3: Testing basic retrieval...")
        
        response = requests.get(
            'http://localhost:8083/personal',
            headers={'Authorization': f'Bearer {access_token}'}
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
        response_data = data.get('data', {})
        if 'snippets' not in response_data or 'count' not in response_data:
            print("  ❌ Missing required fields in response")
            return False
        
        snippets = response_data['snippets']
        snippet_count = response_data['count']
        
        if len(snippets) != snippet_count:
            print(f"  ❌ Count mismatch: array has {len(snippets)} items, count says {snippet_count}")
            return False
        
        if len(snippets) < len(created_snippets):
            print(f"  ❌ Retrieved fewer snippets ({len(snippets)}) than created ({len(created_snippets)})")
            return False
        
        print(f"  ✅ Retrieved {len(snippets)} personal snippets")
        
        # Step 4: Test filtering by language
        print("  📝 Step 4: Testing language filtering...")
        
        # Filter for JavaScript snippets
        js_response = requests.get(
            'http://localhost:8083/personal?language=javascript',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        
        if js_response.status_code != 200:
            print(f"  ❌ Language filter failed: {js_response.status_code}")
            return False
        
        js_data = js_response.json()
        js_snippets = js_data['data']['snippets']
        
        # Verify all returned snippets are JavaScript
        for snippet in js_snippets:
            if snippet['language'] != 'javascript':
                print(f"  ❌ Non-JavaScript snippet in filtered results: {snippet['language']}")
                return False
        
        print(f"  ✅ Language filter working: found {len(js_snippets)} JavaScript snippets")
        
        # Step 5: Test filtering by difficulty
        print("  📝 Step 5: Testing difficulty filtering...")
        
        # Filter for medium difficulty
        medium_response = requests.get(
            'http://localhost:8083/personal?difficulty=medium',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        
        if medium_response.status_code != 200:
            print(f"  ❌ Difficulty filter failed: {medium_response.status_code}")
            return False
        
        medium_data = medium_response.json()
        medium_snippets = medium_data['data']['snippets']
        
        # Verify all returned snippets are medium difficulty
        for snippet in medium_snippets:
            if snippet['difficulty'] != 'medium':
                print(f"  ❌ Non-medium snippet in filtered results: {snippet['difficulty']}")
                return False
        
        print(f"  ✅ Difficulty filter working: found {len(medium_snippets)} medium snippets")
        
        # Step 6: Test filtering by tag
        print("  📝 Step 6: Testing tag filtering...")
        
        # Filter for react tag
        react_response = requests.get(
            'http://localhost:8083/personal?tag=react',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        
        if react_response.status_code != 200:
            print(f"  ❌ Tag filter failed: {react_response.status_code}")
            return False
        
        react_data = react_response.json()
        react_snippets = react_data['data']['snippets']
        
        # Verify all returned snippets have the react tag
        for snippet in react_snippets:
            if 'react' not in [tag.lower() for tag in snippet.get('tags', [])]:
                print(f"  ❌ Snippet without 'react' tag in filtered results")
                return False
        
        print(f"  ✅ Tag filter working: found {len(react_snippets)} react snippets")
        
        # Step 7: Test search functionality
        print("  📝 Step 7: Testing search functionality...")
        
        # Search for "hook" in title/description
        search_response = requests.get(
            'http://localhost:8083/personal?search=hook',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        
        if search_response.status_code != 200:
            print(f"  ❌ Search failed: {search_response.status_code}")
            return False
        
        search_data = search_response.json()
        search_snippets = search_data['data']['snippets']
        
        # Verify search results contain the search term
        for snippet in search_snippets:
            title_lower = snippet['title'].lower()
            desc_lower = snippet['description'].lower()
            if 'hook' not in title_lower and 'hook' not in desc_lower:
                print(f"  ❌ Search result doesn't contain 'hook': {snippet['title']}")
                return False
        
        print(f"  ✅ Search working: found {len(search_snippets)} snippets containing 'hook'")
        
        # Step 8: Test combined filters
        print("  📝 Step 8: Testing combined filters...")
        
        # Filter for JavaScript + easy difficulty
        combined_response = requests.get(
            'http://localhost:8083/personal?language=javascript&difficulty=easy',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        
        if combined_response.status_code != 200:
            print(f"  ❌ Combined filter failed: {combined_response.status_code}")
            return False
        
        combined_data = combined_response.json()
        combined_snippets = combined_data['data']['snippets']
        
        # Verify all results match both criteria
        for snippet in combined_snippets:
            if snippet['language'] != 'javascript':
                print(f"  ❌ Non-JavaScript snippet in combined results")
                return False
            if snippet['difficulty'] != 'easy':
                print(f"  ❌ Non-easy snippet in combined results")
                return False
        
        print(f"  ✅ Combined filters working: found {len(combined_snippets)} easy JavaScript snippets")
        
        # Step 9: Test without authentication
        print("  📝 Step 9: Testing without authentication...")
        
        unauth_response = requests.get('http://localhost:8083/personal')
        
        if unauth_response.status_code != 401:
            print(f"  ❌ Expected 401 for missing auth, got {unauth_response.status_code}")
            return False
        
        print("  ✅ Unauthenticated request properly rejected")
        
        # Step 10: Test with invalid token
        print("  📝 Step 10: Testing with invalid token...")
        
        invalid_response = requests.get(
            'http://localhost:8083/personal',
            headers={'Authorization': 'Bearer invalid.token.here'}
        )
        
        if invalid_response.status_code != 401:
            print(f"  ❌ Expected 401 for invalid token, got {invalid_response.status_code}")
            return False
        
        print("  ✅ Invalid token properly rejected")
        
        # Step 11: Test empty results with non-matching filter
        print("  📝 Step 11: Testing non-matching filters...")
        
        empty_response = requests.get(
            'http://localhost:8083/personal?language=nonexistent',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        
        if empty_response.status_code != 200:
            print(f"  ❌ Non-matching filter should return 200: {empty_response.status_code}")
            return False
        
        empty_data = empty_response.json()
        empty_snippets = empty_data['data']['snippets']
        
        if len(empty_snippets) != 0:
            print(f"  ❌ Non-matching filter should return empty array, got {len(empty_snippets)}")
            return False
        
        print("  ✅ Non-matching filters return empty results correctly")
        
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
    success = test_personal_snippet_retrieval()
    if success:
        print("🎉 Test passed!")
        exit(0)
    else:
        print("💥 Test failed!")
        exit(1)