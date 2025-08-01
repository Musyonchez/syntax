# SyntaxMem Client Source Rules

**Simple, Uniform, Consistent** development guidelines for the SyntaxMem frontend codebase.

## 🎯 Purpose

This document establishes the Sacred Laws for SyntaxMem client development to ensure:
- **Consistency** - Same patterns across all components and pages
- **Maintainability** - Code that's easy to understand and modify
- **Performance** - Optimal user experience and loading times
- **Accessibility** - Inclusive design for all users
- **Security** - Safe handling of user data and authentication

## 🚨 The Sacred Laws (NEVER BREAK)

### Component Rules

1. **Component Structure** - All components follow the same structure pattern
2. **TypeScript Required** - No JavaScript files, TypeScript only
3. **Props Interface** - Define explicit interfaces for all component props
4. **Default Exports** - Use default exports for all components
5. **File Naming** - kebab-case for files, PascalCase for components

### Authentication Rules

6. **Server-Side Auth** - Use server components for auth checks when possible
7. **Token Security** - Never expose JWT tokens in client-side code
8. **Redirect Pattern** - Use Next.js redirect() for unauthenticated users
9. **Session Validation** - Always validate session before accessing user data
10. **Logout Security** - Proper cleanup of client-side auth state

### Styling Rules

11. **Tailwind Only** - Use Tailwind CSS classes exclusively
12. **No Inline Styles** - Never use style attributes
13. **Responsive Design** - All components must work on mobile/tablet/desktop
14. **Dark Mode Support** - Use Tailwind dark: variants for theming
15. **Consistent Spacing** - Use Tailwind spacing scale (4, 8, 16, 24, etc.)

### Performance Rules

16. **Lazy Loading** - Use dynamic imports for heavy components
17. **Image Optimization** - Always use Next.js Image component
18. **Bundle Optimization** - Avoid importing entire libraries
19. **Server Components** - Prefer server components when possible
20. **Client Components** - Only use 'use client' when necessary

### Data Fetching Rules

21. **API Abstraction** - Use centralized API client functions
22. **Error Handling** - Consistent error handling across all API calls
23. **Loading States** - Always show loading indicators for async operations
24. **Cache Strategy** - Implement appropriate caching for API responses
25. **Type Safety** - Define TypeScript interfaces for all API responses

## 📁 File Organization Rules

### Directory Structure
```
src/
├── app/                    # Next.js App Router pages
├── components/             # Reusable components
│   ├── ui/                # Shadcn/UI components
│   ├── auth/              # Authentication components
│   ├── common/            # Shared components
│   └── [feature]/         # Feature-specific components
├── lib/                   # Utility functions
├── types/                 # TypeScript definitions
└── contexts/              # React contexts
```

### Naming Conventions

26. **Components** - PascalCase (e.g., `UserProfile.tsx`)
27. **Files** - kebab-case (e.g., `user-profile.tsx`)
28. **Directories** - kebab-case (e.g., `user-settings/`)
29. **Constants** - SCREAMING_SNAKE_CASE (e.g., `API_BASE_URL`)
30. **Functions** - camelCase (e.g., `getUserProfile`)

## 🧩 Component Patterns

### Standard Component Structure
```typescript
// Import order: React, Next.js, external, internal
import React from 'react'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { UserData } from '@/types/user'

// Props interface
interface ComponentProps {
  data: UserData
  onAction?: () => void
}

// Component with explicit return type
export default function Component({ data, onAction }: ComponentProps): JSX.Element {
  return (
    <div className="space-y-4">
      {/* Component content */}
    </div>
  )
}
```

### Server Component Pattern
```typescript
import { auth } from '@/lib/auth'
import { redirect } from 'next/navigation'

export default async function ServerComponent() {
  const session = await auth()
  
  if (!session?.user) {
    redirect('/login')
  }

  return (
    <div>
      {/* Server-rendered content */}
    </div>
  )
}
```

### Client Component Pattern
```typescript
'use client'

import { useState, useEffect } from 'react'

export default function ClientComponent() {
  const [state, setState] = useState<string>('')

  useEffect(() => {
    // Client-side effects
  }, [])

  return (
    <div>
      {/* Interactive content */}
    </div>
  )
}
```

