# SyntaxMem - Development Guide

A comprehensive guide for developing and maintaining the SyntaxMem platform.

## Quick Start

### Prerequisites
- Node.js 18+
- Python 3.9+
- MongoDB Atlas account
- Google OAuth app credentials

### Development Setup
1. **Clone and setup environment**:
   ```bash
   git clone <repository>
   cd syntax
   ```

2. **Client setup**:
   ```bash
   cd client
   npm install
   cp .env.example .env.local
   # Edit .env.local with your credentials
   npm run dev
   ```

3. **Server setup** (run each in separate terminals):
   ```bash
   # Auth service
   cd server/functions/auth
   python -m venv venv && source venv/bin/activate
   pip install -r requirements.txt
   python -m flask --app main run --host=0.0.0.0 --port=8081 --debug

   # Repeat for snippets (8082), practice (8083), leaderboard (8084), forum (8085)
   ```

## Architecture Overview

### Frontend (Next.js 15)
- **App Router**: Server-first architecture with client components when needed
- **TypeScript**: Strict mode, no `any` types allowed
- **Styling**: Tailwind CSS v4 with Shadcn/ui components
- **State**: Zustand (client) + TanStack Query (server state)
- **Auth**: NextAuth.js v5 with Google OAuth

### Backend (Python Flask)
- **Microservices**: 5 independent services on ports 8081-8085
- **Database**: MongoDB with Motor async driver
- **Authentication**: JWT with Google OAuth integration
- **Code Masking**: Pygments-based intelligent masking

### Database (MongoDB)
- **Collections**: users, snippets, practice_sessions, forum_posts
- **Indexes**: Optimized for common query patterns
- **Aggregation**: Complex pipelines for leaderboards and statistics

## Development Workflow

### 1. Starting Development
```bash
# Start all services in tmux or separate terminals
npm run dev          # Client (3000)
# Server services (8081-8085) - see setup above
```

### 2. Making Changes
- **Client**: Hot reload enabled, changes reflect immediately
- **Server**: Debug mode enabled, auto-restarts on file changes
- **Database**: Use MongoDB Compass for data inspection

### 3. Testing Changes
```bash
# Client testing
cd client
npm run build        # Test production build
npm run lint         # Check code quality

# Server testing
# Each service health check
curl http://localhost:8081/health
curl http://localhost:8082/health
# etc.
```

## Code Standards

### TypeScript/React Guidelines

#### Component Structure
```typescript
"use client" // Only when client features needed

import { useState, useEffect } from "react"
import { ComponentProps } from "@/types"

interface Props {
  // Define props with proper types
}

export function ComponentName({ prop }: Props) {
  // 1. Hooks and state
  const [state, setState] = useState()
  
  // 2. Event handlers
  const handleEvent = () => {
    // Handle event
  }
  
  // 3. Effects
  useEffect(() => {
    // Side effects
  }, [])
  
  // 4. Early returns
  if (!state) return <div>Loading...</div>
  
  // 5. Main render
  return (
    <div className="space-y-4">
      {/* Content */}
    </div>
  )
}
```

#### File Naming Conventions
- **Components**: `kebab-case.tsx` (e.g., `practice-session.tsx`)
- **Types**: `kebab-case.ts` (e.g., `practice-types.ts`)
- **API**: `kebab-case.ts` (e.g., `practice-api.ts`)
- **Pages**: Next.js App Router conventions

#### Import Organization
```typescript
// 1. React and Next.js
import { useState } from "react"
import Link from "next/link"

// 2. Third-party libraries
import { useQuery } from "@tanstack/react-query"

// 3. UI components
import { Button } from "@/components/ui/button"

// 4. Internal components
import { PracticeSession } from "@/components/practice/practice-session"

// 5. Utilities and types
import { cn } from "@/lib/utils"
import type { PracticeSessionType } from "@/types/practice"
```

### Python/Flask Guidelines

#### Function Structure
```python
@app.route("/endpoint", methods=["POST"])
def function_name():
    """Function description"""
    try:
        # 1. Input validation
        data = request.get_json()
        if not data:
            return create_error_response("Invalid JSON data", 400)
        
        # 2. Authentication (if required)
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return create_error_response("Authorization required", 401)
        
        token = auth_header.split(" ")[1]
        user_data = verify_jwt_token_simple(token)
        if not user_data:
            return create_error_response("Invalid token", 401)
        
        # 3. Input sanitization
        field = sanitize_string(data.get("field", ""), 100)
        
        # 4. Async database operations
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(_async_operation(user_data["user_id"], field))
            return create_response(result, "Operation successful")
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"Operation failed: {e}")
        return create_error_response("Operation failed", 500)

async def _async_operation(user_id: str, field: str):
    """Async helper function"""
    collection = await get_collection()
    # Database operations
    return result
```

#### Import Organization
```python
# 1. Standard library
import asyncio
import os
from datetime import datetime

# 2. Third-party
from flask import Flask, request, jsonify
from motor.motor_asyncio import AsyncIOMotorClient

# 3. Local imports
from shared.auth_middleware import verify_jwt_token_simple
from shared.utils import create_response, create_error_response
```

