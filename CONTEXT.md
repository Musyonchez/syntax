# SyntaxMem - AI Assistant Context File

## Project Overview
**SyntaxMem** is an interactive coding practice platform where users complete masked code snippets to improve their programming skills. Think of it as "fill-in-the-blanks" for code learning.

### Original Implementation
The project started with a full-stack implementation stored in the `/old/` directory:
- **Client**: Next.js 15 with Apollo GraphQL, Redux, NextAuth
- **Server**: FastAPI with Strawberry GraphQL + SQLite
- **Features**: Code masking, leaderboards, snippet management, Google OAuth

### Current Status: Complete Rebuild
We are rebuilding SyntaxMem from scratch with a modern, scalable architecture:
- **Client**: Next.js 15 + React 19 + TypeScript + Tailwind CSS
- **Server**: Google Cloud Functions (FaaS) + Python
- **Database**: MongoDB Atlas
- **Deployment**: Vercel (client) + Google Cloud (server)

---

## Core Concept & Features

### How SyntaxMem Works
1. **Code Masking**: Take programming code and intelligently mask tokens (keywords, operators, etc.)
2. **Practice Mode**: Users fill in the blanks to complete the code
3. **Scoring**: Compare user input with correct answers using similarity algorithms
4. **Leaderboards**: Track user performance and rankings

### Example Workflow
```python
# Original Code
def calculate_total(items):
    return sum(item.price for item in items)

# Masked Version (difficulty 5/10)
def _____(items):
    return ___(item.price ___ item in items)

# User fills in: "calculate_total", "sum", "for"
# System scores based on accuracy and similarity
```

---

## Architecture Overview

### Client-Side Stack
- **Framework**: Next.js 15 with App Router
- **UI**: React 19 + TypeScript + Tailwind CSS
- **State**: Zustand (replacing Redux for simplicity)
- **API**: TanStack Query (replacing Apollo GraphQL)
- **Auth**: NextAuth.js v5 with Google OAuth
- **Code Editor**: CodeMirror 6 for syntax highlighting
- **Deployment**: Vercel

### Server-Side Stack  
- **Platform**: Google Cloud Functions (FaaS/Serverless)
- **Language**: Python
- **Database**: MongoDB Atlas
- **Services**: Code masking, similarity scoring, user management
- **API Style**: REST (simple and scalable for FaaS)

---

## Feature Set

### Core MVP Features
1. **Dual Snippet System**:
   - **Official Snippets**: Curated by admin, count towards leaderboard
   - **Personal Snippets**: User-created, for private practice only

2. **Practice System**:
   - Intelligent code masking based on difficulty (1-10 scale)
   - Support for Python and JavaScript initially
   - Real-time scoring and feedback

3. **Leaderboard System**:
   - Global rankings based on official snippet performance
   - Filtering by language and time periods
   - Score calculation includes accuracy and speed

4. **User Management**:
   - Google OAuth authentication only (no file uploads)
   - User profiles with statistics and progress tracking
   - Personal dashboard with analytics

### Community Features
1. **Snippet Submission System**:
   - Users can submit code snippets for review
   - Admin approval process with feedback
   - Credit system for approved contributors

2. **Developer Forum**:
   - Direct communication channel between users and the developer
   - Threaded comment system with nested replies
   - Voting system (upvote/downvote) for content ranking
   - Popular content automatically rises to the top

### Admin Features
- Review queue for submitted snippets
- Forum post creation and management
- User analytics and platform insights

---

## Technical Implementation

### Database Schema (MongoDB)

#### Users Collection
```javascript
{
  _id: ObjectId,
  googleId: String,
  email: String,
  name: String,
  avatar: String,
  role: "user" | "admin",
  preferences: {
    theme: "dark" | "light",
    languages: ["python", "javascript"],
    difficulty: Number
  },
  stats: {
    totalScore: Number,
    practiceTime: Number,
    streak: Number,
    level: Number,
    achievements: [String]
  },
  createdAt: Date,
  lastActive: Date
}
```

#### Snippets Collection
```javascript
{
  _id: ObjectId,
  title: String,
  content: String,
  language: String,
  difficulty: Number,
  type: "official" | "personal",
  status: "active" | "pending" | "rejected",
  author: ObjectId,
  originalAuthor: ObjectId, // For credited submissions
  submittedAt: Date,
  reviewedAt: Date,
  reviewNotes: String,
  solveCount: Number,
  avgScore: Number,
  createdAt: Date
}
```

#### Practice Sessions Collection
```javascript
{
  _id: ObjectId,
  userId: ObjectId,
  snippetId: ObjectId,
  maskedCode: String,
  answers: [String],
  userAnswers: [String],
  score: Number,
  timeSpent: Number,
  mistakes: [{
    position: Number,
    expected: String,
    provided: String
  }],
  createdAt: Date
}
```

