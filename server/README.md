# SyntaxMem Server

**Simple, Uniform, Consistent** Python serverless functions for the SyntaxMem platform.

## 🎯 Overview

The SyntaxMem server consists of modular Python Flask functions that provide secure, scalable backend services for coding practice through memory and pattern recognition.

### Core Philosophy
*Simple does not mean "not good" - it means choosing elegant solutions over complex ones.*

Built server-last, only what client actually needs. Each service is designed for:
- **Serverless deployment** - Independent, scalable functions
- **Production security** - JWT authentication and input validation
- **Consistent patterns** - Same structure across all services
- **Comprehensive testing** - Modular test suites for reliability

## 🏗️ Architecture

```
server/
├── auth/                    # Authentication service (Port 8081)
│   ├── main.py             # Google OAuth + JWT token management
│   ├── README.md           # 15 Sacred Laws for authentication
│   └── requirements.txt    # Python dependencies
├── snippets/               # Code snippet service (Port 8083)
│   ├── main.py            # Personal & official snippet management
│   ├── README.md          # 20 Sacred Laws for snippet management
│   └── requirements.txt   # Python dependencies
├── practice/              # Practice session service (Port 8082)
│   └── main.py           # Interactive coding exercises (coming soon)
├── shared/                # Common utilities
│   ├── auth_utils.py     # JWT token management
│   ├── database.py       # MongoDB connection & collections
│   ├── response_utils.py # Consistent API responses
│   └── README.md         # Utility documentation
├── schemas/               # Data validation
│   ├── personal_snippets.py  # Personal snippet validation
│   ├── official_snippets.py  # Official snippet validation
│   ├── users.py              # User data validation
│   └── README.md             # Schema patterns & rules
└── tests/                 # Comprehensive test suite
    ├── auth/             # 10 authentication tests
    ├── snippets/         # 7 snippet service tests
    ├── run_all_tests.sh  # Master test runner
    └── README.md         # Testing framework documentation
```

## 🚀 Services Status

### ✅ **Production Ready**

**Auth Service** (Port 8081)
- Google OAuth integration with NextAuth.js
- JWT access and refresh token management
- User profile creation and updates
- Session control (logout, logout-all)
- Comprehensive security validation
- **Documentation**: `/auth/README.md`
- **Tests**: 10 comprehensive test files

**Snippets Service** (Port 8083)
- Personal snippet CRUD operations with ownership verification
- Official snippet browsing and filtering
- Advanced search by language, difficulty, tags, content
- Schema validation for data integrity
- **Documentation**: `/snippets/README.md`
- **Tests**: 7 comprehensive test files

### 🚧 **In Development**

**Practice Service** (Port 8082)
- Interactive masked code completion exercises
- Scoring and progress tracking
- Session management and analytics

**Leaderboard Service** (Port 8084)
- User rankings and achievements
- Performance analytics and statistics

**Forum Service** (Port 8085)
- Community discussions and knowledge sharing
- Moderation and content management

## 🔧 Development Setup

### Prerequisites
```bash
Python 3.9+
MongoDB instance
Google OAuth credentials
```

### Environment Setup
Create `.env` file in server root:
```bash
# Database
MONGODB_URI=mongodb://localhost:27017
DATABASE_NAME=syntaxmem

# Authentication
JWT_SECRET=your-super-secure-jwt-secret
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# CORS
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
```

### Service Development
```bash
# Install dependencies for each service
cd auth && pip install -r requirements.txt
cd snippets && pip install -r requirements.txt

# Run individual services
cd auth && python main.py         # Port 8081
cd snippets && python main.py     # Port 8083
cd practice && python main.py     # Port 8082
```

### Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

## 📋 API Documentation

Each service maintains comprehensive API documentation with rules and examples:

- **Auth API**: `/auth/README.md` - 15 Sacred Laws for authentication
- **Snippets API**: `/snippets/README.md` - 20 Sacred Laws for snippet management
- **Shared Utilities**: `/shared/README.md` - Database, auth, and response utilities
- **Schema Validation**: `/schemas/README.md` - Data validation patterns
- **Testing Guide**: `/tests/README.md` - Modular testing framework

### Future Documentation
- **Practice API**: `/practice/README.md` (coming soon)
- **Leaderboard API**: `/leaderboard/README.md` (coming soon)
- **Forum API**: `/forum/README.md` (coming soon)

## 🧪 Testing

