# SyntaxMem

An interactive coding practice platform where users complete masked code snippets to improve programming skills.

## Overview

SyntaxMem provides a "fill-in-the-blanks" approach to learning programming. Users practice with real code snippets where keywords, functions, and variables are masked based on difficulty level.

## Architecture

- **Frontend**: Next.js 15 + React 19 + TypeScript + Tailwind CSS
- **Backend**: Python serverless functions (Google Cloud Functions)
- **Database**: MongoDB Atlas
- **Authentication**: NextAuth.js v5 with Google OAuth

## Features

- **Practice Sessions**: Interactive masked code completion
- **Real-time Scoring**: Immediate feedback with similarity matching
- **Progress Tracking**: User statistics and session history
- **Leaderboards**: Global and weekly rankings
- **Multiple Languages**: Python and JavaScript support
- **Adaptive Difficulty**: 10-level difficulty system

## Quick Start

### Prerequisites
- Node.js 18+
- Python 3.9+
- MongoDB connection string
- Google OAuth credentials

### Client Setup
```bash
cd client
npm install
cp .env.example .env.local
# Add your environment variables
npm run dev
```

### Server Setup
```bash
cd server/functions/auth
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m flask --app main run --host=0.0.0.0 --port=8081 --debug
```

## Environment Variables

### Client (.env.local)
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

### Server (.env)
```
MONGODB_URI=your-mongodb-connection-string
JWT_SECRET=your-jwt-secret
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
CORS_ORIGINS=http://localhost:3000,http://localhost:3001,https://syntaxmem.com
```

## Development

### Running All Services
```bash
# Terminal 1 - Client
cd client && npm run dev

# Terminal 2 - Auth Service
cd server/functions/auth && source venv/bin/activate && python -m flask --app main run --host=0.0.0.0 --port=8081 --debug

# Terminal 3 - Snippets Service
cd server/functions/snippets && source venv/bin/activate && python -m flask --app main run --host=0.0.0.0 --port=8082 --debug

# Terminal 4 - Practice Service
cd server/functions/practice && source venv/bin/activate && python -m flask --app main run --host=0.0.0.0 --port=8083 --debug

# Terminal 5 - Leaderboard Service
cd server/functions/leaderboard && source venv/bin/activate && python -m flask --app main run --host=0.0.0.0 --port=8084 --debug

# Terminal 6 - Forum Service
cd server/functions/forum && source venv/bin/activate && python -m flask --app main run --host=0.0.0.0 --port=8085 --debug
```

## API Endpoints

- **Auth**: `http://localhost:8081` - User authentication and JWT management
- **Snippets**: `http://localhost:8082` - Code snippet management and masking
- **Practice**: `http://localhost:8083` - Practice sessions and scoring
- **Leaderboard**: `http://localhost:8084` - Rankings and statistics
- **Forum**: `http://localhost:8085` - Community discussions

## Project Structure

```
syntax/
├── client/          # Next.js frontend application
├── server/          # Python serverless backend
│   ├── functions/   # Individual Cloud Functions
│   └── shared/      # Shared utilities and middleware
└── README.md
```

## Contributing

1. Follow the established code patterns
2. Use TypeScript strict mode (no `any` types)
3. Test all changes with `npm run build` and `npm run lint`
4. Ensure all server functions start properly
5. Maintain consistent code formatting

## License

MIT License - see LICENSE file for details.