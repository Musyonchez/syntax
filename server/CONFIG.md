# SyntaxMem Server Configuration

This document explains how to configure the SyntaxMem server using environment variables.

## Environment Setup

### 1. Create Environment File

Copy the example environment file and customize it:

```bash
cp .env.example .env
```

### 2. Required Configuration

Edit `.env` file with your actual values:

```bash
# Required Variables
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
DATABASE_NAME=syntaxmem
JWT_SECRET=your-super-secret-jwt-key-minimum-32-characters-long
```

### 3. Optional Configuration

```bash
# JWT Settings
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=720

# CORS Settings
ALLOWED_ORIGINS=https://syntaxmem.dev,http://localhost:3000

# Google OAuth (for reference)
GOOGLE_CLIENT_ID=your-google-oauth-client-id
GOOGLE_CLIENT_SECRET=your-google-oauth-client-secret

# Function Settings
FUNCTION_REGION=us-central1
FUNCTION_MEMORY=512MB
FUNCTION_TIMEOUT=540

# Environment
NODE_ENV=production
LOG_LEVEL=info

# Admin
ADMIN_EMAIL=your-admin-email@example.com
```

## Configuration Reference

### MongoDB Configuration

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `MONGODB_URI` | ✅ | MongoDB connection string | `mongodb+srv://user:pass@cluster.net/` |
| `DATABASE_NAME` | ✅ | Database name | `syntaxmem` |

### Security Configuration

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `JWT_SECRET` | ✅ | JWT signing secret (min 32 chars) | None |
| `JWT_ALGORITHM` | ❌ | JWT algorithm | `HS256` |
| `JWT_EXPIRATION_HOURS` | ❌ | Token expiration hours | `720` (30 days) |

### CORS Configuration

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `ALLOWED_ORIGINS` | ❌ | Comma-separated allowed origins | `http://localhost:3000` |

### Function Configuration

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `FUNCTION_REGION` | ❌ | Google Cloud region | `us-central1` |
| `FUNCTION_MEMORY` | ❌ | Function memory allocation | `512MB` |
| `FUNCTION_TIMEOUT` | ❌ | Function timeout seconds | `540` |

## Local Development

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables

```bash
# Option 1: Use .env file (recommended)
cp .env.example .env
# Edit .env with your values

# Option 2: Export variables
export MONGODB_URI="mongodb+srv://..."
export JWT_SECRET="your-secret-key"
```

### 3. Test Functions Locally

```bash
# Test auth function
cd functions/auth
functions-framework --target=main --port=8080

# Test in another terminal
curl -X POST http://localhost:8080/health
```

## Production Deployment

### 1. Validate Configuration

```bash
./deploy.sh validate
```

### 2. Deploy All Functions

```bash
./deploy.sh
```

### 3. Deploy Single Function

```bash
./deploy.sh single auth-verify auth
```

## Security Best Practices

### 1. JWT Secret

- **Minimum 32 characters** long
- Use a cryptographically secure random string
- **Never commit to version control**

```bash
# Generate secure JWT secret
openssl rand -base64 32
```

### 2. MongoDB URI

- Use **strong passwords**
- **Restrict IP access** in MongoDB Atlas
- Use **environment-specific databases**

### 3. CORS Origins

- **Never use wildcards** (`*`) in production
- List **exact domains** only
- Include protocol (`https://` not just domain)

## Environment-Specific Configurations

### Development

```bash
NODE_ENV=development
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
LOG_LEVEL=debug
```

### Staging

```bash
NODE_ENV=staging
ALLOWED_ORIGINS=https://staging.syntaxmem.dev
LOG_LEVEL=info
```

### Production

```bash
NODE_ENV=production
ALLOWED_ORIGINS=https://syntaxmem.dev
LOG_LEVEL=warn
```

## Troubleshooting

### Configuration Validation Errors

```bash
# Check configuration
./deploy.sh validate

# Common issues:
# - Missing required variables
# - JWT secret too short
# - Invalid MongoDB URI format
```

### Function Deployment Errors

```bash
# Check logs
gcloud functions logs read FUNCTION_NAME --region=us-central1

# Test locally first
cd functions/auth
python -c "from shared.config import config; config.validate()"
```

### Database Connection Issues

```bash
# Test MongoDB connection
python -c "
from shared.database import get_database
import asyncio
asyncio.run(get_database())
"
```

## Configuration Validation

The server automatically validates configuration on startup:

- ✅ Required variables are present
- ✅ JWT secret is sufficiently long
- ✅ MongoDB URI format is valid
- ❌ Fails fast with clear error messages

Example validation error:
```
ValueError: Missing required environment variables: JWT_SECRET, MONGODB_URI
```

## File Structure

```
server/
├── .env                 # Your configuration (never commit)
├── .env.example         # Template file
├── .gitignore          # Excludes .env files
├── CONFIG.md           # This documentation
└── shared/
    └── config.py       # Configuration management
```

---

**Important**: Never commit `.env` files to version control. The `.gitignore` file is configured to exclude them automatically.