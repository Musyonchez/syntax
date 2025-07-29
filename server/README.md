# Server Shell

Python serverless functions following simple, uniform, consistent principles.

## Core Functions
- `/auth` - Google OAuth + JWT (port 8081)
- `/practice` - Practice sessions + scoring (port 8082)  
- `/snippets` - Code management (port 8083)

## Structure
```
server/
├── auth/         # Authentication function
├── practice/     # Practice sessions  
├── snippets/     # Code snippets
└── shared/       # Common utilities
```

## Development
```bash
cd auth && python main.py
cd practice && python main.py  
cd snippets && python main.py
```

Built server-last, only what client actually needs.