#### Forum Posts Collection
```javascript
{
  _id: ObjectId,
  title: String,
  content: String,
  author: ObjectId, // Dev account
  type: "announcement" | "question" | "update",
  isPinned: Boolean,
  votes: { up: Number, down: Number },
  commentCount: Number,
  createdAt: Date,
  updatedAt: Date
}
```

#### Forum Comments Collection
```javascript
{
  _id: ObjectId,
  postId: ObjectId,
  parentId: ObjectId, // For nested replies
  content: String,
  author: ObjectId,
  votes: { up: Number, down: Number, score: Number },
  depth: Number, // Nesting level
  createdAt: Date,
  updatedAt: Date
}
```

---

## API Structure

### Core Endpoints
- `POST /auth/verify` - Verify JWT tokens
- `GET /snippets/official` - List official snippets
- `GET /snippets/personal` - List user's personal snippets
- `GET /snippets/:id/mask` - Get masked version for practice
- `POST /practice/submit` - Submit practice attempt
- `GET /leaderboard` - Get leaderboard data
- `GET /users/profile` - Get user profile and stats

### Content Management
- `POST /snippets/create` - Create personal snippet
- `POST /snippets/submit` - Submit snippet for review
- `GET /snippets/submissions` - Get user's submissions
- `GET /admin/snippets/pending` - Get review queue (admin)
- `PUT /admin/snippets/:id/review` - Approve/reject submission

### Forum System
- `GET /forum/posts` - Get forum posts with pagination
- `POST /forum/posts` - Create new post (dev only)
- `GET /forum/posts/:id/comments` - Get post comments
- `POST /forum/comments` - Create comment
- `PUT /forum/votes` - Vote on post/comment

---

## Core Services

### Code Masking Engine
- **Purpose**: Intelligently mask tokens in code based on difficulty
- **Languages**: Python, JavaScript (expandable)
- **Algorithm**: Uses Pygments tokenization to identify keywords, operators, punctuation
- **Difficulty Scaling**: 1-10 scale affects probability of masking (10% to 100%)
- **Preservation**: Maintains imports, comments, and code structure

### Similarity Scoring
- **Purpose**: Compare user answers with correct solutions
- **Algorithm**: String similarity with fuzzy matching
- **Scoring**: Weighted by token importance and user response time
- **Feedback**: Detailed mistake analysis for learning

### Progress Tracking
- **Scope**: Official snippets only (personal snippets don't affect rankings)
- **Metrics**: Accuracy, speed, consistency, improvement over time
- **Achievements**: Badges for milestones, streaks, language mastery

---

## Project Structure

```
/syntax/
├── client/          # Next.js frontend (empty, to be built)
├── server/          # Google Cloud Functions (empty, to be built)
├── old/             # Original implementation (reference only)
│   ├── client/      # Original Next.js app
│   ├── server/      # Original FastAPI app
│   └── ...          # Other prototype directories
├── progress.md      # Detailed feature checklist and progress
└── CONTEXT.md       # This file - complete project context
```

---

## Development Philosophy

### Focus Areas
1. **User Experience**: Smooth, intuitive practice interface
2. **Performance**: Fast loading, responsive interactions
3. **Scalability**: Serverless architecture for automatic scaling
4. **Community**: Foster learning through interaction and contribution
5. **Quality**: Curated content with proper review processes

### Technical Decisions
- **FaaS over Traditional Server**: Cost-effective, auto-scaling, zero maintenance
- **MongoDB over SQL**: Flexible schema for rapid iteration
- **Next.js App Router**: Modern React patterns with server components
- **Zustand over Redux**: Simpler state management for better DX
- **TanStack Query**: Better server state management than GraphQL for this use case

---

## Current Development Status

### Completed
- ✅ Project architecture planning
- ✅ Database schema design
- ✅ API endpoint specification
- ✅ Feature requirement analysis
- ✅ Technology stack selection

### In Progress
- 🔄 Setting up development environment
- 🔄 Creating foundational project structure

### Next Steps
1. Initialize Next.js client project
2. Set up Google Cloud Functions
3. Configure MongoDB Atlas
4. Implement core authentication
5. Build code masking service
6. Create practice interface

---

## Important Notes for AI Assistants

### When Working on This Project
1. **Always prioritize MVP features** over advanced enhancements
2. **Maintain the dual snippet system** - official vs personal is crucial
3. **Leaderboard only tracks official snippets** - this is a key business rule
4. **Forum is for dev-user communication** - not general user discussion
5. **Focus on code quality and user experience** over feature quantity

### Key Files to Reference
- `progress.md` - Detailed feature checklist and development progress
- `old/` directory - Original implementation for reference (don't modify)
- This file (`CONTEXT.md`) - Complete project understanding

### Development Approach
- Start with core features, expand gradually
- Test early and often
- Prioritize mobile responsiveness
- Implement proper error handling
- Add analytics from the beginning

---

**Last Updated**: 2025-07-12  
**Status**: Planning Complete - Ready for Development  
**Next Action**: Initialize client and server projects