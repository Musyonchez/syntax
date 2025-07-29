# SyntaxMem Testing Suite

**Simple, Uniform, Consistent** modular testing for all server functionality.

## 🎯 New Structure

### **Modular Organization**
```
tests/
├── auth/                    # Authentication tests
│   ├── test_token_cleanup.py      # One test per file
│   ├── test_logout_all.py
│   ├── test_session_limits.py
│   └── run_auth_tests.sh          # Auth module runner
├── users/                   # User management tests (future)
│   ├── test_user_creation.py
│   ├── test_user_updates.py
│   └── run_users_tests.sh
├── snippets/                # Code snippets tests (future)
│   ├── test_snippet_crud.py
│   ├── test_masking_logic.py
│   └── run_snippets_tests.sh
├── sessions/                # Practice sessions tests (future)
│   └── run_sessions_tests.sh
└── run_all_tests.sh         # Master test runner
```

### **Benefits of New Structure**
- **Small, focused files** - One test per file, easy to understand
- **Modular execution** - Run individual tests or entire modules
- **Scalable organization** - Add new modules without complexity
- **Clear ownership** - Each module owns its tests
- **Independent failures** - One broken test doesn't break others

## 🚀 Running Tests

### **Individual Test**
```bash
cd tests/auth
python test_token_cleanup.py
```

### **Module Tests**
```bash
cd tests/auth
./run_auth_tests.sh
```

### **All Tests**
```bash
cd tests
./run_all_tests.sh
```

## 📋 Current Tests

### **Auth Module** (`auth/`) - **10 Comprehensive Tests**

**Core Auth Flow Tests:**
- `test_login_register.py` - Complete login/register flow validation
- `test_token_refresh.py` - Token refresh endpoint with edge cases  
- `test_schema_validation.py` - Input validation and data sanitization

**Session Management Tests:**
- `test_token_cleanup.py` - Automatic expired token cleanup
- `test_logout.py` - Single device logout with token cleanup
- `test_logout_all.py` - Logout all devices functionality
- `test_session_limits.py` - 2-token session limits enforcement

**Edge Case Tests:**
- `test_invalid_tokens.py` - Malformed/expired JWT token handling
- `test_concurrent_logins.py` - Race conditions and concurrent requests

**Security Tests:**
- `test_security.py` - Injection attacks, XSS, token manipulation

### **Future Modules**
- `users/` - User profile management, role changes
- `snippets/` - CRUD operations, masking algorithm
- `sessions/` - Practice session lifecycle, scoring

## 🔧 Test Patterns

### **File Naming**
- `test_feature_name.py` - Descriptive, specific names
- One test function per file: `test_feature_name()`
- Clear test purpose in docstring

### **Module Runner Pattern**
Each module has `run_module_tests.sh`:
```bash
#!/bin/bash
echo "🔐 Running Auth Tests"
python test_token_cleanup.py
python test_logout_all.py  
python test_session_limits.py
```

### **Test Function Pattern**
```python
async def test_feature_name():
    """Test specific feature functionality"""
    print("🧪 Testing Feature Name...")
    
    try:
        # Setup
        # Test logic
        # Assertions
        print("  ✅ Feature works correctly")
        return True
    except Exception as e:
        print(f"  ❌ Exception: {e}")
        return False
    finally:
        # Cleanup
```

## 🎯 Benefits Over Monolithic Approach

### **Before** (Single Large File)
- ❌ 500+ line test files
- ❌ All tests fail if one breaks
- ❌ Hard to debug specific issues
- ❌ Difficult to maintain

### **After** (Modular Structure)
- ✅ Small, focused test files (~50 lines each)
- ✅ Independent test execution
- ✅ Easy to debug and maintain
- ✅ Scales to hundreds of tests

---

**Remember**: Keep tests as simple as the features they test. One test, one file, one purpose. 🎯

*Good structure enables rapid development. Great structure enables rapid debugging.*