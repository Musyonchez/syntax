#!/usr/bin/env python3
"""
Test 06: Official Snippet Retrieval
Tests the GET /official endpoint for retrieving official snippets with filtering (public access)
"""

import requests
import json
from datetime import datetime

def get_admin_token():
    """Helper function to get an admin auth token for creating test data"""
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

def create_official_snippet(admin_token, snippet_data):
    """Helper function to create an official snippet"""
    response = requests.post(
        'http://localhost:8083/official',
        json=snippet_data,
        headers={
            'Authorization': f'Bearer {admin_token}',
            'Content-Type': 'application/json'
        }
    )
    
    if response.status_code != 200:
        return None
    
    data = response.json()
    if not data.get('success'):
        return None
    
    return data.get('data', {})

def test_official_snippet_retrieval():
    """Test retrieving official snippets with various filtering options (public access)"""
    print("🧪 Testing Official Snippet Retrieval...")
    
    try:
        # Step 1: Get admin token to create test data
        print("  📝 Step 1: Getting admin token to create test data...")
        admin_token, admin_id, admin_email = get_admin_token()
        
        if not admin_token:
            print("  ❌ Failed to get admin authentication token")
            return False
        
        print(f"  ✅ Got admin token for creating test data")
        
        # Step 2: Create diverse official snippets for testing filters
        print("  📝 Step 2: Creating diverse official snippets for testing...")
        
        test_snippets = [
            {
                "title": "JavaScript Array Methods",
                "description": "Learn essential array methods like map, filter, reduce",
                "code": "const arr = [1,2,3];\nconst doubled = arr.map(x => x * 2);\nconst evens = arr.filter(x => x % 2 === 0);",
                "language": "javascript",
                "category": "array-methods",
                "tags": ["javascript", "array", "functional", "map", "filter"],
                "difficulty": "easy"
            },
            {
                "title": "Python List Comprehensions",
                "description": "Master Python list comprehensions for data processing",
                "code": "numbers = [1, 2, 3, 4, 5]\nsquares = [x**2 for x in numbers if x % 2 == 0]\nprint(squares)  # [4, 16]",
                "language": "python",
                "category": "data-structures",
                "tags": ["python", "list", "comprehension", "filtering"],
                "difficulty": "medium"
            },
            {
                "title": "CSS Flexbox Layout",
                "description": "Create responsive layouts with CSS Flexbox",
                "code": ".container {\n  display: flex;\n  justify-content: center;\n  align-items: center;\n  gap: 1rem;\n}",
                "language": "css",
                "category": "layout",
                "tags": ["css", "flexbox", "layout", "responsive"],
                "difficulty": "medium"
            },
            {
                "title": "Advanced React Hooks",
                "description": "Complex state management with useReducer and useContext",
                "code": "const [state, dispatch] = useReducer(reducer, initialState);\nconst context = useContext(MyContext);\nreturn <Component state={state} dispatch={dispatch} />;",
                "language": "javascript",
                "category": "react-advanced",
                "tags": ["react", "hooks", "useReducer", "useContext", "advanced"],
                "difficulty": "hard"
            }
        ]
        
        created_snippets = []
        for snippet_data in test_snippets:
            snippet = create_official_snippet(admin_token, snippet_data)
            if snippet:
                created_snippets.append(snippet)
            else:
                print(f"  ⚠️ Failed to create official snippet: {snippet_data['title']}")
        
        if len(created_snippets) < 3:
            print(f"  ❌ Could only create {len(created_snippets)} official snippets, need at least 3")
            return False
        
        print(f"  ✅ Created {len(created_snippets)} official snippets")
        
        # Step 3: Test basic retrieval (no auth required, public access)
        print("  📝 Step 3: Testing basic retrieval (public access)...")
        
        response = requests.get('http://localhost:8083/official')
        
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
        
        print(f"  ✅ Retrieved {len(snippets)} official snippets (public access working)")
        
        # Step 4: Test filtering by language
        print("  📝 Step 4: Testing language filtering...")
        
        # Filter for JavaScript snippets
        js_response = requests.get('http://localhost:8083/official?language=javascript')
        
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
        medium_response = requests.get('http://localhost:8083/official?difficulty=medium')
        
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
        react_response = requests.get('http://localhost:8083/official?tag=react')
        
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
        
        # Search for "array" in title/description
        search_response = requests.get('http://localhost:8083/official?search=array')
        
        if search_response.status_code != 200:
            print(f"  ❌ Search failed: {search_response.status_code}")
            return False
        
        search_data = search_response.json()
        search_snippets = search_data['data']['snippets']
        
        # Verify search results contain the search term
        for snippet in search_snippets:
            title_lower = snippet['title'].lower()
            desc_lower = snippet['description'].lower()
            if 'array' not in title_lower and 'array' not in desc_lower:
                print(f"  ❌ Search result doesn't contain 'array': {snippet['title']}")
                return False
        
        print(f"  ✅ Search working: found {len(search_snippets)} snippets containing 'array'")
        
        # Step 8: Test combined filters
        print("  📝 Step 8: Testing combined filters...")
        
        # Filter for JavaScript + hard difficulty
        combined_response = requests.get('http://localhost:8083/official?language=javascript&difficulty=hard')
        
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
            if snippet['difficulty'] != 'hard':
                print(f"  ❌ Non-hard snippet in combined results")
                return False
        
        print(f"  ✅ Combined filters working: found {len(combined_snippets)} hard JavaScript snippets")
        
        # Step 9: Test empty results with non-matching filter
        print("  📝 Step 9: Testing non-matching filters...")
        
        empty_response = requests.get('http://localhost:8083/official?language=nonexistent')
        
        if empty_response.status_code != 200:
            print(f"  ❌ Non-matching filter should return 200: {empty_response.status_code}")
            return False
        
        empty_data = empty_response.json()
        empty_snippets = empty_data['data']['snippets']
        
        if len(empty_snippets) != 0:
            print(f"  ❌ Non-matching filter should return empty array, got {len(empty_snippets)}")
            return False
        
        print("  ✅ Non-matching filters return empty results correctly")
        
        # Step 10: Test public access (no authentication required)
        print("  📝 Step 10: Testing public access (no authentication required)...")
        
        # Make requests without any authentication headers - should work fine
        public_response = requests.get('http://localhost:8083/official?difficulty=easy')
        
        if public_response.status_code != 200:
            print(f"  ❌ Public access failed: {public_response.status_code}")
            return False
        
        public_data = public_response.json()
        if not public_data.get('success'):
            print("  ❌ Public access should work without authentication")
            return False
        
        public_snippets = public_data['data']['snippets']
        print(f"  ✅ Public access working: retrieved {len(public_snippets)} snippets without auth")
        
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
    success = test_official_snippet_retrieval()
    if success:
        print("🎉 Test passed!")
        exit(0)
    else:
        print("💥 Test failed!")
        exit(1)