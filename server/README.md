# SyntaxMem Server - Simple, Uniform, Consistent

Python serverless functions following elegant simplicity principles.

*Simple does not mean "not good" - it means choosing elegant solutions over complex ones.*

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

**Principle**: Simple = elegant, maintainable, excellent serverless functions.