# SyntaxMem - Simple, Uniform, Consistent

**Last Updated**: 2025-07-29  
**Status**: Phase 2 Complete ✅ | Authentication System Production-Ready 🚀  
**Branch**: main

## 🎯 Core Doctrine

**One Principle**: Simple, Uniform, Consistent

Every decision, every line of code, every component must follow this principle:

- **Simple**: No complexity unless absolutely necessary _(Simple ≠ "not good" - it means elegant, maintainable, excellent)_
- **Uniform**: Same patterns everywhere, no exceptions
- **Consistent**: Predictable structure and behavior throughout

## 📁 Project Structure

### Production-Ready Architecture

```
syntax/
├── client/     # Next.js 15 frontend with auth integration
├── server/     # Python serverless functions
│   ├── auth/       # Google OAuth + JWT (port 8081) ✅ COMPLETE
│   ├── practice/   # Practice sessions (port 8082) 🚧 PLANNED
│   ├── snippets/   # Code management (port 8083) 🚧 PLANNED
│   ├── shared/     # Common utilities ✅ COMPLETE
│   ├── schemas/    # Data validation ✅ COMPLETE
│   └── tests/      # Modular test suite ✅ COMPLETE
└── old/        # Previous implementation (preserved)
```

### Why This Structure?

- **3 functions max**: auth, practice, snippets (removed leaderboard, forum bloat)
- **Client-first**: Build UI first, then only the server endpoints it needs
- **Serverless**: Google Cloud Functions for cost efficiency
- **Iterative**: Add features one at a time, test each addition

## 🚨 Development Rules

### The Sacred Laws (NEVER BREAK)

1. **Simple First**: Always choose the simplest solution that works _(elegant, not cheap)_
2. **No Over-Engineering**: If it's complex, it's wrong _(complexity is the enemy of excellence)_
3. **Client Drives Server**: Build client pages first, server endpoints second
4. **One Pattern Everywhere**: Same structure, same naming, same approach
5. **Test As You Build**: Each feature must work before adding the next

### Client Rules

- **Next.js 15** with App Router (simple routing)
- **TypeScript strict** (no `any` types ever)
- **Tailwind CSS** (no custom CSS complexity)
- **Minimal components** (each does one thing well)
- **No unnecessary animations** (CSS transitions only)

### Server Rules

- **Flask functions** (simple, straightforward)
- **Same structure** in every function (uniform imports, patterns)
- **Minimal endpoints** (only what client actually uses)
- **Consistent responses** (same format everywhere)
- **Simple error handling** (no complex exception hierarchies)

### Database Rules

- **MongoDB** (document-based simplicity)
- **Simple collections** (users, snippets, sessions)
- **No complex joins** (keep queries simple)
- **Consistent field names** (same naming everywhere)

## ✅ Completed Phases

### Phase 1: Foundation ✅ COMPLETE

1. **Landing page** ✅ Simple hero + Google signin
2. **Google OAuth** ✅ Complete backend auth endpoint
3. **Protected dashboard** ✅ Shows user profile + security controls

### Phase 2: Session Management ✅ COMPLETE

1. **Token cleanup** ✅ Automatic expired token removal
2. **Logout all devices** ✅ Backend endpoint + frontend button
3. **Session limits** ✅ 2-token maximum per user
4. **Schema validation** ✅ Complete data validation system
5. **Modular test suite** ✅ Automated testing for all features

## 🚧 Planned Phases

### Phase 3: Core Features

1. **Practice sessions** - Interactive masked code completion
2. **Code snippets** - CRUD operations with masking algorithm
3. **Scoring system** - Simple progress tracking

### Phase 4: Polish

1. **Browse snippets** - Filtered list with search
2. **User stats** - Practice progress and achievements
3. **Admin features** - Content management

## 📋 File Patterns

### Client Component Structure

```typescript
// components/simple-name.tsx
export function SimpleName() {
  // 1. State (minimal)
  // 2. Handlers (simple)
  // 3. Return JSX (clean)
}
```

### Server Function Structure