### Comprehensive Test Suite
- **17 total test files** across auth and snippets modules
- **Modular structure** - one test per file for focused testing
- **Independent execution** - tests can run individually or as modules
- **Production coverage** - authentication, CRUD, security, validation

### Run All Tests
```bash
cd tests
./run_all_tests.sh    # Runs auth + snippets modules
```

### Run Individual Module Tests
```bash
cd tests/auth
./run_auth_tests.sh           # 10 auth tests

cd tests/snippets
./run_snippets_tests.sh       # 7 snippets tests
```

### Run Individual Tests
```bash
cd tests/auth
python test_token_refresh.py

cd tests/snippets
python test_personal_snippet_create.py
```

### Test Coverage
- **Authentication flow** - Login, register, token refresh, logout
- **Security validation** - JWT verification, input sanitization
- **CRUD operations** - Create, read, update, delete snippets
- **Data integrity** - Schema validation and normalization
- **Error handling** - Comprehensive error scenarios
- **Performance** - Response time and load testing

## 🔐 Security Features

### Authentication & Authorization
- **Google OAuth 2.0** - Secure third-party authentication
- **JWT Tokens** - Stateless authentication with configurable expiry
- **Session Management** - Multi-device session control
- **Input Validation** - Comprehensive data sanitization
- **CORS Protection** - Configurable origin restrictions

### Data Protection
- **Schema Validation** - Strict data validation before database operations
- **SQL Injection Prevention** - MongoDB parameterized queries
- **XSS Protection** - Input sanitization and output encoding
- **Rate Limiting** - API request throttling (planned)
- **Audit Logging** - Security event tracking (planned)

## 📊 Performance & Monitoring

### Performance Targets
- **Response Time** - < 200ms for API endpoints
- **Throughput** - 1000+ requests/second per service
- **Availability** - 99.9% uptime target
- **Database** - Optimized queries with proper indexing

### Monitoring (Planned)
- **Health Checks** - `/health` endpoint for each service
- **Metrics Collection** - Request/response time tracking
- **Error Tracking** - Centralized error logging
- **Performance Analytics** - Service performance dashboards

## 🚀 Deployment

### Serverless Deployment
Each service is designed for independent serverless deployment:

**Recommended Platforms:**
- **AWS Lambda** - Automatic scaling, pay-per-request
- **Vercel Functions** - Seamless integration with frontend
- **Google Cloud Functions** - Google OAuth integration benefits
- **Azure Functions** - Enterprise deployment option

### Docker Deployment
```bash
# Build individual service containers
docker build -t syntaxmem-auth ./auth
docker build -t syntaxmem-snippets ./snippets

# Run with docker-compose
docker-compose up -d
```

### Production Checklist
- [ ] Environment variables secured
- [ ] MongoDB connection optimized for production
- [ ] Google OAuth configured for production domain
- [ ] CORS origins updated for production
- [ ] Rate limiting implemented
- [ ] Monitoring and logging configured
- [ ] SSL/TLS certificates installed
- [ ] Database backups automated

## 📈 Scaling Strategy

### Horizontal Scaling
- **Stateless Services** - No server-side session storage
- **Independent Functions** - Services can scale independently
- **Database Optimization** - Connection pooling and indexing
- **CDN Integration** - Static asset optimization

### Performance Optimization
- **Caching Layer** - Redis for frequent data (planned)
- **Database Indexing** - Optimized queries for common operations
- **Async Processing** - Background tasks for heavy operations
- **Connection Pooling** - Efficient database connections

## 🤝 Contributing

### Development Workflow
1. Follow existing service patterns in `/auth` and `/snippets`
2. Implement comprehensive error handling and validation
3. Add corresponding tests following modular test patterns
4. Update service README with Sacred Laws
5. Ensure all tests pass before submitting

### Code Standards
- **Python 3.9+** - Modern Python features and syntax
- **Flask** - Lightweight web framework for all services
- **PyMongo** - MongoDB driver for database operations
- **Async/Await** - Use async patterns for database operations
- **Type Hints** - Include type annotations for better code clarity

### Sacred Laws Philosophy
Each service maintains its own set of Sacred Laws (rules that must never be broken):
- **Auth Service**: 15 Sacred Laws covering security and token management
- **Snippets Service**: 20 Sacred Laws covering data integrity and ownership
- **Shared Utilities**: Consistent patterns across all services

---

**Remember**: Keep services simple, secure, and scalable. Each function should do one thing exceptionally well. 🎯

*Simple architecture enables complex features. Complex architecture creates simple bugs.*