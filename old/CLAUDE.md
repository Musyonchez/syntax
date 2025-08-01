# SyntaxMem - AI Assistant Context

**Last Updated**: 2025-07-26  
**Current Status**: Production Ready ✅ | Client Optimized ✅ | Server Enhanced ✅  
**Branch**: development  

## 🎯 Project Overview
SyntaxMem is an interactive coding practice platform where users complete masked code snippets to improve programming skills. Think "fill-in-the-blanks" for code learning.

**Architecture**: Next.js 15 client + Python serverless backend (Google Cloud Functions) + MongoDB Atlas

## 📁 Current Project State

### Client (`/client/`) - Optimized & Production Ready ✅
- **Framework**: Next.js 15 + React 19 + TypeScript + Tailwind CSS + Shadcn/ui
- **Authentication**: NextAuth.js v5 with Google OAuth (JWT-only, simplified auth flow)
- **State**: Zustand stores + TanStack Query for server state
- **Practice Interface**: Complete CodeMirror integration with masked code editor
- **Status**: Phase 1 & 2 complete, recently optimized to remove 500+ lines of bloated code
- **Next**: Community features (leaderboard, snippets management, forum UI)

### Server (`/server/`) - Production Ready ✅
- **Functions**: auth (8081), snippets (8082), practice (8083), leaderboard (8084), forum (8085)
- **Shared**: Enhanced utilities with proper logging, validation, and security
- **Status**: All microservices production-ready with comprehensive improvements
- **Recent**: Major security and performance enhancements applied to all functions

## 🚀 Development Commands

### Client Development
```bash
cd client
npm run dev          # Start dev server (http://localhost:3000)
npm run build        # Production build
npm run lint         # ESLint check
```

### Server Development  
```bash
# Run each service in separate terminals
cd server/functions/auth && source venv/bin/activate && python -m flask --app main run --host=0.0.0.0 --port=8081 --debug
cd server/functions/snippets && source venv/bin/activate && python -m flask --app main run --host=0.0.0.0 --port=8082 --debug
cd server/functions/practice && source venv/bin/activate && python -m flask --app main run --host=0.0.0.0 --port=8083 --debug
cd server/functions/leaderboard && source venv/bin/activate && python -m flask --app main run --host=0.0.0.0 --port=8084 --debug
cd server/functions/forum && source venv/bin/activate && python -m flask --app main run --host=0.0.0.0 --port=8085 --debug
```

## 🎨 Code Style & Standards

### TypeScript Standards
- **Strict mode enabled** - no `any` types
- **Functional components** with hooks
- **Server components** by default, client components only when needed
- **Zod validation** for all API schemas

### Component Patterns
```typescript
// Component structure (keep consistent)
export function ComponentName() {
  // 1. State and hooks first
  // 2. Event handlers
  // 3. Effects
  // 4. Return JSX
}

// File naming
components/feature/component-name.tsx  // kebab-case
types/feature.ts                       // feature-based grouping
lib/api/feature.ts                     // feature-based API
```

### UI Component Standards
- **Use Shadcn/ui components** from `/components/ui/`
- **Consistent spacing**: `className="space-y-4"` for vertical, `space-x-4` for horizontal
- **Color classes**: Use theme colors like `text-foreground`, `bg-background`
- **Icons**: Use Lucide React icons consistently
- **Animations**: CSS transitions preferred over heavy animation libraries

### Python Function Standards
```python
# Flask function structure (keep consistent)
@app.post("/endpoint")
async def function_name():
    try:
        # 1. Validate input with proper validation functions
        # 2. Database operations
        # 3. Business logic
        # 4. Return response with create_response()
    except Exception as e:
        logger.error(f"Operation failed: {e}")
        return create_error_response("Operation failed", 500)
```

## 🗂️ File Organization Rules

### Client Structure (maintain this structure)
```
src/
├── app/                 # Next.js App Router pages
├── components/
│   ├── ui/             # Shadcn/ui base components
│   ├── layout/         # Navigation, Footer (optimized)
│   ├── auth/           # Authentication components
│   ├── practice/       # Practice interface (complete)
│   ├── home/           # Landing page components
│   └── common/         # Shared components
├── lib/
│   ├── api/            # API client functions (simplified)
│   ├── auth/           # NextAuth config (optimized)
│   └── utils.ts        # Utility functions
├── stores/             # Zustand state stores (minimal)
├── types/              # TypeScript definitions
└── hooks/              # Custom React hooks
```

