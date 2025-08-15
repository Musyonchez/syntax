# SyntaxMem - Simple, Uniform, Consistent

**Last Updated**: 2025-08-15  
**Status**: Fresh Start 🚀 | Unified Next.js Architecture  
**Branch**: main

## 🎯 Core Doctrine

**One Principle**: Simple, Uniform, Consistent

Every decision, every line of code, every component must follow this principle:

- **Simple**: No complexity unless absolutely necessary _(Simple ≠ "not good" - it means elegant, maintainable, excellent)_
- **Uniform**: Same patterns everywhere, no exceptions
- **Consistent**: Predictable structure and behavior throughout

## 📁 Project Structure

### Unified Next.js Architecture

```
syntax/
├── app/                    # Next.js 15 App Router
│   ├── (auth)/            # Auth route group
│   │   ├── login/         # Login page
│   │   └── signup/        # Signup page
│   ├── dashboard/         # Protected dashboard
│   ├── practice/          # Practice sessions
│   ├── snippets/          # Code snippet management
│   ├── api/               # API routes (replaces separate server)
│   │   ├── auth/          # Authentication endpoints
│   │   ├── snippets/      # Snippet CRUD endpoints
│   │   └── practice/      # Practice session endpoints
│   ├── globals.css        # Global styles
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Home page
├── components/            # Reusable components
│   ├── auth/              # Authentication components
│   ├── ui/                # Base UI components
│   ├── practice/          # Practice-specific components
│   └── snippets/          # Snippet-specific components
├── lib/                   # Utilities and configurations
│   ├── auth.ts            # Authentication config
│   ├── db.ts              # Database connection
│   ├── utils.ts           # Utility functions
│   └── validations.ts     # Zod schemas
├── types/                 # TypeScript type definitions
└── public/                # Static assets
```

### Why This Structure?

- **Single App**: No more client/server separation complexity
- **API Routes**: Next.js API routes replace separate Flask services
- **File-based Routing**: Intuitive navigation structure
- **Colocation**: Related features grouped together
- **Type Safety**: End-to-end TypeScript

## 🚨 Development Rules

### The Sacred Laws (NEVER BREAK)

1. **Simple First**: Always choose the simplest solution that works _(elegant, not cheap)_
2. **No Over-Engineering**: If it's complex, it's wrong _(complexity is the enemy of excellence)_
3. **One Pattern Everywhere**: Same structure, same naming, same approach
4. **API Routes Over External Services**: Use Next.js API routes instead of separate servers
5. **Test As You Build**: Each feature must work before adding the next

### Next.js Rules

- **App Router Only** (no pages directory)
- **TypeScript Strict** (no `any` types ever)
- **Tailwind CSS** (no custom CSS complexity)
- **Server Components** (default, use client components only when needed)
- **API Routes** (for all backend functionality)

### Database Rules

- **MongoDB** (document-based simplicity)
- **Mongoose ODM** (for schema validation and consistency)
- **Simple collections** (users, snippets, sessions)
- **No complex joins** (keep queries simple)
- **Consistent field names** (same naming everywhere)

## ✅ Planned Implementation Phases

### Phase 1: Foundation
1. **Landing page** - Simple hero + authentication
2. **Authentication** - NextAuth.js with Google OAuth
3. **Protected routes** - Middleware-based protection
4. **Database setup** - MongoDB connection and basic schemas

### Phase 2: Core Features
1. **User dashboard** - Profile and session management
2. **Snippet management** - CRUD operations via API routes
3. **Practice sessions** - Interactive masked code completion
4. **Progress tracking** - Simple scoring system

### Phase 3: Polish
1. **Browse snippets** - Filtered list with search
2. **User statistics** - Practice progress and achievements
3. **Admin features** - Content management dashboard

## 📋 File Patterns

### Component Structure

```typescript
// components/feature/component-name.tsx
'use client'; // Only if client-side interactivity needed

export function ComponentName() {
  // 1. State (minimal)
  // 2. Handlers (simple)
  // 3. Return JSX (clean)
}
```

### API Route Structure

