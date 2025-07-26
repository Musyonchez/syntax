# SyntaxMem Server

Python serverless backend for the SyntaxMem coding practice platform, built with Flask and designed for Google Cloud Functions.

## Architecture

The backend consists of 5 independent microservices, each running on a separate port:

- **Auth Service** (8081): User authentication and JWT management
- **Snippets Service** (8082): Code snippet management and masking
- **Practice Service** (8083): Practice sessions and scoring
- **Leaderboard Service** (8084): Rankings and statistics
- **Forum Service** (8085): Community discussions

## Features

- **Microservices Architecture**: Independent, scalable services
- **MongoDB Integration**: Async Motor driver with aggregation pipelines
- **JWT Authentication**: Secure token-based authentication
- **Code Masking Engine**: Intelligent code masking using Pygments
- **Input Validation**: Comprehensive validation and sanitization
- **Structured Logging**: Production-ready logging across all services
- **CORS Support**: Environment-based origin configuration

## Development Setup

### Prerequisites
- Python 3.9+
- MongoDB connection string
- Google OAuth credentials

### Environment Variables (.env)
```
MONGODB_URI=your-mongodb-connection-string
DATABASE_NAME=syntaxmem
JWT_SECRET=your-jwt-secret-key
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
CORS_ORIGINS=http://localhost:3000,http://localhost:3001,https://syntaxmem.com
```

### Running Individual Services

Each service runs independently in its own virtual environment:

```bash
# Auth Service (Port 8081)
cd functions/auth
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m flask --app main run --host=0.0.0.0 --port=8081 --debug

# Snippets Service (Port 8082)
cd functions/snippets
source venv/bin/activate
python -m flask --app main run --host=0.0.0.0 --port=8082 --debug

# Practice Service (Port 8083)
cd functions/practice
source venv/bin/activate
python -m flask --app main run --host=0.0.0.0 --port=8083 --debug

# Leaderboard Service (Port 8084)
cd functions/leaderboard
source venv/bin/activate
python -m flask --app main run --host=0.0.0.0 --port=8084 --debug

# Forum Service (Port 8085)
cd functions/forum
source venv/bin/activate
python -m flask --app main run --host=0.0.0.0 --port=8085 --debug
```

## Service Details

### Auth Service (8081)
**Purpose**: User authentication and JWT management

**Key Endpoints**:
- `POST /google-auth` - Google OAuth authentication
- `POST /refresh` - Token refresh
- `GET /health` - Health check

**Features**:
- Google OAuth integration
- JWT token creation and validation
- User profile management
- Secure token refresh

### Snippets Service (8082)
**Purpose**: Code snippet management and masking

**Key Endpoints**:
- `GET /official` - Get official snippets
- `GET /personal` - Get user's personal snippets
- `POST /create` - Create new snippet
- `GET /{id}` - Get specific snippet
- `POST /{id}/mask` - Generate masked version
- `POST /submit` - Submit for review
- `GET /submissions` - Get user submissions

**Features**:
- Dual snippet system (official/personal)
- Intelligent code masking using Pygments
- Difficulty-based masking algorithm
- Snippet submission workflow

### Practice Service (8083)
**Purpose**: Practice sessions and scoring

**Key Endpoints**:
- `POST /start` - Start practice session
- `POST /submit` - Submit completed session
- `GET /stats` - Get practice statistics
- `GET /history` - Get practice history
- `GET /session/{id}` - Get session details

**Features**:
- Complete session management
- Advanced scoring algorithm with time bonuses
- Progress tracking and statistics
- Session history with filtering

### Leaderboard Service (8084)
**Purpose**: Rankings and user statistics

**Key Endpoints**:
- `GET /global` - Global leaderboard
- `GET /weekly` - Weekly leaderboard
- `GET /user/{id}/rank` - User's rank and stats

**Features**:
- Global and weekly rankings
- Language-specific leaderboards
- Complex MongoDB aggregation pipelines
- Accurate rank calculations

### Forum Service (8085)
**Purpose**: Community discussions

**Key Endpoints**:
- `GET /posts` - Get forum posts
- `POST /posts` - Create new post
- `GET /posts/{id}` - Get specific post with replies
- `POST /posts/{id}/replies` - Create reply
- `POST /posts/{id}/vote` - Vote on post
- `GET /categories` - Get available categories

**Features**:
- Threaded discussions
- Voting system
- Category organization
- Content moderation

## Shared Utilities

### Database (`shared/database.py`)
- Async MongoDB connections using Motor
- Collection getters for each service
- Connection pooling for serverless environments

### Authentication (`shared/auth_middleware.py`)
- JWT token verification
- Token creation and refresh
- Security validation

### Code Masking (`shared/masking.py`)
- Pygments-based tokenization
- Intelligent masking algorithm
- Difficulty-based token selection
- Answer validation with similarity scoring

### Utilities (`shared/utils.py`)
- Response formatting functions
- Input validation and sanitization
- Timestamp utilities
- Error handling helpers

### Configuration (`shared/config.py`)
- Environment variable management
- Configuration validation
- Development/production settings

## Database Schema

### Collections
- **users**: User profiles and statistics
- **snippets**: Code snippets (official and personal)
- **practice_sessions**: Practice session data
- **forum_posts**: Forum posts and replies

### Key Indexes
- Users: `googleId`, `email`
- Snippets: `type`, `language`, `difficulty`, `userId`
- Practice Sessions: `userId`, `snippetId`, `status`
- Forum Posts: `category`, `createdAt`, `votes`

## Development Guidelines

### Code Standards
```python
# Standard function structure
@app.route("/endpoint", methods=["POST"])
def function_name():
    try:
        # 1. Input validation
        data = request.get_json()
        if not data:
            return create_error_response("Invalid JSON data", 400)
        
        # 2. Authentication (if required)
        auth_header = request.headers.get("Authorization")
        user_data = verify_jwt_token_simple(token)
        
        # 3. Business logic
        result = await async_operation()
        
        # 4. Response
        return create_response(result, "Operation successful")
        
    except Exception as e:
        logger.error(f"Operation failed: {e}")
        return create_error_response("Operation failed", 500)
```

### Security Best Practices
- Always validate and sanitize input
- Use structured logging (no print statements)
- Implement proper error handling
- Validate JWT tokens on protected routes
- Use parameterized database queries
- Implement rate limiting where appropriate

### Performance Optimizations
- Use MongoDB aggregation pipelines
- Implement proper pagination
- Cache frequently accessed data
- Optimize database indexes
- Use async operations where possible

## Testing

Each service includes health check endpoints for monitoring:
```bash
curl http://localhost:8081/health
curl http://localhost:8082/health
curl http://localhost:8083/health
curl http://localhost:8084/health
curl http://localhost:8085/health
```

## Deployment

The services are designed for Google Cloud Functions deployment:

```bash
# Deploy individual function
gcloud functions deploy auth-service \
  --runtime python39 \
  --trigger-http \
  --allow-unauthenticated \
  --source functions/auth/
```

## Contributing

1. Follow the established patterns in existing functions
2. Use structured logging instead of print statements
3. Implement proper input validation and error handling
4. Test all endpoints before submitting changes
5. Maintain consistent response formats
6. Update shared utilities when adding common functionality