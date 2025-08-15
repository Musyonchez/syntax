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
# Edit .env.local with your values

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

### Core Features
- **Google OAuth Authentication** - Secure user management
- **Interactive Practice Sessions** - Masked code completion exercises
- **Snippet Management** - Create, edit, and organize code snippets
- **Progress Tracking** - Monitor learning progress and statistics

### Technical Features
- **Next.js 15** - App Router with Server Components
- **TypeScript** - End-to-end type safety
- **Tailwind CSS** - Utility-first styling
- **MongoDB** - Document-based data storage
- **NextAuth.js** - Secure authentication

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
NEXTAUTH_SECRET=your-secret-here
NEXTAUTH_URL=http://localhost:3000
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# Database
MONGODB_URI=mongodb://localhost:27017/syntaxmem
```

## 📝 Development Guidelines

1. **Keep it Simple** - Choose the most straightforward solution
2. **Follow Patterns** - Use established conventions throughout
3. **Type Everything** - No `any` types, strict TypeScript
4. **Server First** - Default to Server Components, use Client Components only when needed
5. **API Routes** - Use Next.js API routes for all backend functionality

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

- **`app/`** - Next.js App Router pages and API routes
- **`components/`** - Reusable React components
- **`lib/`** - Utility functions, database config, authentication
- **`types/`** - TypeScript type definitions
- **`public/`** - Static assets

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
