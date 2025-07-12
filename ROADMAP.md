# SyntaxMem MVP Development Progress

## Project Overview
**SyntaxMem** - Interactive coding practice platform where users complete masked code snippets to improve programming skills.

## Core Architecture
- **Client**: Next.js 15 + React 19 + TypeScript + Tailwind CSS
- **Server**: Google Cloud Functions (FaaS) + Python
- **Database**: MongoDB Atlas
- **Auth**: Google OAuth via NextAuth.js v5
- **Deployment**: Vercel (client) + Google Cloud (server)

---

## MVP Feature Checklist

### 🎯 Essential Features
- [ ] **Landing Page** - Hero section, how it works, call-to-action
- [ ] **Google Authentication** - Sign in/out with Google OAuth
- [ ] **Practice Mode** - Code completion with intelligent token masking
- [ ] **Dual Snippet System** - Official vs Personal snippets
- [ ] **Basic Leaderboard** - Score tracking and user rankings (official snippets only)
- [ ] **User Dashboard** - Personal stats and progress overview
- [ ] **Mobile Responsive** - Works seamlessly on all devices

### 🏆 Content Management
- [ ] **Official Snippets** - Curated, high-quality snippets for leaderboard
- [ ] **Personal Snippets** - Private practice snippets (no leaderboard impact)
- [ ] **Submission System** - Users submit snippets for review
- [ ] **Review Queue** - Admin interface for approving/rejecting submissions

### 💬 Community Features
- [ ] **Developer Forum** - Direct communication with dev
- [ ] **Threaded Comments** - Nested replies on forum posts
- [ ] **Voting System** - Upvote/downvote posts and comments
- [ ] **Content Ranking** - Popular content rises to top

---

## 🛠️ Technical Implementation

### Client-Side (Next.js)
- [ ] Set up Next.js 15 project with TypeScript and Tailwind
- [ ] Configure NextAuth.js v5 for Google OAuth
- [ ] Build core UI components (Navbar, Footer, Layout)
- [ ] Implement practice interface with CodeMirror 6
- [ ] Create leaderboard and dashboard pages
- [ ] Add state management with Zustand
- [ ] Set up TanStack Query for API calls

### Server-Side (Python FaaS)
- [ ] Set up Google Cloud Functions project
- [ ] Create authentication middleware
- [ ] Build code masking service (Python/JavaScript support)
- [ ] Implement snippet CRUD operations
- [ ] Create leaderboard scoring system
- [ ] Set up MongoDB connection and models
- [ ] Add user analytics tracking

### Database Schema (MongoDB)
- [ ] Design Users collection
- [ ] Design Snippets collection (with official/personal types)
- [ ] Design Practice Sessions collection
- [ ] Design Leaderboard collection (official snippets only)
- [ ] Design Forum Posts collection
- [ ] Design Forum Comments collection
- [ ] Design User Votes collection
- [ ] Set up MongoDB Atlas instance

---

## 🔗 API Endpoints

### Core Features
- [ ] `POST /auth/verify` - Verify JWT tokens
- [ ] `GET /snippets/official` - List official snippets
- [ ] `GET /snippets/personal` - List user's personal snippets
- [ ] `GET /snippets/:id/mask` - Get masked version for practice
- [ ] `POST /practice/submit` - Submit practice attempt
- [ ] `GET /leaderboard` - Get leaderboard data (official snippets only)
- [ ] `GET /users/profile` - Get user profile and stats

### Content Management
- [ ] `POST /snippets/create` - Create personal snippet
- [ ] `POST /snippets/submit` - Submit snippet for review
- [ ] `GET /snippets/submissions` - Get user's submissions
- [ ] `GET /admin/snippets/pending` - Get review queue (admin)
- [ ] `PUT /admin/snippets/:id/review` - Approve/reject submission

### Forum System
- [ ] `GET /forum/posts` - Get forum posts with pagination
- [ ] `POST /forum/posts` - Create new post (dev only)
- [ ] `GET /forum/posts/:id/comments` - Get post comments
- [ ] `POST /forum/comments` - Create comment
- [ ] `PUT /forum/votes` - Vote on post/comment

---

## ⚙️ Core Services
- [ ] **Code Masking Engine** - Intelligent token masking with difficulty levels
- [ ] **Similarity Scoring** - Compare user input with correct answers
- [ ] **Progress Tracking** - Track user performance and improvement (official snippets only)
- [ ] **Analytics Service** - Capture user behavior and engagement
- [ ] **Content Moderation** - Review submitted snippets for quality
- [ ] **Forum Management** - Handle posts, comments, and voting
- [ ] **Ranking Algorithm** - Sort forum content by popularity

---

## 📊 Success Metrics
- [ ] User can sign in with Google
- [ ] User can practice code completion exercises
- [ ] Scoring system works accurately
- [ ] Leaderboard updates in real-time
- [ ] Mobile experience is smooth
- [ ] Page load times under 3 seconds

---

## 🚀 Post-MVP Enhancements
- Advanced difficulty adaptation
- Multiple programming languages (Go, Rust, Java)
- Enhanced gamification system (badges, achievements, streaks)
- Learning path recommendations
- VS Code extension
- Team challenges and competitions
- Advanced forum features (tagging, search, notifications)
- Snippet categories and advanced filtering
- AI-powered snippet suggestions
- Code review features for submissions

---

## 📝 Development Notes
- Focus on core functionality first
- Prioritize user experience and performance
- Keep architecture simple and scalable
- Add comprehensive error handling
- Implement proper analytics from the start

---

## 🗃️ Database Schema Design

### Snippets Collection
```javascript
{
  _id: ObjectId,
  title: String,
  content: String,
  language: String,
  difficulty: Number,
  type: "official" | "personal", // NEW
  status: "active" | "pending" | "rejected", // NEW
  author: ObjectId,
  originalAuthor: ObjectId, // For credited submissions
  submittedAt: Date,
  reviewedAt: Date,
  reviewNotes: String,
  isPublic: Boolean,
  solveCount: Number,
  avgScore: Number,
  createdAt: Date
}
```

### Forum Posts Collection
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

### Forum Comments Collection
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

### User Votes Collection
```javascript
{
  _id: ObjectId,
  userId: ObjectId,
  targetId: ObjectId, // Post or comment ID
  targetType: "post" | "comment",
  voteType: "up" | "down",
  createdAt: Date
}
```

---

**Last Updated**: 2025-07-12
**Status**: Planning & Initial Setup - Updated with Community Features