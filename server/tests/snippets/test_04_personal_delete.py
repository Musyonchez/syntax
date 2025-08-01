#!/usr/bin/env python3
"""
Test 04: Personal Snippet Deletion
Tests the DELETE /personal/<id> endpoint for soft-deleting personal snippets with ownership verification
"""

import requests
import json
from datetime import datetime

def get_auth_token():
    """Helper function to get a valid auth token"""
    test_user_data = {
        "email": f"test_delete_snippets_{datetime.now().strftime('%Y%m%d_%H%M%S')}@example.com",
        "name": "Test Delete Snippets User",
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

def get_snippet_by_id(access_token, snippet_id):
    """Helper function to get a snippet by ID (via GET /personal)"""
    response = requests.get(
        'http://localhost:8083/personal',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    
    if response.status_code != 200:
        return None
    
    data = response.json()
    if not data.get('success'):
        return None
    
    snippets = data['data']['snippets']
    for snippet in snippets:
        if snippet['_id'] == snippet_id:
            return snippet
    
    return None

def test_personal_snippet_deletion():
    """Test deleting personal snippets with ownership verification and soft delete behavior"""
    print("🧪 Testing Personal Snippet Deletion...")
    
    try:
        # Step 1: Get authentication token
        print("  📝 Step 1: Getting authentication token...")
        access_token, user_id, user_email = get_auth_token()
        
        if not access_token:
            print("  ❌ Failed to get authentication token")
            return False
        
        print(f"  ✅ Got auth token for user: {user_email}")
        
        # Step 2: Create a test snippet to delete
        print("  📝 Step 2: Creating test snippet to delete...")
        
        test_snippet = {
            "title": "Test Snippet for Deletion",
            "description": "This snippet will be deleted for testing",
            "code": "const toDelete = () => {\n  console.log('This will be deleted');\n};",
            "language": "javascript",
            "tags": ["test", "deletion", "temporary"],
            "difficulty": "easy"
        }
        
        created_snippet = create_test_snippet(access_token, test_snippet)
        if not created_snippet:
            print("  ❌ Failed to create test snippet")
            return False
        
        snippet_id = created_snippet['_id']
        print(f"  ✅ Created test snippet with ID: {snippet_id}")
        
        # Step 3: Verify snippet exists and is active
        print("  📝 Step 3: Verifying snippet exists and is active...")
        
        retrieved_snippet = get_snippet_by_id(access_token, snippet_id)
        if not retrieved_snippet:
            print("  ❌ Could not find created snippet")
            return False
        
        if not retrieved_snippet.get('isActive', False):
            print("  ❌ Created snippet is not active")
            return False
        
        print("  ✅ Snippet exists and is active")
        
        # Step 4: Test successful deletion
        print("  📝 Step 4: Testing successful snippet deletion...")
        
        delete_response = requests.delete(
            f'http://localhost:8083/personal/{snippet_id}',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        
        print(f"  📡 Delete response status: {delete_response.status_code}")
        
        if delete_response.status_code != 200:
            print(f"  ❌ Expected 200, got {delete_response.status_code}")
            print(f"  📄 Response: {delete_response.text}")
            return False
        
        # Parse and validate response
        try:
            data = delete_response.json()
        except json.JSONDecodeError:
            print("  ❌ Invalid JSON response")
            return False
        
        if not data.get('success'):
            print(f"  ❌ Delete failed: {data.get('message', 'Unknown error')}")
            return False
        
        response_data = data.get('data', {})
        if not response_data.get('deleted'):
            print("  ❌ Response should indicate deletion success")
            return False
        
        print("  ✅ Snippet deletion successful")
        
        # Step 5: Verify soft delete (snippet no longer appears in GET requests)
        print("  📝 Step 5: Verifying soft delete behavior...")
        
        deleted_snippet = get_snippet_by_id(access_token, snippet_id)
        if deleted_snippet is not None:
            print("  ❌ Deleted snippet still appears in GET requests (soft delete failed)")
            return False
        
        print("  ✅ Soft delete working - snippet no longer appears in GET requests")
        
        # Step 6: Test deleting non-existent snippet
        print("  📝 Step 6: Testing deletion of non-existent snippet...")
        
        fake_id = "507f1f77bcf86cd799439011"  # Valid ObjectId format but doesn't exist
        nonexistent_response = requests.delete(
            f'http://localhost:8083/personal/{fake_id}',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        
        if nonexistent_response.status_code != 404:
            print(f"  ❌ Expected 404 for non-existent snippet, got {nonexistent_response.status_code}")
            return False
        
        print("  ✅ Non-existent snippet deletion properly rejected")
        
        # Step 7: Test deleting already deleted snippet
        print("  📝 Step 7: Testing deletion of already deleted snippet...")
        
        already_deleted_response = requests.delete(
            f'http://localhost:8083/personal/{snippet_id}',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        
        if already_deleted_response.status_code != 404:
            print(f"  ❌ Expected 404 for already deleted snippet, got {already_deleted_response.status_code}")
            return False
        
        print("  ✅ Already deleted snippet properly rejected")
        
        # Step 8: Test deleting with invalid snippet ID format
        print("  📝 Step 8: Testing with invalid snippet ID format...")
        
        invalid_id_response = requests.delete(
            'http://localhost:8083/personal/invalid_id_format',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        
        if invalid_id_response.status_code != 400:
            print(f"  ❌ Expected 400 for invalid ID format, got {invalid_id_response.status_code}")
            return False
        
        print("  ✅ Invalid snippet ID format properly rejected")
        
        # Step 9: Test ownership verification with different user
        print("  📝 Step 9: Testing ownership verification...")
        
        # Create another snippet first
        another_snippet = create_test_snippet(access_token, {
            "title": "Another Test Snippet",
            "description": "For ownership testing",
            "code": "console.log('ownership test');",
            "language": "javascript",
            "tags": ["ownership"],
            "difficulty": "easy"
        })
        
        if not another_snippet:
            print("  ⚠️ Could not create snippet for ownership test, skipping")
        else:
            another_snippet_id = another_snippet['_id']
            
            # Get a different user's token
            other_user_token, other_user_id, other_user_email = get_auth_token()
            if not other_user_token:
                print("  ⚠️ Could not create second user, skipping ownership test")
            else:
                ownership_response = requests.delete(
                    f'http://localhost:8083/personal/{another_snippet_id}',
                    headers={'Authorization': f'Bearer {other_user_token}'}
                )
                
                if ownership_response.status_code != 404:  # Should return 404 for access denied
                    print(f"  ❌ Expected 404 for ownership violation, got {ownership_response.status_code}")
                    return False
                
                print("  ✅ Ownership verification working")
        
        # Step 10: Test without authentication
        print("  📝 Step 10: Testing without authentication...")
        
        # Create one more snippet to test with
        final_snippet = create_test_snippet(access_token, {
            "title": "Final Test Snippet",
            "description": "For unauth test",
            "code": "console.log('unauth test');",
            "language": "javascript",
            "tags": ["unauth"],
            "difficulty": "easy"
        })
        
        if final_snippet:
            final_snippet_id = final_snippet['_id']
            
            unauth_response = requests.delete(
                f'http://localhost:8083/personal/{final_snippet_id}'
            )
            
            if unauth_response.status_code != 401:
                print(f"  ❌ Expected 401 for missing auth, got {unauth_response.status_code}")
                return False
            
            print("  ✅ Unauthenticated deletion properly rejected")
        else:
            print("  ⚠️ Could not create snippet for unauth test, skipping")
        
        # Step 11: Test with invalid auth token
        print("  📝 Step 11: Testing with invalid auth token...")
        
        if final_snippet:
            invalid_auth_response = requests.delete(
                f'http://localhost:8083/personal/{final_snippet_id}',
                headers={'Authorization': 'Bearer invalid.token.here'}
            )
            
            if invalid_auth_response.status_code != 401:
                print(f"  ❌ Expected 401 for invalid token, got {invalid_auth_response.status_code}")
                return False
            
            print("  ✅ Invalid token properly rejected")
        
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
    success = test_personal_snippet_deletion()
    if success:
        print("🎉 Test passed!")
        exit(0)
    else:
        print("💥 Test failed!")
        exit(1)