# Auth Service

**Simple, Uniform, Consistent** authentication service for SyntaxMem platform.

## 🎯 Purpose

The Auth service handles:
- **Google OAuth** - Secure sign-in with Google accounts
- **JWT tokens** - Access and refresh token management  
- **User management** - Profile creation and updates
- **Session control** - Multi-device session management

## 🚀 Endpoints

### Authentication
- `POST /login/google` - Google OAuth login flow
- `POST /refresh` - Refresh access token
- `POST /logout` - Logout from current session  
- `POST /logout-all` - Logout from all sessions

### User Management
- `GET /profile` - Get user profile (requires auth)
- `PUT /profile` - Update user profile (requires auth)

### Health Check
- `GET /health` - Service health status

## 🔑 Authentication Flow

### 1. Login Process
```
Client → POST /login/google with Google token
Server → Validates Google token
Server → Creates/updates user in database
Server → Returns JWT access + refresh tokens
```

### 2. Token Usage
```
Client → Includes "Bearer <access_token>" in Authorization header
Server → Validates token and extracts user info
Server → Processes request with authenticated user context
```

### 3. Token Refresh
```
Client → POST /refresh with refresh token
Server → Validates refresh token
Server → Issues new access token
Client → Uses new access token for requests
```

## 📋 Request/Response Format

### Success Response
```json
{
  "success": true,
  "message": "Operation successful",
  "data": { ... }
}
```

### Error Response
```json
{
  "success": false,
  "message": "Error description",
  "error": "Error details"
}
```

## 🚨 Service Rules

### The Sacred Laws (NEVER BREAK)

1. **JWT Security** - Always use secure JWT signing with HS256 algorithm
2. **Token Expiry** - Access tokens expire in 1 hour, refresh tokens in 30 days
3. **Input Validation** - All input must be validated using UserSchema
4. **Error Handling** - Never expose internal errors to clients
5. **CORS Configuration** - Only allow configured origins

### Authentication Rules

6. **Bearer Tokens** - All protected endpoints require "Bearer <token>" format
7. **Token Type Validation** - Verify token type matches endpoint requirement
8. **User Ownership** - Users can only access/modify their own data
9. **Session Limits** - Implement reasonable session limits per user
10. **Secure Logout** - Always invalidate refresh tokens on logout

### Database Rules

11. **Schema Validation** - Use UserSchema for all user data operations
12. **Soft Updates** - Only update fields that are provided and valid
13. **Timestamp Management** - Always update 'updatedAt' on modifications
14. **Error Recovery** - Handle database errors gracefully
15. **Connection Management** - Properly close database connections

## ⚠️ CRITICAL: Async/Sync Integration Pattern

**THE EVENT LOOP PROBLEM AND SOLUTION**

### 🚨 The Problem
Flask is synchronous but MongoDB operations are async. Mixing them incorrectly causes:
- **"Event loop is closed" errors**
- **Database connection failures**
- **Request timeouts and crashes**

### ✅ The Solution (MANDATORY PATTERN)
Every Flask route that needs database access MUST use this exact pattern:

```python
@app.route('/endpoint', methods=['POST'])
def sync_endpoint():
    """Sync Flask route"""
    try:
        # 1. Validate input synchronously
        data = request.get_json()
        # ... input validation ...
        
        # 2. Create new event loop for async operations
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            # 3. CRITICAL: Reset database connection
            db.client = None
            db.db = None
            
            # 4. Run async handler
            result = loop.run_until_complete(_handle_async_operation(data))
            return result
        except Exception as async_error:
            raise async_error
        finally:
            # 5. ALWAYS close the loop
            loop.close()
            
    except Exception as e:
        return create_error_response(f'Operation failed: {str(e)}', 500)

async def _handle_async_operation(data):
    """Separate async handler - ALL database ops go here"""
    try:
        # All async database operations
        collection = await db.get_users_collection()
        result = await collection.find_one(...)
        return create_response(result, 'Success')
    except Exception as e:
        return create_error_response(f'Database error: {str(e)}', 500)
```

### 🔴 NEVER DO THIS (BROKEN PATTERN)
```python
# ❌ This WILL cause "Event loop is closed" errors
@app.route('/endpoint')
def broken_endpoint():
    loop = asyncio.new_event_loop()
    # ... async operations inline ...
    # No db connection reset = FAILURE
```

### 🟢 Key Success Factors
1. **New event loop per request** - `asyncio.new_event_loop()`
2. **Database connection reset** - `db.client = None; db.db = None`
3. **Separate async handlers** - Keep Flask routes sync, handlers async
4. **Always close loop** - Use try/finally to ensure cleanup
5. **Proper error handling** - Catch and convert async errors

### 📊 This Pattern Powers
- ✅ All 10 auth tests passing
- ✅ Production-ready reliability  
- ✅ Zero "Event loop is closed" errors
- ✅ Clean separation of sync/async boundaries

## 🔧 Environment Variables

Required environment variables:
```bash
JWT_SECRET=your-secret-key-here
MONGODB_URI=mongodb://connection-string
DATABASE_NAME=syntaxmem
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
GOOGLE_CLIENT_ID=your-google-client-id
```

## 🧪 Testing

Run auth tests:
```bash
cd ../tests/auth
./run_auth_tests.sh
```

Test coverage includes:
- Google OAuth validation
- JWT token creation and verification
- User profile management
- Session management and logout
- Security edge cases

## 📊 Monitoring

Key metrics to monitor:
- **Login success rate** - Track authentication failures
- **Token refresh rate** - Monitor token usage patterns
- **Session duration** - Average user session length
- **Error rates** - Authentication and validation errors

## 🚫 What NOT to Do

### ⚠️ CRITICAL Async/Sync Don'ts
- ❌ **NEVER** mix async/sync without the proven pattern above
- ❌ **NEVER** skip database connection reset (`db.client = None; db.db = None`)
- ❌ **NEVER** reuse event loops across requests  
- ❌ **NEVER** do async operations directly in Flask routes
- ❌ **NEVER** forget to close event loops in finally blocks
- ❌ **BREAKING THESE RULES = "Event loop is closed" ERRORS**

### Forbidden Security Patterns
- ❌ Store passwords (Google OAuth only)
- ❌ Log sensitive data (tokens, personal info)
- ❌ Expose internal errors to clients
- ❌ Allow weak JWT secrets
- ❌ Skip token expiry validation

### Security Don'ts
- ❌ Use HTTP for token transmission
- ❌ Store tokens in localStorage (use httpOnly cookies when possible)
- ❌ Allow token reuse after logout
- ❌ Skip CORS validation
- ❌ Return user data without authentication

## ✅ Success Metrics

You know auth is working when:
- **Zero unauthorized access** to protected resources
- **Fast login/logout** - under 500ms response time
- **Secure token handling** - no token leakage in logs
- **Clean error messages** - helpful but not revealing
- **Reliable session management** - consistent across devices

---

**Remember**: Authentication is the foundation of security. Keep it simple, secure, and reliable. 🔐

*If users can't trust your auth, they can't trust your platform.*