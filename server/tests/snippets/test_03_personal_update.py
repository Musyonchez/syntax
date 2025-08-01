#!/usr/bin/env python3
"""
Test 03: Personal Snippet Update
Tests the PUT /personal/<id> endpoint for updating personal snippets with ownership verification
"""

import requests
import json
from datetime import datetime

def get_auth_token():
    """Helper function to get a valid auth token"""
    test_user_data = {
        "email": f"test_update_snippets_{datetime.now().strftime('%Y%m%d_%H%M%S')}@example.com",
        "name": "Test Update Snippets User",
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

def test_personal_snippet_update():
    """Test updating personal snippets with ownership verification"""
    print("🧪 Testing Personal Snippet Update...")
    
    try:
        # Step 1: Get authentication token
        print("  📝 Step 1: Getting authentication token...")
        access_token, user_id, user_email = get_auth_token()
        
        if not access_token:
            print("  ❌ Failed to get authentication token")
            return False
        
        print(f"  ✅ Got auth token for user: {user_email}")
        
        # Step 2: Create a test snippet to update
        print("  📝 Step 2: Creating test snippet to update...")
        
        original_snippet = {
            "title": "Original React Component",
            "description": "Original description for testing updates",
            "code": "const OriginalComponent = () => {\n  return <div>Original</div>;\n};",
            "language": "javascript",
            "tags": ["react", "original", "test"],
            "difficulty": "easy"
        }
        
        created_snippet = create_test_snippet(access_token, original_snippet)
        if not created_snippet:
            print("  ❌ Failed to create test snippet")
            return False
        
        snippet_id = created_snippet['_id']
        print(f"  ✅ Created test snippet with ID: {snippet_id}")
        
        # Step 3: Test basic update
        print("  📝 Step 3: Testing basic snippet update...")
        
        update_data = {
            "title": "Updated React Component",
            "description": "Updated description after modification",
            "code": "const UpdatedComponent = () => {\n  return <div>Updated Content</div>;\n};",
            "tags": ["react", "updated", "modified"],
            "difficulty": "medium"
        }
        
        update_response = requests.put(
            f'http://localhost:8083/personal/{snippet_id}',
            json=update_data,
            headers={
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
        )
        
        print(f"  📡 Update response status: {update_response.status_code}")
        
        if update_response.status_code != 200:
            print(f"  ❌ Expected 200, got {update_response.status_code}")
            print(f"  📄 Response: {update_response.text}")
            return False
        
        # Parse and validate response
        try:
            data = update_response.json()
        except json.JSONDecodeError:
            print("  ❌ Invalid JSON response")
            return False
        
        if not data.get('success'):
            print(f"  ❌ Update failed: {data.get('message', 'Unknown error')}")
            return False
        
        updated_snippet = data.get('data', {})
        
        # Validate updates were applied
        if updated_snippet['title'] != update_data['title']:
            print(f"  ❌ Title not updated: expected {update_data['title']}, got {updated_snippet['title']}")
            return False
        
        if updated_snippet['description'] != update_data['description']:
            print(f"  ❌ Description not updated")
            return False
        
        if updated_snippet['code'] != update_data['code']:
            print(f"  ❌ Code not updated")
            return False
        
        if updated_snippet['difficulty'] != update_data['difficulty']:
            print(f"  ❌ Difficulty not updated")
            return False
        
        # Validate unchanged fields
        if updated_snippet['userId'] != user_id:
            print(f"  ❌ User ID should not change")
            return False
        
        if updated_snippet['language'] != original_snippet['language']:
            print(f"  ❌ Language should remain unchanged when not provided in update")
            return False
        
        print("  ✅ Basic update successful")
        print(f"  📝 Updated title: {updated_snippet['title']}")
        print(f"  📝 Updated difficulty: {updated_snippet['difficulty']}")
        
        # Step 4: Test partial update
        print("  📝 Step 4: Testing partial update...")
        
        partial_update = {
            "description": "Partially updated description only"
        }
        
        partial_response = requests.put(
            f'http://localhost:8083/personal/{snippet_id}',
            json=partial_update,
            headers={
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
        )
        
        if partial_response.status_code != 200:
            print(f"  ❌ Partial update failed: {partial_response.status_code}")
            return False
        
        partial_data = partial_response.json()
        partial_snippet = partial_data['data']
        
        # Validate only description changed
        if partial_snippet['description'] != partial_update['description']:
            print("  ❌ Description not updated in partial update")
            return False
        
        if partial_snippet['title'] != update_data['title']:
            print("  ❌ Title changed unexpectedly in partial update")
            return False
        
        print("  ✅ Partial update working correctly")
        
        # Step 5: Test updating with invalid snippet ID
        print("  📝 Step 5: Testing with invalid snippet ID...")
        
        invalid_id_response = requests.put(
            'http://localhost:8083/personal/invalid_id_format',
            json={"title": "Should fail"},
            headers={
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
        )
        
        if invalid_id_response.status_code != 400:
            print(f"  ❌ Expected 400 for invalid ID format, got {invalid_id_response.status_code}")
            return False
        
        print("  ✅ Invalid snippet ID properly rejected")
        
        # Step 6: Test updating non-existent snippet
        print("  📝 Step 6: Testing with non-existent snippet ID...")
        
        fake_id = "507f1f77bcf86cd799439011"  # Valid ObjectId format but doesn't exist
        nonexistent_response = requests.put(
            f'http://localhost:8083/personal/{fake_id}',
            json={"title": "Should not work"},
            headers={
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
        )
        
        if nonexistent_response.status_code != 404:
            print(f"  ❌ Expected 404 for non-existent snippet, got {nonexistent_response.status_code}")
            return False
        
        print("  ✅ Non-existent snippet properly rejected")
        
        # Step 7: Test ownership verification with different user
        print("  📝 Step 7: Testing ownership verification...")
        
        # Get a different user's token
        other_user_token, other_user_id, other_user_email = get_auth_token()
        if not other_user_token:
            print("  ⚠️ Could not create second user, skipping ownership test")
        else:
            ownership_response = requests.put(
                f'http://localhost:8083/personal/{snippet_id}',
                json={"title": "Unauthorized access attempt"},
                headers={
                    'Authorization': f'Bearer {other_user_token}',
                    'Content-Type': 'application/json'
                }
            )
            
            if ownership_response.status_code != 404:  # Should return 404 for access denied
                print(f"  ❌ Expected 404 for ownership violation, got {ownership_response.status_code}")
                return False
            
            print("  ✅ Ownership verification working")
        
        # Step 8: Test without authentication
        print("  📝 Step 8: Testing without authentication...")
        
        unauth_response = requests.put(
            f'http://localhost:8083/personal/{snippet_id}',
            json={"title": "Should fail"},
            headers={'Content-Type': 'application/json'}
        )
        
        if unauth_response.status_code != 401:
            print(f"  ❌ Expected 401 for missing auth, got {unauth_response.status_code}")
            return False
        
        print("  ✅ Unauthenticated update properly rejected")
        
        # Step 9: Test with invalid auth token
        print("  📝 Step 9: Testing with invalid auth token...")
        
        invalid_auth_response = requests.put(
            f'http://localhost:8083/personal/{snippet_id}',
            json={"title": "Should fail"},
            headers={
                'Authorization': 'Bearer invalid.token.here',
                'Content-Type': 'application/json'
            }
        )
        
        if invalid_auth_response.status_code != 401:
            print(f"  ❌ Expected 401 for invalid token, got {invalid_auth_response.status_code}")
            return False
        
        print("  ✅ Invalid token properly rejected")
        
        # Step 10: Test with invalid update data
        print("  📝 Step 10: Testing with invalid update data...")
        
        invalid_updates = [
            ({"language": "invalid_language"}, "invalid language"),
            ({"difficulty": "invalid_difficulty"}, "invalid difficulty"),
            ({"tags": "should_be_array"}, "invalid tags format"),
            ({"title": ""}, "empty title"),
            ({"code": ""}, "empty code")
        ]
        
        for invalid_data, description in invalid_updates:
            invalid_response = requests.put(
                f'http://localhost:8083/personal/{snippet_id}',
                json=invalid_data,
                headers={
                    'Authorization': f'Bearer {access_token}',
                    'Content-Type': 'application/json'
                }
            )
            
            if invalid_response.status_code not in [400, 422]:
                print(f"  ❌ Expected 400/422 for {description}, got {invalid_response.status_code}")
                return False
        
        print("  ✅ Invalid update data properly rejected")
        
        # Step 11: Test updating tags and language
        print("  📝 Step 11: Testing tags and language updates...")
        
        advanced_update = {
            "language": "typescript",
            "tags": ["typescript", "react", "components", "advanced"],
            "code": "const AdvancedComponent: React.FC = () => {\n  return <div>TypeScript!</div>;\n};"
        }
        
        advanced_response = requests.put(
            f'http://localhost:8083/personal/{snippet_id}',
            json=advanced_update,
            headers={
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
        )
        
        if advanced_response.status_code != 200:
            print(f"  ❌ Advanced update failed: {advanced_response.status_code}")
            return False
        
        advanced_data = advanced_response.json()
        advanced_snippet = advanced_data['data']
        
        if advanced_snippet['language'] != advanced_update['language']:
            print("  ❌ Language not updated correctly")
            return False
        
        if len(advanced_snippet['tags']) != len(advanced_update['tags']):
            print("  ❌ Tags not updated correctly")
            return False
        
        print("  ✅ Advanced updates (language, tags, code) working")
        
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
    success = test_personal_snippet_update()
    if success:
        print("🎉 Test passed!")
        exit(0)
    else:
        print("💥 Test failed!")
        exit(1)