#!/usr/bin/env python3
"""
Test 06: Session Schema Validation
Unit test for SessionSchema validation to ensure it's as strict as other schemas
Since session endpoints aren't implemented yet, we test the schema directly
"""

import sys
sys.path.append('../../schemas')
from sessions import SessionSchema

def test_session_schema_validation():
    """Test that SessionSchema properly validates types and throws errors"""
    print("Testing SessionSchema validation...")
    
    # Test 1: Valid session data should work
    try:
        valid_data = {
            'userId': 'user123',
            'snippetId': 'snippet456',
            'duration': 120.5,
            'score': 85,
            'completed': True
        }
        result = SessionSchema.validate_create(valid_data)
        print("✅ Valid session data accepted")
    except Exception as e:
        print(f"❌ Valid session data should work: {e}")
        return False
    
    # Test 2: Type validation for required fields
    type_tests = [
        ({'userId': 123, 'snippetId': 'snippet456'}, "non-string userId"),
        ({'userId': 'user123', 'snippetId': 456}, "non-string snippetId"),
        ({'userId': 'user123', 'snippetId': 'snippet456', 'duration': 'not_number'}, "non-number duration"),
        ({'userId': 'user123', 'snippetId': 'snippet456', 'score': 'not_number'}, "non-number score"),
        ({'userId': 'user123', 'snippetId': 'snippet456', 'completed': 'not_boolean'}, "non-boolean completed"),
    ]
    
    for invalid_data, description in type_tests:
        try:
            SessionSchema.validate_create(invalid_data)
            print(f"❌ FAILED: Should have rejected {description}")
            return False
        except ValueError as e:
            print(f"✅ Correctly rejected {description}: {e}")
        except Exception as e:
            print(f"❌ Unexpected error for {description}: {e}")
            return False
    
    # Test 3: Value validation
    value_tests = [
        ({'userId': 'user123', 'snippetId': 'snippet456', 'duration': -5}, "negative duration"),
        ({'userId': 'user123', 'snippetId': 'snippet456', 'score': -10}, "negative score"),
    ]
    
    for invalid_data, description in value_tests:
        try:
            SessionSchema.validate_create(invalid_data)
            print(f"❌ FAILED: Should have rejected {description}")
            return False
        except ValueError as e:
            print(f"✅ Correctly rejected {description}: {e}")
        except Exception as e:
            print(f"❌ Unexpected error for {description}: {e}")
            return False
    
    # Test 4: Required field validation
    required_tests = [
        ({'snippetId': 'snippet456'}, "missing userId"),
        ({'userId': 'user123'}, "missing snippetId"),
        ({'userId': '', 'snippetId': 'snippet456'}, "empty userId"),
        ({'userId': 'user123', 'snippetId': ''}, "empty snippetId"),
    ]
    
    for invalid_data, description in required_tests:
        try:
            SessionSchema.validate_create(invalid_data)
            print(f"❌ FAILED: Should have rejected {description}")
            return False
        except ValueError as e:
            print(f"✅ Correctly rejected {description}: {e}")
        except Exception as e:
            print(f"❌ Unexpected error for {description}: {e}")
            return False
    
    return True

if __name__ == '__main__':
    success = test_session_schema_validation()
    if success:
        print("\n🎉 SessionSchema validation tests passed!")
        print("📝 SessionSchema is now as strict as other schemas")
        exit(0)
    else:
        print("\n💥 SessionSchema validation tests failed!")
        exit(1)