```typescript
// app/api/feature/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  try {
    // 1. Validate input
    // 2. Process (simple logic)
    // 3. Return response
    return NextResponse.json({ success: true, data: result });
  } catch (error) {
    return NextResponse.json({ error: 'Message' }, { status: 500 });
  }
}
```

### Page Structure

```typescript
// app/feature/page.tsx
export default function FeaturePage() {
  // 1. Data fetching (server component)
  // 2. Simple logic
  // 3. Return JSX
}
```

## 🎨 Code Standards

### Naming Conventions

- **Files**: `kebab-case.tsx`, `route.ts`
- **Components**: `PascalCase`
- **Functions**: `camelCase`
- **Variables**: `camelCase`
- **Constants**: `UPPER_SNAKE_CASE`

### Import Order (Always)

```typescript
// 1. React/Next
import { NextRequest } from 'next/server';
// 2. Libraries
import { z } from 'zod';
// 3. Internal
import { auth } from '@/lib/auth';
// 4. Types
import type { User } from '@/types';
```

## 🚫 What NOT to Do

### Forbidden Complexity

- ❌ Separate backend services
- ❌ Multiple state management libraries
- ❌ Over-engineered animations
- ❌ Complex component hierarchies
- ❌ Premature optimization
- ❌ Feature creep

### Forbidden Patterns

- ❌ Pages directory (use App Router only)
- ❌ External API calls to own services
- ❌ Creating components with 500+ lines
- ❌ Adding libraries without justification
- ❌ Building features "just in case"
- ❌ Complex error handling

## 🔄 Development Workflow

### The Simple Cycle

1. **Pick one small feature**
2. **Create API route** (if backend needed)
3. **Build page/component** (consume API)
4. **Add types and validation** (ensure type safety)
5. **Test and commit** (make it work, move on)

### Example: Adding Practice Feature

1. Create API route: `app/api/practice/route.ts`
2. Create page: `app/practice/page.tsx`
3. Add components: `components/practice/session.tsx`
4. Add types: `types/practice.ts`
5. Test functionality and commit

## 🎯 Technology Stack

### Core Stack

- **Next.js 15**: App Router, API Routes, Server Components
- **TypeScript**: Strict mode, no any types
- **Tailwind CSS**: Utility-first styling
- **MongoDB**: Document database
- **Mongoose**: ODM for schema validation

### Authentication

- **NextAuth.js**: Session management
- **Google OAuth**: Primary authentication provider
- **JWT**: Secure token-based sessions

### Development Tools

- **ESLint**: Code linting
- **Prettier**: Code formatting
- **TypeScript**: Type checking

## 🚀 Development Commands

### Core Commands

```bash
npm run dev          # Start development server
npm run build        # Production build
npm run start        # Start production server
npm run lint         # ESLint check
npm run type-check   # TypeScript validation
```

### Database Commands

```bash
# MongoDB connection will be handled via environment variables
# MONGODB_URI=mongodb://localhost:27017/syntaxmem
```

## 🎯 Success Metrics

### Target Goals

- **Single codebase** - No client/server separation
- **Fast development** - New features in hours, not days
- **Type safety** - End-to-end TypeScript
- **Simple deployment** - Single Next.js app
- **Predictable patterns** - Every feature follows same structure

### Performance Targets

- **Build time** - Under 30 seconds
- **Page load** - Under 2 seconds
- **API response** - Under 500ms
- **Bundle size** - Optimized and minimal

## 🛠️ Environment Setup

### Required Environment Variables

```bash
# Authentication
NEXTAUTH_SECRET=your-secret-here
NEXTAUTH_URL=http://localhost:3000
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# Database
MONGODB_URI=mongodb://localhost:27017/syntaxmem

# Optional
NODE_ENV=development
```

## 🚀 Ready to Build

**Current Status**: Fresh start with unified Next.js architecture  
**Next Steps**: Implement authentication and basic pages  
**Foundation**: Clean Next.js 15 app with TypeScript and Tailwind  
**Principle**: Simple, Uniform, Consistent

---

**Remember**: If it's not simple, uniform, and consistent - it doesn't belong in this codebase. Period. 🎯

*Simple ≠ "not good". Simple = choosing the most elegant solution. The best code is so simple it looks obvious in hindsight.*