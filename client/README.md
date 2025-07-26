# SyntaxMem Client

SyntaxMem client application built with Next.js 15, React 19, and TypeScript. An interactive coding practice platform where users complete masked code snippets to improve programming skills.

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ 
- npm/yarn/pnpm/bun
- Backend APIs running (see server setup)

### Development Setup

1. **Install dependencies:**
```bash
npm install
```

2. **Environment configuration:**
```bash
cp .env.example .env.local
# Configure API URLs and auth credentials
```

3. **Start development server:**
```bash
npm run dev
```

4. **Open application:**
Open [http://localhost:3000](http://localhost:3000) with your browser.

## 🔗 Backend APIs

The client connects to these backend services:

- **Auth API**: `http://localhost:8081` - Authentication & user management
- **Snippets API**: `http://localhost:8082` - Code snippet management  
- **Practice API**: `http://localhost:8083` - Practice sessions & progress
- **Leaderboard API**: `http://localhost:8084` - Rankings & statistics
- **Forum API**: `http://localhost:8085` - Community discussions

## 🎯 Key Features

- **Google OAuth Authentication** with NextAuth.js v5
- **Code Masking Practice** with CodeMirror 6
- **Real-time Progress Tracking** 
- **Community Leaderboards**
- **Dark/Light Theme Support**
- **Responsive Design** with Tailwind CSS

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
