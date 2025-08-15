# SyntaxMem

A simple, elegant code practice platform built with Next.js 15. Practice coding through interactive masked code completion exercises.

## 🎯 Philosophy

**Simple, Uniform, Consistent** - Every feature follows this core principle for maintainable, predictable code.

## ⚡ Quick Start

```bash
# Install dependencies
npm install

# Set up environment variables
cp .env.example .env.local
# Edit .env.local with your MongoDB Atlas URL and Google OAuth credentials

# Start development server
npm run dev
```

Visit [http://localhost:3000](http://localhost:3000) to see the app.

## 🏗️ Architecture

**Unified Next.js App** - Single codebase with API routes replacing separate backend services.

```
syntax/
├── app/                 # Next.js 15 App Router
│   ├── (auth)/         # Authentication pages
│   ├── dashboard/      # User dashboard
│   ├── practice/       # Practice sessions
│   ├── snippets/       # Snippet management
│   └── api/            # Backend API routes
├── components/         # Reusable components
├── lib/               # Utilities & config
└── types/             # TypeScript definitions
```

## 🚀 Features

### ✅ Currently Available
- **Premium Landing Page** - Professional SaaS-grade design with modern UI/UX
- **Responsive Design** - Mobile-first approach with glassmorphism effects
- **Interactive Components** - Smooth animations and micro-interactions
- **Modern Navigation** - Sticky navbar with functional mobile menu
- **Comprehensive Footer** - Social proof, newsletter, and complete site navigation

### 🚧 Coming Soon
- **Google OAuth Authentication** - Secure user management
- **Interactive Practice Sessions** - Masked code completion exercises
- **Snippet Management** - Create, edit, and organize code snippets
- **Progress Tracking** - Monitor learning progress and statistics
- **User Dashboard** - Personal analytics and session management

### 🛠️ Technical Stack
- **Next.js 15** - App Router with Server Components
- **TypeScript** - End-to-end type safety
- **Tailwind CSS** - Utility-first styling with custom design system
- **MongoDB Atlas** - Document-based data storage
- **NextAuth.js** - Secure authentication (planned)

## 🛠️ Development

### Commands

```bash
npm run dev          # Development server
npm run build        # Production build
npm run start        # Start production server
npm run lint         # Code linting
npm run type-check   # TypeScript validation
```

### Environment Variables

```bash
# Authentication
NEXTAUTH_SECRET=generate-with-openssl-rand-base64-32
NEXTAUTH_URL=http://localhost:3000
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# Database (MongoDB Atlas)
MONGODB_URI=your-mongodb-atlas-connection-string
```

## 📝 Development Guidelines

1. **Simple, Uniform, Consistent** - Core principle for all decisions
2. **Design System First** - Follow established color palette and component patterns
3. **Type Everything** - No `any` types, strict TypeScript
4. **Server First** - Default to Server Components, use Client Components only when needed
5. **API Routes** - Use Next.js API routes for all backend functionality
6. **Mobile-First** - Responsive design with Tailwind CSS
7. **Performance** - Optimize for speed and user experience

## 🎨 Design System

### Color Palette
- **Primary**: Blue to Purple gradients (#3B82F6 to #8B5CF6)
- **Neutrals**: Gray scale for text and backgrounds
- **Accents**: Green for success, appropriate colors for warnings/errors

### Component Standards
- **Glassmorphism**: Backdrop blur effects with transparency
- **Animations**: Subtle hover effects and smooth transitions
- **Typography**: Consistent font sizes and spacing
- **Spacing**: Unified padding/margin scale
- **Buttons**: Gradient styles with hover transforms

## 🧪 Testing

```bash
# Run tests (when implemented)
npm test
```

## 🚀 Deployment

The app is designed for easy deployment on platforms like Vercel:

```bash
# Build for production
npm run build

# Deploy (example with Vercel)
vercel deploy
```

## 📖 Project Structure

- **`app/`** - Next.js App Router pages and API routes (landing page complete)
- **`components/layout/`** - Navigation and footer components (premium design)
- **`lib/`** - Utility functions, database config, authentication
- **`types/`** - TypeScript type definitions
- **`public/`** - Static assets including logo and icons

## 🚀 Current Status

### ✅ Completed
- **Landing Page**: Full-screen hero, features, how-it-works, and CTA sections
- **Navigation**: Sticky navbar with mobile menu and glassmorphism
- **Footer**: Comprehensive footer with social proof and newsletter
- **Design System**: Established color palette, typography, and component standards
- **Environment**: MongoDB Atlas and Google OAuth credentials configured

### 🚧 In Progress
- **Authentication System**: NextAuth.js integration with Google OAuth

### 📋 Next Steps
1. Implement authentication pages (login, signup)
2. Create protected route middleware
3. Build user dashboard
4. Develop snippet management system
5. Create practice session functionality

## 🤝 Contributing

1. Follow the "Simple, Uniform, Consistent" principle
2. Use TypeScript strictly (no `any` types)
3. Follow existing patterns and conventions
4. Test your changes before submitting

## 📚 Learn More

- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS](https://tailwindcss.com)
- [NextAuth.js](https://next-auth.js.org)
- [MongoDB](https://www.mongodb.com)

## 📄 License

MIT License - see the [LICENSE](LICENSE) file for details.

---

**Built with ❤️ and the principle of Simple, Uniform, Consistent**