```python
# server/function/main.py
from flask import Flask

app = Flask(__name__)

@app.route('/endpoint')
def simple_endpoint():
    # 1. Validate input
    # 2. Process (simple logic)
    # 3. Return response
    return {'success': True, 'data': result}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=808X, debug=True)
```

## 🎨 Code Standards

### Naming Conventions

- **Files**: `kebab-case.tsx`, `main.py`
- **Components**: `PascalCase`
- **Functions**: `snake_case` (Python), `camelCase` (TypeScript)
- **Variables**: `camelCase` (TypeScript), `snake_case` (Python)

### Import Order (Always)

```typescript
// 1. React/Next
import { useState } from "react";
// 2. Libraries
import axios from "axios";
// 3. Components
import { Button } from "./button";
// 4. Utils
import { cn } from "@/lib/utils";
```

```python
# 1. Standard library
import os
# 2. Third party
from flask import Flask
# 3. Local
from shared.utils import create_response
```

## 🚫 What NOT to Do

### Forbidden Complexity

- ❌ Multiple state management libraries
- ❌ Over-engineered animations
- ❌ Complex component hierarchies
- ❌ Microservices for everything
- ❌ Premature optimization
- ❌ Feature creep

### Forbidden Patterns

- ❌ Creating components with 500+ lines
- ❌ Adding libraries without justification
- ❌ Building features "just in case"
- ❌ Complex error handling
- ❌ Debug code in production

## 🔄 Development Workflow

### The Simple Cycle

1. **Pick one small feature**
2. **Build client UI first** (static, simple)
3. **Add server endpoint** (minimal, focused)
4. **Connect and test** (make it work)
5. **Commit and move on** (don't over-polish)

### Example: Adding Practice Feature

1. Create `/practice` page with static masked code
2. Add `/practice/start` endpoint that returns one snippet
3. Connect client to fetch and display real data
4. Add submit functionality (client form + server endpoint)
5. Done. Move to next feature.

## 🎯 Success Metrics ✅

### Achieved Goals

- **Authentication system** - Production-ready with full test coverage
- **Modular architecture** - Easy to extend and maintain
- **Automated testing** - All features validated automatically
- **Clean codebase** - Follows Simple, Uniform, Consistent doctrine
- **Security features** - Token cleanup, logout all devices, session limits

### Ongoing Targets

- **Build time stays fast** (under 30 seconds)
- **New features take hours, not days** (simplicity)
- **Code is boring and predictable** (uniform, consistent)
- **Anyone can understand it immediately** (simple)

## 🗂️ Old vs New

### What We Learned from `/old/`

- ✅ **Good**: Core features work, auth flow solid, masking algorithm effective
- ❌ **Bad**: Over-engineered, 5 services, complex state management, 500+ lines of bloat
- 🎯 **New Approach**: Keep the good ideas, rebuild with doctrine

### Preserved Knowledge

- Google OAuth flow pattern
- JWT token structure
- Code masking algorithm
- MongoDB schema design
- Practice session scoring logic

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
cd server/auth && source venv/bin/activate && python -m flask --app main run --host=0.0.0.0 --port=8081 --debug
cd server/snippets && source venv/bin/activate && python -m flask --app main run --host=0.0.0.0 --port=8082 --debug
cd server/practice && source venv/bin/activate && python -m flask --app main run --host=0.0.0.0 --port=8083 --debug
cd server/leaderboard && source venv/bin/activate && python -m flask --app main run --host=0.0.0.0 --port=8084 --debug
cd server/forum && source venv/bin/activate && python -m flask --app main run --host=0.0.0.0 --port=8085 --debug

## 🚀 Production Ready

**Current Status**: Phase 2 complete - Authentication system production-ready
**Next Step**: Build core features (practice sessions, code snippets)
**Foundation**: Complete auth system with automated testing
**Principle**: Simple, Uniform, Consistent

---

**Remember**: If it's not simple, uniform, and consistent - it doesn't belong in this codebase. Period. 🎯

*Simple ≠ "not good". Simple = choosing the most elegant solution. The best code is so simple it looks obvious in hindsight.*
```

