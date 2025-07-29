# SyntaxMem - Simple, Uniform, Consistent

Interactive coding practice platform with masked code completion.

## Architecture

**Principles**: Simple, Uniform, Consistent

- **Client**: Next.js 15 + TypeScript + Tailwind
- **Server**: Python serverless functions (Google Cloud)  
- **Database**: MongoDB Atlas
- **Auth**: Google OAuth + JWT

## Structure

```
syntax/
├── client/     # Next.js frontend
├── server/     # Python serverless backend  
└── README.md
```

## Development

```bash
# Client
cd client && npm run dev

# Server functions
cd server/auth && python main.py
cd server/practice && python main.py
cd server/snippets && python main.py
```

Simple. Uniform. Consistent.