### Server Structure (maintain this structure)
```
server/
├── functions/          # Individual Cloud Functions
│   ├── auth/           # Port 8081 - JWT & Google OAuth
│   ├── snippets/       # Port 8082 - Code management
│   ├── practice/       # Port 8083 - Sessions & scoring
│   ├── leaderboard/    # Port 8084 - Rankings
│   └── forum/          # Port 8085 - Discussions
├── shared/             # Shared utilities
│   ├── database.py     # MongoDB connections
│   ├── auth_middleware.py # JWT validation
│   ├── masking.py      # Code masking engine
│   ├── config.py       # Environment config
│   └── utils.py        # Response utilities
```

## 🔧 Key Technical Decisions

### Database Schema (MongoDB)
- **Users**: googleId, email, name, avatar, role, preferences, stats
- **Snippets**: Dual system (official/personal), language, difficulty, type, status
- **Practice Sessions**: userId, snippetId, maskedCode, answers, score, timeSpent
- **Leaderboard**: Official snippets only, language-based rankings
- **Forum Posts**: posts, replies, voting, categories

### Authentication Flow
1. Google OAuth via NextAuth.js (client)
2. Simplified token exchange with backend `/auth/google-auth`
3. JWT token storage (client localStorage via NextAuth)
4. Backend validates JWT on protected routes

### Code Masking Algorithm
- Uses Pygments tokenization for Python/JavaScript
- Difficulty scale 1-10 affects masking probability
- Priority: keywords → functions → variables
- Preserves imports, comments, strings

## 📋 Current Status

### ✅ Complete & Production Ready
1. **Authentication System** - Google OAuth, JWT handling, secure flows
2. **Practice Interface** - CodeMirror integration, masked code editor, scoring
3. **API Infrastructure** - All 5 microservices with comprehensive validation
4. **Database Operations** - MongoDB with proper aggregation pipelines
5. **Security** - Input validation, sanitization, error handling across all services
6. **Code Quality** - Removed 500+ lines of bloated code, optimized components

### 🔄 Ready for Implementation (Phase 3)
1. **Leaderboard UI** - Rankings display, filtering, real-time updates
2. **Snippets Management** - Browse, create, edit, submit snippets interface
3. **Forum System** - Posts, comments, voting UI components

## 🚨 Critical Rules for AI Assistants

### Always Maintain
1. **Type safety** - No `any` types, proper Zod validation
2. **Component consistency** - Follow established patterns
3. **Error handling** - Proper try/catch with structured logging
4. **Authentication** - Verify JWT tokens on all protected routes
5. **Code quality** - Avoid over-engineering, keep components focused

### Never Break
1. **File structure** - Don't reorganize existing folders
2. **Naming conventions** - Keep kebab-case for files, PascalCase for components
3. **Import paths** - Use `@/` prefix for absolute imports
4. **Database schema** - Don't modify collection structures without updating all related code
5. **Security** - Never expose JWT secrets or remove auth middleware
6. **Simplicity** - Don't add unnecessary complexity or heavy animation libraries

### Before Making Changes
1. **Check existing patterns** in similar components
2. **Test builds** with `npm run build` and `npm run lint`
3. **Verify server functions** compile and start properly
4. **Keep components focused** - avoid creating overly complex components
5. **Use CSS transitions** instead of heavy animation libraries when possible

## 🔗 Recent Major Improvements (July 26, 2025)

### Client Optimizations
- **API Client**: Simplified from 213 to 108 lines (49% reduction)
- **Authentication**: Removed complex token refresh logic, simplified config
- **Theme Management**: Removed redundant Zustand store, use next-themes only
- **Navigation**: Reduced from 433 to 151 lines (65% reduction)
- **Performance**: Removed excessive Framer Motion animations

### Server Enhancements
- **Security**: Added comprehensive input validation across all functions
- **Logging**: Replaced debug prints with structured logging
- **Error Handling**: Standardized error responses and exception handling
- **Performance**: Optimized MongoDB queries and pagination
- **Consistency**: Applied uniform patterns across all microservices

## 💡 Environment Setup
```bash
# Client
cp client/.env.example client/.env.local
# Add: NEXTAUTH_URL, NEXTAUTH_SECRET, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET

# Server  
cp server/.env.example server/.env
# Add: MONGODB_URI, JWT_SECRET, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET
```

---

**Remember**: Keep things simple and focused. The codebase is now optimized and production-ready. Avoid over-engineering and maintain the clean, efficient patterns that have been established! 🚀