# SyntaxMem - Authentication Flow Documentation

**Simple, Uniform, Consistent** authentication flows for all user operations.

## 🔐 Login Flow (Existing User)

### Step-by-Step Process

```mermaid
sequenceDiagram
    participant User
    participant Client
    participant NextAuth
    participant Backend
    participant MongoDB

    User->>Client: Click "Sign in with Google"
    Client->>NextAuth: signIn("google")
    NextAuth->>Google: OAuth redirect
    Google->>NextAuth: OAuth callback with user data
    NextAuth->>Backend: POST /google-auth (googleId, email, name, avatar)
    Backend->>MongoDB: Find user by googleId
    MongoDB->>Backend: Return existing user
    Backend->>Backend: Update lastLoginAt, name, avatar
    Backend->>MongoDB: Store updated user data
    Backend->>Backend: Create JWT access token (1h expiry)
    Backend->>Backend: Create refresh token (30d expiry)
    Backend->>MongoDB: Store refresh token
    Backend->>NextAuth: Return {token, refreshToken, user}
    NextAuth->>NextAuth: Create session with backend data only
    NextAuth->>Client: Redirect to /dashboard
    Client->>User: Show dashboard with user profile
```

### Key Points
- **Existing user found** by `googleId` in database
- **Profile updated** with latest Google data
- **Login timestamp** recorded
- **New tokens issued** for this session
- **NextAuth session** populated with backend data only

---

## 👤 Register Flow (New User)

### Step-by-Step Process

```mermaid
sequenceDiagram
    participant User
    participant Client
    participant NextAuth
    participant Backend
    participant MongoDB

    User->>Client: Click "Sign in with Google" (first time)
    Client->>NextAuth: signIn("google")
    NextAuth->>Google: OAuth redirect
    Google->>NextAuth: OAuth callback with user data
    NextAuth->>Backend: POST /google-auth (googleId, email, name, avatar)
    Backend->>MongoDB: Find user by googleId
    MongoDB->>Backend: User not found
    Backend->>Backend: Create new user object
    Backend->>MongoDB: Insert new user document
    MongoDB->>Backend: Return inserted user with _id
    Backend->>Backend: Create JWT access token (1h expiry)
    Backend->>Backend: Create refresh token (30d expiry)  
    Backend->>MongoDB: Store refresh token
    Backend->>NextAuth: Return {token, refreshToken, user}
    NextAuth->>NextAuth: Create session with backend data only
    NextAuth->>Client: Redirect to /dashboard
    Client->>User: Show dashboard with "Welcome" message
```

### Key Points
- **New user created** when `googleId` not found
- **Default role** assigned (`"user"`)
- **Timestamps set** (createdAt, updatedAt, lastLoginAt)
- **Same token flow** as existing user
- **Identical session creation** - no difference client-side

---

## 🔄 Token Refresh Flow

### Step-by-Step Process

```mermaid
sequenceDiagram
    participant Client
    participant Backend
    participant MongoDB

    Client->>Client: Detect access token expired (401 from API)
    Client->>Backend: POST /refresh {refreshToken}
    Backend->>Backend: Verify refresh token JWT
    Backend->>MongoDB: Check refresh token exists in database
    MongoDB->>Backend: Return stored refresh token
    Backend->>MongoDB: Get user data by userId
    MongoDB->>Backend: Return current user data
    Backend->>Backend: Create new JWT access token (1h expiry)
    Backend->>Client: Return {token, user}
    Client->>Client: Update session with new access token
    Client->>Client: Retry original API request
```

### Key Points
- **Refresh tokens stored** in database for revocation
- **User data refreshed** from database (role changes, etc.)
- **New access token** issued with latest user data
- **Refresh token remains** valid until 30-day expiry
- **Session updated** with new token and user data

---

## 🚪 Logout Flow

### Step-by-Step Process

```mermaid
sequenceDiagram
    participant User
    participant Client
    participant NextAuth
    participant Backend
    participant MongoDB

    User->>Client: Click "Sign Out"
    Client->>NextAuth: signOut()
    NextAuth->>Client: Clear session data
    Client->>Backend: POST /logout {refreshToken} (optional)
    Backend->>MongoDB: Delete refresh token from database
    MongoDB->>Backend: Confirm deletion
    Backend->>Client: Return success
    Client->>User: Redirect to home page
```

### Key Points
- **NextAuth clears** session immediately
- **Optional backend call** to revoke refresh token
- **Database cleanup** prevents token reuse
- **Simple redirect** to public pages

---

## 🔒 API Request Flow (Protected Routes)

### Step-by-Step Process

```mermaid
sequenceDiagram
    participant Client
    participant NextAuth
    participant Backend
    
    Client->>NextAuth: Get session
    NextAuth->>Client: Return session with backendToken
    Client->>Backend: API request with Authorization: Bearer {backendToken}
    Backend->>Backend: Verify JWT access token
    alt Token Valid
        Backend->>Backend: Extract user data from token
        Backend->>Backend: Process API request
        Backend->>Client: Return API response
    else Token Expired
        Backend->>Client: Return 401 Unauthorized
        Client->>Client: Trigger refresh token flow
    end
```

### Key Points
- **Session contains** `backendToken` for API requests
- **JWT verification** on every protected endpoint
- **User context** extracted from valid tokens
- **Automatic refresh** triggered on 401 errors

---

## 🛡️ Security Principles

### Backend-Driven Authentication
- **No standalone client sessions** - backend must validate all auth
- **Database storage required** - users and refresh tokens persisted
- **JWT contains user context** - role, permissions embedded
- **Refresh tokens revocable** - stored in database for security

### Token Strategy
- **Short-lived access tokens** (1 hour) - minimize exposure
- **Long-lived refresh tokens** (30 days) - reduce login frequency  
- **Refresh tokens stored** - enable revocation and session management
- **JWT secrets secure** - environment variable only

### Flow Consistency
- **Same endpoints** for login and register - backend determines flow
- **Uniform responses** - consistent error handling and data format
- **NextAuth integration** - session mechanics handled by framework
- **Simple client logic** - complex auth handled server-side

---

## 🔧 Environment Configuration

### Client (.env.local)
```bash
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-secret-key
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
NEXT_PUBLIC_AUTH_API_URL=http://localhost:8081
```

### Server (.env)
```bash
MONGODB_URI=your-mongodb-connection-string
DATABASE_NAME=syntaxmem
JWT_SECRET=your-jwt-secret-minimum-32-chars
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
CORS_ORIGINS=http://localhost:3000
```

---

**Remember**: Simple ≠ "not good". Simple = elegant, secure, maintainable authentication flows that scale with your application needs.