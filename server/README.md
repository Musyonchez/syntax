# SyntaxMem Server

**Simple, Uniform, Consistent** Python serverless functions for the SyntaxMem platform.

## 🎯 Overview

The SyntaxMem server consists of modular Python Flask functions that provide secure, scalable backend services for coding practice through memory and pattern recognition.

### Core Philosophy
*Simple does not mean "not good" - it means choosing elegant solutions over complex ones.*

Built server-last, only what client actually needs. Each service is designed for:
- **Serverless deployment** - Independent, scalable functions
- **Production security** - JWT authentication and comprehensive input validation
- **Consistent patterns** - Same structure across all services
- **Comprehensive testing** - Modular test suites with full coverage
- **Strict validation** - All schemas follow consistent type checking

## 🏗️ Architecture

```
server/
├── auth/                    # Authentication service (Port 8081) ✅ PRODUCTION READY
│   ├── main.py             # Google OAuth + JWT token management
│   ├── README.md           # Authentication documentation
│   └── requirements.txt    # Python dependencies
├── snippets/               # Code snippet service (Port 8083) ✅ PRODUCTION READY
│   ├── main.py            # Personal & official snippet management
│   ├── README.md          # Snippet management documentation
│   └── requirements.txt   # Python dependencies
├── practice/              # Practice session service (Port 8082) 🚧 PLANNED
│   └── main.py           # Interactive coding exercises (coming soon)
├── shared/                # Common utilities ✅ COMPLETE
│   ├── auth_utils.py     # JWT token management
│   ├── database.py       # MongoDB async connection & collections
│   ├── response_utils.py # Consistent API responses
│   └── README.md         # Utility documentation
├── schemas/               # Data validation ✅ COMPLETE
│   ├── personal_snippets.py  # Personal snippet validation (strict)
│   ├── official_snippets.py  # Official snippet validation (strict)
│   ├── users.py              # User data validation (strict)
│   ├── tokens.py             # Refresh token validation (strict)
│   ├── sessions.py           # Practice session validation (strict)
│   └── README.md             # Schema patterns & validation rules
└── tests/                 # Comprehensive test suite ✅ COMPLETE
    ├── auth/             # 6 authentication tests (all schemas covered)
    ├── snippets/         # 8 snippet service tests (comprehensive)
    ├── run_all_tests.sh  # Master test runner
    └── README.md         # Testing framework documentation
```

## 🚀 Services Status

### ✅ **Production Ready**

**Auth Service** (Port 8081) - **Phase 2 Complete**
- Google OAuth integration with role-based access control (admin detection)
- JWT access and refresh token management with automatic cleanup
- Multi-device session management (2-token limit per user)
- Complete logout functionality (single device + logout all devices)
- Comprehensive schema validation (users, tokens, sessions)
- **Admin Features**: Automatic admin detection for `musyonchez@gmail.com`
- **Security**: Token cleanup, session limits, strict validation
- **Documentation**: `/auth/README.md`
- **Tests**: 6 comprehensive test files covering all functionality

**Snippets Service** (Port 8083) - **Phase 2 Complete**  
- Personal snippet CRUD operations with ownership verification
- Official snippet management with admin-only creation
- Advanced filtering (language, difficulty, tags, search, combined filters)
- Comprehensive schema validation with strict type checking
- **Admin Features**: Admin-only official snippet creation
- **Public Access**: Official snippets browsable without authentication
- **Security**: Role-based access control, input validation
- **Documentation**: `/snippets/README.md`
- **Tests**: 8 comprehensive test files covering all functionality

### 🏗️ **Foundation Complete**

**Shared Utilities** - All services use common patterns
- **Database**: Async MongoDB with Motor driver for performance
- **Auth Utils**: JWT token management and verification
- **Response Utils**: Consistent API response format
- **Async/Sync Integration**: Proper event loop handling

**Schema Validation** - All schemas consistently strict
- **Type Validation**: Proper type checking before processing
- **Error Handling**: 400/422 responses instead of 500 crashes
- **Consistent Philosophy**: No silent defaults, throw validation errors
- **Full Coverage**: Users, tokens, sessions, personal snippets, official snippets

### 🚧 **Planned Phases**

**Phase 3: Core Features**
- **Practice Service** (Port 8082) - Interactive masked code completion
- **Scoring System** - Progress tracking and analytics

**Phase 4: Polish**
- **Enhanced Features** - Browse snippets, user stats
- **Admin Dashboard** - Content management interface

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

# Admin Configuration
ADMIN_EMAIL=your-admin-email@gmail.com

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
cd practice && python main.py     # Port 8082 (when implemented)
```

### Quick Start
```bash
# 1. Start MongoDB
mongod

# 2. Terminal 1: Auth service
cd server/auth && python main.py

# 3. Terminal 2: Snippets service  
cd server/snippets && python main.py

