# SyntaxMem Client

**Simple, Uniform, Consistent** Next.js frontend for the SyntaxMem platform.

## 🎯 Overview

The SyntaxMem client is a modern React application built with Next.js 15, providing an intuitive interface for coding practice through memory and pattern recognition.

### Key Features
- **🔐 Authentication** - Google OAuth integration with NextAuth.js
- **📝 Code Snippets** - Browse and manage personal/official code snippets
- **🎯 Practice Sessions** - Interactive masked code completion exercises
- **🏆 Leaderboard** - User rankings and achievement tracking
- **💬 Community Forum** - Developer discussions and knowledge sharing
- **📊 Dashboard** - Comprehensive user progress and statistics

## 🏗️ Architecture

```
client/
├── src/
│   ├── app/                 # Next.js App Router pages
│   │   ├── dashboard/       # User dashboard and stats
│   │   ├── login/           # Authentication pages
│   │   ├── practice/        # Interactive practice sessions
│   │   ├── snippets/        # Code snippet management
│   │   ├── leaderboard/     # Rankings and achievements
│   │   └── forum/           # Community discussions
│   ├── components/          # Reusable React components
│   │   ├── auth/           # Authentication components
│   │   ├── common/         # Shared UI components
│   │   ├── layout/         # Navigation and footer
│   │   └── practice/       # Practice session components
│   ├── lib/                # Utility libraries
│   │   ├── auth.ts         # NextAuth configuration
│   │   └── utils.ts        # Helper functions
│   └── types/              # TypeScript type definitions
├── public/                 # Static assets
└── docs/                   # Component documentation
```

## 🚀 Technology Stack

### Core Framework
- **Next.js 15.4.4** - React framework with App Router
- **React 19** - UI library with latest features
- **TypeScript** - Type safety and developer experience

### Authentication
- **NextAuth.js** - Authentication library
- **Google OAuth** - Secure sign-in integration
- **JWT Tokens** - Session management

### Styling & UI
- **Tailwind CSS** - Utility-first CSS framework
- **Shadcn/UI** - High-quality component library
- **Radix UI** - Headless component primitives
- **Lucide Icons** - Beautiful SVG icons

### Development Tools
- **ESLint** - Code linting and formatting
- **TypeScript** - Static type checking
- **PostCSS** - CSS processing
- **Next.js DevTools** - Development optimization

## 🔧 Development Setup

### Prerequisites
```bash
Node.js 18+ 
npm/yarn/pnpm
```

### Installation
```bash
# Clone repository
git clone <repository-url>
cd syntaxmem/client

# Install dependencies
npm install

# Start development server
npm run dev
```

### Environment Variables
Create `.env.local` file:
```bash
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-nextauth-secret
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# API endpoints
NEXT_PUBLIC_AUTH_API=http://localhost:8081
NEXT_PUBLIC_SNIPPETS_API=http://localhost:8083
NEXT_PUBLIC_PRACTICE_API=http://localhost:8082
```

## 📋 Available Scripts

```bash
# Development
npm run dev          # Start development server
npm run build        # Build for production
npm run start        # Start production server

# Code Quality
npm run lint         # Run ESLint linting
npm run lint:fix     # Fix linting issues
npm run type-check   # TypeScript type checking

# Testing
npm run test         # Run test suite (future)
npm run test:e2e     # End-to-end tests (future)
```

## 🎨 Component Structure

### Layout Components
- **Navbar** - Main navigation with auth state
- **Footer** - Site footer with links
- **MobileMenu** - Responsive mobile navigation

### Feature Components
- **Dashboard** - User stats and quick actions
- **Practice Session** - Interactive coding exercises
- **Code Editor** - Syntax-highlighted code input
- **Snippet Browser** - Personal and official snippet management
- **User Dropdown** - Profile and logout actions

### UI Components
- **Button** - Customizable button component
- **Card** - Content container with variants
- **Dialog** - Modal dialogs and overlays
- **Input** - Form input components
- **Avatar** - User profile images

## 🔐 Authentication Flow

### Login Process
```typescript
// Google OAuth with NextAuth.js
const session = await auth()
if (!session?.user) {
  redirect('/login')
}

// JWT token from backend
const token = session.user.backendToken
```

### Protected Routes
All authenticated pages use server-side auth check:
```typescript
export default async function ProtectedPage() {
  const session = await auth()
  if (!session?.user) {
    redirect('/login')
  }
  // Render protected content
}
```

## 📱 Responsive Design

### Breakpoints
- **Mobile**: `< 768px` - Single column layout
- **Tablet**: `768px - 1024px` - Adaptive layouts
- **Desktop**: `> 1024px` - Full multi-column layouts

### Design Principles
- **Mobile-first** - Start with mobile design
- **Progressive enhancement** - Add features for larger screens
- **Touch-friendly** - Appropriate touch targets
- **Accessible** - WCAG 2.1 compliance

## 🎯 Feature Status

### ✅ **Production Ready**
- **Authentication** - Google OAuth with NextAuth.js
- **Dashboard** - User stats and navigation
- **Navigation** - Responsive navbar and mobile menu
- **Theme Support** - Light/dark mode toggle
- **Landing Page** - Marketing and feature showcase

### 🚧 **In Development**
- **Practice Sessions** - Interactive coding exercises
- **Snippet Management** - CRUD operations for code snippets
- **Leaderboard** - User rankings and achievements
- **Forum** - Community discussions
- **Profile Editing** - User profile management

### 📋 **Planned Features**
- **Offline Support** - Progressive Web App features
- **Push Notifications** - Achievement and reminder notifications
- **Advanced Analytics** - Detailed progress tracking
- **Social Features** - Friend connections and sharing
- **Mobile App** - React Native companion app

## 🚀 Deployment

### Build Process
```bash
# Production build
npm run build

# Start production server
npm run start
```

### Deployment Targets
- **Vercel** - Recommended (zero-config)
- **Netlify** - Static site deployment
- **AWS Amplify** - Full-stack deployment
- **Docker** - Containerized deployment

### Production Checklist
- [ ] Environment variables configured
- [ ] API endpoints updated for production
- [ ] Google OAuth configured for production domain
- [ ] Build optimization verified
- [ ] Performance metrics acceptable
- [ ] SEO metadata configured
- [ ] Error tracking configured

## 📊 Performance

### Core Web Vitals Targets
- **LCP** < 2.5s - Largest Contentful Paint
- **FID** < 100ms - First Input Delay  
- **CLS** < 0.1 - Cumulative Layout Shift

### Optimization Features
- **Image Optimization** - Next.js automatic image optimization
- **Code Splitting** - Automatic route-based splitting
- **Tree Shaking** - Remove unused JavaScript
- **Minification** - Compress CSS and JavaScript
- **Caching** - Efficient browser and CDN caching

## 🤝 Contributing

### Development Workflow
1. Follow existing component patterns
2. Use TypeScript for all new code
3. Follow Tailwind CSS conventions
4. Test components across breakpoints
5. Ensure accessibility standards
6. Update documentation

### Code Style
- **ESLint** configuration enforced
- **Prettier** for consistent formatting
- **TypeScript** strict mode enabled
- **Component naming** - PascalCase for components
- **File naming** - kebab-case for files

---

**Remember**: Keep components simple, reusable, and accessible. The frontend should provide an intuitive experience while maintaining performance. 🎯

*Great user experience starts with great developer experience.*