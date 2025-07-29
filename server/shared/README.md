# SyntaxMem Shared Utilities

**Simple, Uniform, Consistent** utilities shared across all serverless functions.

## 🎯 Purpose

This directory contains production-ready utilities that all serverless functions use:
- **Authentication** ✅ JWT token creation, verification, and user management
- **Database** ✅ MongoDB connection with async Motor driver
- **Response formatting** ✅ Consistent API response structure
- **Security** ✅ Input sanitization and validation helpers

## 📁 Files Status

### `auth_utils.py` ✅ PRODUCTION READY
JWT token management for authentication flows.

**Key Functions:**
- `create_access_token(user)` - Generate 1-hour access tokens ✅
- `create_refresh_token(user_id)` - Generate 30-day refresh tokens ✅
- `verify_token(token, type)` - Validate and decode tokens ✅
- `sanitize_string(input)` - Clean user input strings ✅

**Features:**
- Configurable token expiry ✅
- Secure JWT signing with HS256 ✅
- Automatic token type validation ✅
- Input sanitization for security ✅

### `database.py` ✅ PRODUCTION READY
MongoDB connection and collection management.

**Key Features:**
- Async MongoDB client using Motor ✅
- Automatic connection management ✅
- Collection getter methods for users, refresh_tokens ✅
- Connection cleanup utilities ✅
- Event loop compatibility for serverless ✅

**Collections Supported:**
- `users` - User profiles and authentication data ✅
- `refresh_tokens` - Session management tokens ✅
- Ready for future: `snippets`, `sessions` ✅

### `response_utils.py` ✅ PRODUCTION READY
Standardized API response formatting.

**Response Format:**
```python
{
    "success": true,
    "message": "Operation successful", 
    "data": { ... }
}
```

**Functions:**
- `create_response(data, message)` - Success responses ✅
- `create_error_response(message, status_code)` - Error responses ✅

## 🚨 Usage Rules

### The Sacred Laws (NEVER BREAK)
1. **Import Pattern** - Always use `sys.path.append('../shared')` ✅
2. **No Business Logic** - Utilities only, no feature-specific code ✅
3. **Consistent Patterns** - Same function signatures across all utilities ✅
4. **Error Handling** - Always return meaningful error responses ✅
5. **Stateless Functions** - No global state, no side effects ✅

### Import Example
```python
# In any serverless function
import sys
sys.path.append('../shared')
from auth_utils import AuthUtils
from database import db
from response_utils import create_response, create_error_response
```

## ✅ Production Features

**Security:**
- JWT tokens with configurable expiry ✅
- Input sanitization prevents injection attacks ✅
- Secure token generation ✅
- Proper error handling without information leakage ✅

**Performance:**
- Async database operations ✅
- Connection pooling and reuse ✅
- Minimal memory footprint ✅
- Fast token operations ✅

**Reliability:**
- Comprehensive error handling ✅
- Automated testing coverage ✅
- Event loop compatibility ✅
- Graceful failure modes ✅

## 🧪 Testing Coverage

All shared utilities have automated tests:
- **Authentication tests** - Token creation, verification, edge cases ✅
- **Database tests** - Connection, collection access, cleanup ✅
- **Response tests** - Format validation, error handling ✅

**Test Location:** `../tests/auth/` (integrated with feature tests)

## 🎯 Current Status

**Completed Utilities:** ✅ PRODUCTION READY
- Authentication (JWT tokens, validation, security) ✅
- Database (MongoDB connection, collections, async operations) ✅
- Response formatting (consistent API responses) ✅

**Future Utilities:** 🚧 PLANNED
- Extended validation helpers
- Email/notification utilities
- File upload/storage helpers
- Logging and monitoring utils

---

**Remember**: Shared utilities should be boring and predictable. If it's exciting or clever, it probably doesn't belong here. 🎯

*Simple utilities enable complex features. Complex utilities create simple bugs.*