# 4. Terminal 3: Run tests
cd server/tests && ./run_all_tests.sh
```

## 📋 API Documentation

Each service maintains comprehensive API documentation:

- **Auth API**: `/auth/README.md` - Authentication, tokens, session management
- **Snippets API**: `/snippets/README.md` - Personal & official snippet management
- **Shared Utilities**: `/shared/README.md` - Database, auth, and response utilities
- **Schema Validation**: `/schemas/README.md` - Strict validation patterns
- **Testing Guide**: `/tests/README.md` - Comprehensive testing framework

## 🧪 Testing

### Comprehensive Test Suite
- **14 total test files** across auth and snippets modules
- **Modular structure** - focused testing with clear sequential naming
- **Independent execution** - tests can run individually or as suites
- **Complete coverage** - authentication, CRUD, security, validation, admin features

### Test Statistics
```
Auth Tests:     6 tests (all schemas + functionality)
Snippet Tests:  8 tests (comprehensive CRUD + admin features)
Total Coverage: Authentication, CRUD, Security, Validation, Admin Features
```

### Run All Tests
```bash
cd tests
./run_all_tests.sh    # Runs auth + snippets suites (14 tests total)
```

### Run Individual Module Tests
```bash
cd tests/auth
./run_auth_tests.sh           # 6 auth tests (users, tokens, sessions)

cd tests/snippets  
./run_snippets_tests.sh       # 8 snippets tests (personal + official)
```

### Run Individual Tests
```bash
cd tests/auth
python test_01_user_creation.py
python test_05_schema_validation.py
python test_06_session_schema.py

cd tests/snippets
python test_01_personal_create.py
python test_08_schema_validation.py
```

### Test Coverage Details
- **Authentication Flow**: User creation, token refresh, logout, logout-all
- **Schema Validation**: All 5 schemas with strict type checking
- **CRUD Operations**: Personal snippets with ownership verification
- **Admin Features**: Official snippet creation, role-based access
- **Security Validation**: JWT verification, input sanitization, type safety
- **Error Handling**: Comprehensive error scenarios with proper status codes

## 🔐 Security Features

### Authentication & Authorization
- **Google OAuth 2.0** - Secure third-party authentication
- **JWT Tokens** - Stateless authentication with automatic cleanup
- **Role-Based Access** - Admin detection and permissions
- **Session Management** - Multi-device control with 2-token limit
- **Input Validation** - Comprehensive data sanitization
- **CORS Protection** - Configurable origin restrictions

### Data Protection
- **Strict Schema Validation** - All schemas enforce type safety
- **Type Safety** - No silent type conversion, proper error responses
- **SQL Injection Prevention** - MongoDB parameterized queries
- **XSS Protection** - Input sanitization and validation
- **Admin Security** - Role-based endpoint protection
- **Data Integrity** - Consistent validation across all schemas

### Schema Security
All schemas now follow strict validation principles:
- **Type Validation**: Proper type checking before processing
- **Error Responses**: 400/422 instead of 500 crashes
- **No Silent Defaults**: Validation errors thrown for invalid data
- **Consistent Behavior**: Same validation philosophy across all schemas

## 📊 Current Status

### ✅ Completed (Phase 2)
- **Authentication System**: Production-ready with full test coverage
- **Snippet Management**: Complete CRUD with admin features
- **Schema Validation**: All schemas strictly validated
- **Test Suite**: Comprehensive coverage (14 tests)
- **Admin Features**: Role detection, official snippet management
- **Security**: Token cleanup, session limits, type safety

### 🎯 Success Metrics Achieved
- **Build Time**: Fast (under 30 seconds)
- **Code Quality**: Simple, uniform, consistent
- **Test Coverage**: 100% core functionality
- **Security**: Production-ready validation
- **Documentation**: Comprehensive and up-to-date

## 🚀 Deployment

### Production Ready Services
Both auth and snippets services are production-ready with:
- Comprehensive error handling
- Security validation
- Performance optimization
- Full test coverage

### Serverless Deployment
Each service is designed for independent serverless deployment:

**Recommended Platforms:**
- **Google Cloud Functions** - Google OAuth integration benefits
- **AWS Lambda** - Automatic scaling, pay-per-request  
- **Vercel Functions** - Seamless integration with frontend
- **Azure Functions** - Enterprise deployment option

### Production Checklist
- [x] Environment variables secured
- [x] MongoDB async connection optimized
- [x] Google OAuth admin detection configured
- [x] Comprehensive schema validation implemented
- [x] Full test suite coverage
- [ ] Rate limiting implemented (planned)
- [ ] Monitoring and logging configured (planned)
- [ ] SSL/TLS certificates installed
- [ ] Database backups automated (planned)

## 🤝 Contributing

### Development Workflow
1. Follow existing service patterns in `/auth` and `/snippets`
2. Implement strict schema validation following established patterns
3. Add comprehensive tests following modular test structure
4. Update service documentation
5. Ensure all tests pass before submitting

### Code Standards
- **Python 3.9+** - Modern Python features and syntax
- **Flask** - Lightweight web framework for all services
- **Motor/PyMongo** - Async MongoDB driver for performance
- **Strict Validation** - All schemas must enforce type safety
- **Type Hints** - Include type annotations for clarity
- **Error Handling** - Proper HTTP status codes (400/422 not 500)

### Schema Validation Standards
All new schemas must follow the established pattern:
- **Type validation first** - Check types before processing
- **Throw errors** - No silent defaults or type conversion
- **Consistent messages** - Clear, specific error messages
- **Test coverage** - Comprehensive validation tests

---

**Current Phase**: Phase 2 Complete ✅  
**Status**: Authentication + Snippets Production Ready 🚀  
**Next**: Phase 3 - Core Practice Features

*Simple architecture enables complex features. Complex architecture creates simple bugs.* 🎯