## 🎨 Styling Guidelines

### Tailwind Class Order
31. **Layout** - display, position, flexbox
32. **Spacing** - margin, padding
33. **Sizing** - width, height
34. **Typography** - font, text
35. **Colors** - background, text, border
36. **Effects** - shadow, opacity, transform
37. **Responsive** - sm:, md:, lg:, xl:
38. **State** - hover:, focus:, active:
39. **Dark Mode** - dark:

### Example Class Order
```typescript
<div className="flex items-center justify-between w-full p-4 bg-white border border-gray-200 rounded-lg shadow-sm hover:shadow-md transition-shadow md:p-6 dark:bg-gray-800 dark:border-gray-700">
```

## 🔐 Security Rules

### Authentication
40. **No Hardcoded Secrets** - Use environment variables only
41. **Token Expiry** - Handle expired tokens gracefully
42. **CSRF Protection** - Use NextAuth.js built-in protection
43. **Secure Headers** - Implement security headers
44. **Input Validation** - Validate all user inputs

### Data Handling
45. **Sanitize Inputs** - Clean user data before processing
46. **Escape Outputs** - Prevent XSS attacks
47. **No Sensitive Logs** - Never log sensitive user data
48. **Secure Storage** - Use secure methods for client-side storage
49. **API Security** - Validate all API responses

## ♿ Accessibility Rules

### WCAG 2.1 Compliance
50. **Semantic HTML** - Use proper HTML elements
51. **Alt Text** - Provide alt text for all images
52. **Keyboard Navigation** - Ensure full keyboard accessibility
53. **Focus Indicators** - Visible focus states for all interactive elements
54. **ARIA Labels** - Use ARIA attributes when necessary
55. **Color Contrast** - Meet WCAG AA contrast requirements

### Screen Reader Support
56. **Heading Hierarchy** - Proper h1, h2, h3 structure
57. **Form Labels** - Associate labels with form inputs
58. **Error Messages** - Clear, descriptive error messages
59. **Loading States** - Announce loading states to screen readers
60. **Live Regions** - Use ARIA live regions for dynamic content

## 📱 Responsive Design Rules

### Breakpoint Strategy
61. **Mobile First** - Start with mobile design
62. **Progressive Enhancement** - Add features for larger screens
63. **Touch Targets** - Minimum 44px touch targets
64. **Content Reflow** - Ensure content works at all viewport sizes
65. **Performance** - Optimize for mobile networks

## 🚫 What NOT to Do

### Forbidden Patterns
- ❌ Inline styles or style attributes
- ❌ JavaScript files (TypeScript only)
- ❌ Global CSS outside of globals.css
- ❌ Hardcoded API URLs
- ❌ Client-side JWT token storage in localStorage
- ❌ Any component over 200 lines
- ❌ Copy-paste code instead of creating reusable components
- ❌ Skip error handling for API calls
- ❌ Missing loading states for async operations
- ❌ Non-semantic HTML elements

### Performance Don'ts
- ❌ Import entire libraries (import only what you need)
- ❌ Large images without optimization
- ❌ Synchronous operations in render loops
- ❌ Memory leaks in useEffect
- ❌ Unnecessary re-renders
- ❌ Bundle large dependencies unnecessarily

## ✅ Success Metrics

You know the codebase is healthy when:
- **Zero TypeScript errors** - All code properly typed
- **Fast loading times** - < 3s initial page load
- **Mobile responsiveness** - Works perfectly on all device sizes
- **Accessibility score** - 100% Lighthouse accessibility score
- **Consistent patterns** - Same approach used everywhere
- **Easy debugging** - Clear component and function names
- **Maintainable code** - New developers can contribute quickly

## 🔧 Tools and Enforcement

### Automated Checks
- **ESLint** - Code quality and consistency
- **TypeScript** - Type safety
- **Prettier** - Code formatting
- **Lighthouse** - Performance and accessibility
- **Next.js Build** - Bundle optimization warnings

### Pre-commit Hooks
- Lint all staged files
- Type check all code
- Format with Prettier
- Check for security issues

---

**Remember**: These rules exist to make development faster and more enjoyable. When in doubt, follow the patterns established in existing components. 🎯

*Consistency enables velocity. Great rules enable great code.*