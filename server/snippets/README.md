# Snippets Service

**Simple, Uniform, Consistent** code snippet management for SyntaxMem platform.

## 🎯 Purpose

The Snippets service handles:
- **Personal Snippets** - User-created code snippets for practice and reference
- **Official Snippets** - Curated platform content for structured learning
- **Search & Filtering** - Find snippets by language, difficulty, tags, and content
- **Ownership Management** - Secure access control for personal snippets

## 🚀 Endpoints

### Personal Snippets (Authentication Required)
- `GET /personal` - Get user's personal snippets with filtering
- `POST /personal` - Create new personal snippet
- `PUT /personal/<id>` - Update personal snippet (ownership verified)
- `DELETE /personal/<id>` - Soft delete personal snippet (ownership verified)

### Official Snippets (Public Access)
- `GET /official` - Get published official snippets with filtering
- `GET /official/<id>` - Get specific official snippet by ID

### Health Check
- `GET /health` - Service health status

## 🔍 Filtering & Search

All GET endpoints support these query parameters:

### Common Filters
- `language` - Filter by programming language (js, python, etc.)
- `difficulty` - Filter by difficulty level (easy, medium, hard)
- `tag` - Filter by specific tag
- `search` - Text search in title and description

### Official Snippets Only
- `category` - Filter by category (loops, functions, algorithms, etc.)

### Example Requests
```bash
# Get personal JavaScript snippets
GET /personal?language=javascript&difficulty=medium

# Search official snippets
GET /official?search=array&category=algorithms

# Get snippets by tag
GET /personal?tag=react
```

## 📋 Data Models

### Personal Snippet
```json
{
  "_id": "ObjectId",
  "userId": "user123",
  "title": "React Component Example",
  "description": "Basic functional component",
  "code": "const MyComponent = () => { ... }",
  "language": "javascript",
  "tags": ["react", "component"],
  "difficulty": "easy",
  "isPrivate": true,
  "usageCount": 5,
  "lastUsed": "2025-01-30T12:00:00Z",
  "isActive": true,
  "createdAt": "2025-01-25T10:00:00Z",
  "updatedAt": "2025-01-30T12:00:00Z"
}
```

### Official Snippet
```json
{
  "_id": "ObjectId",
  "title": "Array Map Method",
  "description": "Learn array transformation with map",
  "code": "const numbers = [1,2,3]; const doubled = numbers.map(x => x * 2);",
  "language": "javascript",
  "category": "arrays",
  "tags": ["array", "map", "transformation"],
  "difficulty": "medium",
  "learningObjectives": ["Understand map function", "Array transformation"],
  "hints": "Map creates a new array",
  "solution": "Full solution with explanation",
  "createdBy": "admin123",
  "approvedBy": "admin456",
  "estimatedTime": 300,
  "isPublished": true,
  "practiceCount": 1250,
  "averageScore": 85.5,
  "createdAt": "2025-01-20T08:00:00Z",
  "updatedAt": "2025-01-25T14:00:00Z"
}
```

## 🔐 Authentication Flow

### Personal Snippets (Protected)
```
Client → Includes "Bearer <access_token>" in Authorization header
Server → Validates JWT token
Server → Extracts user_id from token
Server → Verifies ownership for modify operations
Server → Processes request with user context
```

### Official Snippets (Public)
```
Client → Makes request without authentication
Server → Only returns published snippets
Server → Processes request with public access
```

## 🚨 Service Rules

### The Sacred Laws (NEVER BREAK)

1. **Ownership Verification** - Users can only modify their own personal snippets
2. **Schema Validation** - All data must pass PersonalSnippetSchema or OfficialSnippetSchema
3. **Soft Deletes** - Personal snippets are marked inactive, never hard deleted
4. **Published Only** - Official snippets endpoints only return published content
5. **JWT Authentication** - Personal snippet endpoints require valid access tokens

### Data Integrity Rules

6. **Required Fields** - Title, code, and language are mandatory for all snippets
7. **Lowercase Normalization** - Languages, tags, categories stored in lowercase
8. **Difficulty Validation** - Only easy/medium/hard allowed, default to medium
9. **Tag Sanitization** - Clean and normalize all tags
10. **Timestamp Management** - Always update 'updatedAt' on modifications

### Security Rules

11. **No Data Leakage** - Never return other users' private snippets
12. **Input Sanitization** - Clean all user input before processing
13. **Error Handling** - Don't expose internal errors or data structures
14. **Rate Limiting** - Implement reasonable request limits
15. **CORS Configuration** - Only allow configured origins

### Performance Rules

16. **Efficient Queries** - Use database indexes for common filters
17. **Pagination** - Implement pagination for large result sets
18. **Caching** - Cache frequently accessed official snippets
19. **Connection Management** - Properly close database connections
20. **Async Operations** - Use async/await for all database operations

## 🔧 Environment Variables

Required environment variables:
```bash
JWT_SECRET=your-secret-key-here
MONGODB_URI=mongodb://connection-string
DATABASE_NAME=syntaxmem
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
```

## 🧪 Testing

Run snippets tests:
```bash
cd ../tests/snippets
./run_snippets_tests.sh
```

Test coverage includes:
- Personal snippet CRUD operations
- Ownership verification
- Official snippet retrieval
- Filtering and search functionality
- Schema validation
- Authentication integration

## 📊 Monitoring

Key metrics to monitor:
- **Snippet creation rate** - Track user engagement
- **Search query patterns** - Popular languages and topics
- **Official snippet usage** - Most accessed content
- **Error rates** - Validation and database errors
- **Response times** - Query performance

## 🚫 What NOT to Do

### Forbidden Patterns
- ❌ Return other users' private snippets
- ❌ Allow hard deletion of personal snippets
- ❌ Skip ownership verification on updates/deletes
- ❌ Return unpublished official snippets to public
- ❌ Store sensitive data in snippet content

### Performance Don'ts
- ❌ Return unlimited results without pagination
- ❌ Use inefficient regex queries on large datasets
- ❌ Skip database indexes on filtered fields
- ❌ Make synchronous database calls
- ❌ Load full snippet content for list views

### Security Don'ts
- ❌ Trust client-provided user IDs
- ❌ Skip authentication for personal endpoints
- ❌ Log snippet content (may contain sensitive code)
- ❌ Allow script injection in snippet code
- ❌ Expose database errors to clients

## ✅ Success Metrics

You know snippets service is working when:
- **Zero unauthorized access** to personal snippets
- **Fast search results** - under 200ms for filtered queries
- **Clean data integrity** - all snippets follow schema rules
- **Reliable filtering** - accurate results for all filter combinations
- **Smooth CRUD operations** - create/update/delete work flawlessly

---

**Remember**: Snippets are the core learning content. Keep them organized, secure, and easily discoverable. 📝

*Great snippets enable great learning experiences.*