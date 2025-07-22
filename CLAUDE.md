# SyntaxMem - AI Assistant Context

**Last Updated**: 2025-07-22  
**Current Status**: Phase 1 Complete ✅ | Phase 2 Ready to Begin  
**Branch**: development  

## 🎯 Project Overview
SyntaxMem is an interactive coding practice platform where users complete masked code snippets to improve programming skills. Think "fill-in-the-blanks" for code learning.

**Architecture**: Next.js 15 client + Python serverless backend (Google Cloud Functions) + MongoDB Atlas

## 📁 Current Project State

### Client (`/client/`) - Phase 1 Complete ✅
- **Framework**: Next.js 15 + React 19 + TypeScript + Tailwind CSS + Shadcn/ui
- **Authentication**: NextAuth.js v5 with Google OAuth (JWT-only, no database sessions)
- **State**: Zustand stores + TanStack Query for server state
- **Status**: Landing page, auth system, navigation, and foundation complete
- **Next**: CodeMirror integration for practice interface (Phase 2)

### Server (`/server/`) - Core Functions Implemented ✅
- **Functions**: auth, snippets, practice, leaderboard, forum
- **Shared**: masking.py (Pygments), database.py (Motor), auth_middleware.py (JWT)
- **Status**: All microservices implemented, ready for deployment

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
cd server
./dev-server.sh      # Start all local functions
./test-api.sh        # Test API endpoints
./deploy.sh          # Deploy to Google Cloud
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
- **Animations**: Framer Motion for complex animations, CSS for simple ones

### Python Function Standards
```python
# FastAPI function structure (keep consistent)
@app.post("/endpoint")
async def function_name(
    request: RequestModel,
    user_data: Dict[str, Any] = Depends(verify_token)
):
    try:
        # 1. Validate input
        # 2. Database operations
        # 3. Business logic
        # 4. Return response with create_response()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Operation failed: {str(e)}")
```

## 🗂️ File Organization Rules

### Client Structure (maintain this structure)
```
src/
├── app/                 # Next.js App Router pages
├── components/
│   ├── ui/             # Shadcn/ui base components
│   ├── layout/         # Navigation, Footer, etc.
│   ├── auth/           # Authentication components
│   ├── practice/       # Practice interface (Phase 2)
│   └── common/         # Shared components
├── lib/
│   ├── api/            # API client functions
│   ├── auth/           # NextAuth config
│   └── utils.ts        # Utility functions
├── stores/             # Zustand state stores
├── types/              # TypeScript definitions
└── hooks/              # Custom React hooks
```

### Server Structure (maintain this structure)
```
server/
├── functions/          # Individual Cloud Functions
│   ├── auth/
│   ├── snippets/
│   ├── practice/
│   ├── leaderboard/
│   └── forum/
├── shared/             # Shared utilities
│   ├── database.py
│   ├── auth_middleware.py
│   ├── masking.py
│   ├── config.py
│   └── utils.py
└── [deploy scripts]
```

## 🔧 Key Technical Decisions

### Database Schema (MongoDB)
- **Users**: googleId, email, name, avatar, role, preferences, stats
- **Snippets**: Dual system (official/personal), language, difficulty, type, status
- **Practice Sessions**: userId, snippetId, maskedCode, answers, score, timeSpent
- **Leaderboard**: Official snippets only, language-based rankings

### Authentication Flow
1. Google OAuth via NextAuth.js (client)
2. Token exchange with backend `/auth/google-auth`
3. JWT token storage (client localStorage via NextAuth)
4. Backend validates JWT on protected routes

### Code Masking Algorithm
- Uses Pygments tokenization for Python/JavaScript
- Difficulty scale 1-10 affects masking probability
- Priority: keywords → functions → variables
- Preserves imports, comments, strings

## 📋 Current Phase 2 Tasks

### Ready to Implement
1. **CodeMirror Integration** (`client/src/components/practice/`)
   - code-editor.tsx with syntax highlighting
   - Theme integration (dark/light)
   - Language support (Python, JavaScript)

2. **Practice Interface** (`client/src/app/practice/`)
   - practice/page.tsx - snippet selection
   - practice/[id]/page.tsx - practice session
   - Real-time code completion

3. **API Integration**
   - Connect to `/snippets/mask` endpoint
   - Practice session management
   - Score submission and display

## 🚨 Critical Rules for AI Assistants

### Always Maintain
1. **Phase tracking** - Update `client/PROGRESS.md` when completing features
2. **Type safety** - No `any` types, proper Zod validation
3. **Component consistency** - Follow established patterns
4. **Error handling** - Proper try/catch with user-friendly messages
5. **Authentication** - Verify JWT tokens on all protected routes

### Never Break
1. **File structure** - Don't reorganize existing folders
2. **Naming conventions** - Keep kebab-case for files, PascalCase for components
3. **Import paths** - Use `@/` prefix for absolute imports
4. **Database schema** - Don't modify collection structures without updating all related code
5. **Security** - Never expose JWT secrets or remove auth middleware

### Before Making Changes
1. **Read current progress** in `client/PROGRESS.md`
2. **Check existing patterns** in similar components
3. **Test authentication flow** if touching auth code
4. **Verify builds pass** with `npm run build`
5. **Update progress docs** when completing features

## 🔗 Key Files to Reference
- `CONTEXT.md` - Complete project specification
- `client/PROGRESS.md` - Development progress tracker
- `client/DEVELOPMENT.md` - Comprehensive client development plan
- `server/CONFIG.md` - Server configuration guide
- `server/SETUP.md` - Google Cloud Functions setup

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

**Remember**: This is an incremental development process. Each phase builds on the previous one. Always test current functionality before adding new features. Keep the codebase uniform and follow established patterns! 🚀