## API Development

### Client API Integration
```typescript
// Define types first
interface CreateRequestType {
  title: string
  content: string
}

interface CreateResponseType {
  id: string
  created_at: string
}

// API function
export const apiFunction = {
  async create(data: CreateRequestType): Promise<CreateResponseType> {
    const response = await serviceApi.post<CreateResponseType>('/create', data)
    if (!response.success || !response.data) {
      throw new Error(response.error || 'Create failed')
    }
    return response.data
  }
}
```

### Server API Implementation
```python
@app.route("/create", methods=["POST"])
def create_item():
    try:
        # Validation
        data = request.get_json()
        title = sanitize_string(data.get("title", ""), 100)
        content = sanitize_string(data.get("content", ""), 5000)
        
        if not title or not content:
            return create_error_response("Title and content required", 400)
        
        # Authentication
        user_data = verify_jwt_token_simple(get_token_from_request())
        
        # Business logic
        result = await_async_create(user_data["user_id"], title, content)
        
        return create_response(result, "Item created", 201)
        
    except Exception as e:
        logger.error(f"Create failed: {e}")
        return create_error_response("Create failed", 500)
```

## Database Operations

### MongoDB Best Practices
```python
# Use aggregation pipelines for complex queries
pipeline = [
    {"$match": {"userId": user_id, "status": "completed"}},
    {"$lookup": {
        "from": "snippets",
        "localField": "snippetId", 
        "foreignField": "_id",
        "as": "snippet"
    }},
    {"$sort": {"completedAt": -1}},
    {"$limit": per_page},
    {"$skip": skip}
]

cursor = collection.aggregate(pipeline)
results = await cursor.to_list(length=per_page)
```

### Indexing Strategy
```javascript
// Key indexes for performance
db.users.createIndex({ "googleId": 1 }, { unique: true })
db.snippets.createIndex({ "type": 1, "language": 1, "difficulty": 1 })
db.practice_sessions.createIndex({ "userId": 1, "status": 1, "completedAt": -1 })
db.forum_posts.createIndex({ "category": 1, "createdAt": -1 })
```

## Security Guidelines

### Input Validation
```python
def validate_and_sanitize(data: dict) -> dict:
    """Validate and sanitize user input"""
    return {
        "title": sanitize_string(data.get("title", ""), 100),
        "content": sanitize_string(data.get("content", ""), 5000),
        "difficulty": max(1, min(10, int(data.get("difficulty", 5))))
    }
```

### Authentication
```typescript
// Client-side auth check
const { data: session, status } = useSession()

if (status === "loading") return <div>Loading...</div>
if (!session) redirect("/auth/signin")

// Server-side auth middleware
function requireAuth(handler) {
  return async (req, res) => {
    const token = getToken({ req })
    if (!token) return res.status(401).json({ error: "Unauthorized" })
    
    return handler(req, res)
  }
}
```

## Performance Optimization

### Client-Side
- Use Server Components by default
- Implement proper loading states
- Optimize images with Next.js Image
- Use TanStack Query for caching
- Avoid over-engineering animations

### Server-Side
- Use MongoDB aggregation pipelines
- Implement proper pagination
- Use async operations
- Optimize database indexes
- Cache frequently accessed data

## Debugging

### Client Debugging
```typescript
// Use React DevTools and browser console
console.log("Debug info:", { state, props })

// TanStack Query DevTools
import { ReactQueryDevtools } from "@tanstack/react-query-devtools"
```

### Server Debugging
```python
# Use structured logging
logger.info(f"Processing request: {data}")
logger.error(f"Operation failed: {e}")

# Flask debug mode
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8081)
```

## Deployment

### Client (Vercel)
```bash
npm run build
# Deploy to Vercel
```

### Server (Google Cloud Functions)
```bash
gcloud functions deploy service-name \
  --runtime python39 \
  --trigger-http \
  --allow-unauthenticated \
  --source functions/service/
```

## Troubleshooting

### Common Issues
1. **Build Failures**: Check TypeScript errors and missing dependencies
2. **Auth Issues**: Verify environment variables and OAuth setup
3. **Database Errors**: Check MongoDB connection and indexes
4. **API Errors**: Check CORS settings and endpoint URLs

### Health Checks
```bash
# Check all services
curl http://localhost:3000/_next/health
curl http://localhost:8081/health
curl http://localhost:8082/health
curl http://localhost:8083/health
curl http://localhost:8084/health
curl http://localhost:8085/health
```

## Contributing

1. **Follow established patterns** in existing code
2. **Test thoroughly** with build and lint commands
3. **Maintain type safety** - no `any` types
4. **Keep components focused** - avoid over-engineering
5. **Use structured logging** instead of print statements
6. **Update documentation** when adding new features

---

Remember: Keep it simple, maintainable, and follow the established patterns! 🚀