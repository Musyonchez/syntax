# SyntaxMem Client

Next.js 15 frontend application for the SyntaxMem coding practice platform.

## Features

- **Modern Stack**: Next.js 15 + React 19 + TypeScript + Tailwind CSS
- **Authentication**: NextAuth.js v5 with Google OAuth
- **Practice Interface**: CodeMirror integration with masked code completion
- **Real-time Scoring**: Immediate feedback and progress tracking
- **Responsive Design**: Mobile-first design with dark/light theme support
- **State Management**: Zustand + TanStack Query for optimal performance

## Development

### Prerequisites
- Node.js 18+
- npm or yarn

### Setup
```bash
# Install dependencies
npm install

# Copy environment file
cp .env.example .env.local

# Start development server
npm run dev
```

### Environment Variables (.env.local)
```
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-secret-key
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
NEXT_PUBLIC_AUTH_API_URL=http://localhost:8081
NEXT_PUBLIC_SNIPPETS_API_URL=http://localhost:8082
NEXT_PUBLIC_PRACTICE_API_URL=http://localhost:8083
NEXT_PUBLIC_LEADERBOARD_API_URL=http://localhost:8084
NEXT_PUBLIC_FORUM_API_URL=http://localhost:8085
```

### Scripts
```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run start        # Start production server
npm run lint         # Run ESLint
```

## Architecture

### Key Technologies
- **Next.js 15**: App Router, Server Components, optimized builds
- **React 19**: Latest React features with concurrent rendering
- **TypeScript**: Strict mode enabled, no `any` types allowed
- **Tailwind CSS v4**: Utility-first styling with design system
- **Shadcn/ui**: High-quality, accessible UI components
- **NextAuth.js v5**: Authentication with Google OAuth
- **TanStack Query**: Server state management and caching
- **Zustand**: Lightweight client state management
- **CodeMirror**: Advanced code editor with syntax highlighting

### Project Structure
```
src/
├── app/                 # Next.js App Router
│   ├── page.tsx        # Landing page
│   ├── practice/       # Practice interface
│   ├── dashboard/      # User dashboard
│   ├── auth/           # Authentication pages
│   └── api/            # API routes
├── components/
│   ├── ui/             # Base UI components (Shadcn/ui)
│   ├── layout/         # Navigation, footer
│   ├── auth/           # Authentication components
│   ├── practice/       # Practice session components
│   ├── home/           # Landing page sections
│   └── providers/      # Context providers
├── lib/
│   ├── api/            # API client functions
│   ├── auth/           # NextAuth configuration
│   └── utils.ts        # Utility functions
├── hooks/              # Custom React hooks
├── stores/             # Zustand state stores
└── types/              # TypeScript definitions
```

## Key Components

### Practice Interface
- **Practice Session**: Complete practice workflow management
- **Code Editor**: CodeMirror with syntax highlighting
- **Masked Code Editor**: Interactive fill-in-the-blanks interface
- **Timer**: Real-time session timing
- **Score Display**: Immediate feedback and results

### Authentication
- **Signin Form**: Google OAuth integration
- **Auth Provider**: Session management
- **Protected Routes**: Automatic redirection

### Layout
- **Navigation**: Responsive navigation with user menu
- **Theme Provider**: Dark/light mode support
- **Footer**: Site footer with links

## API Integration

The client communicates with 5 microservices:

- **Auth API** (8081): User authentication and JWT management
- **Snippets API** (8082): Code snippet management and masking
- **Practice API** (8083): Practice sessions and scoring
- **Leaderboard API** (8084): Rankings and statistics
- **Forum API** (8085): Community discussions

### API Client
```typescript
// Simplified API client with automatic JWT injection
import { practiceApi } from '@/lib/api/practice'

const session = await practiceApi.startSession({
  snippet_id: 'abc123',
  difficulty: 5
})
```

## Development Guidelines

### Code Standards
- Use TypeScript strict mode (no `any` types)
- Follow functional component patterns
- Prefer server components when possible
- Use proper error boundaries
- Implement proper loading states

### Component Patterns
```typescript
// Standard component structure
export function ComponentName() {
  // 1. Hooks and state
  const [state, setState] = useState()
  
  // 2. Event handlers
  const handleAction = () => {
    // Handle action
  }
  
  // 3. Effects
  useEffect(() => {
    // Side effects
  }, [])
  
  // 4. Render
  return (
    <div>
      {/* JSX */}
    </div>
  )
}
```

### Styling Guidelines
- Use Tailwind CSS utility classes
- Follow design system colors and spacing
- Use CSS transitions instead of heavy animation libraries
- Maintain responsive design principles

## Performance Optimizations

- **Code Splitting**: Automatic route-based splitting
- **Image Optimization**: Next.js Image component
- **Bundle Analysis**: Optimized dependencies
- **Caching**: TanStack Query for server state
- **SSR/SSG**: Static generation where appropriate

## Testing

```bash
# Run type checking
npm run build

# Run linting
npm run lint
```

## Deployment

The application is optimized for Vercel deployment:

```bash
# Build for production
npm run build

# Test production build locally
npm run start
```

## Contributing

1. Follow established patterns in existing components
2. Maintain TypeScript strict mode
3. Test changes with `npm run build` and `npm run lint`
4. Keep components focused and avoid over-engineering
5. Use CSS transitions instead of heavy animation libraries