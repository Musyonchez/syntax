export interface ApiResponse<T = unknown> {
  success: boolean
  data?: T
  message?: string
  error?: string
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  pages: number
  limit: number
}

export interface LeaderboardEntry {
  user_id: string
  username: string
  avatar: string
  score: number
  level: number
  streak: number
  rank: number
}

export interface ForumPost {
  _id: string
  title: string
  content: string
  author: {
    user_id: string
    name: string
    avatar: string
    role: string
  }
  category: string
  tags: string[]
  votes: number
  comments_count: number
  created_at: string
  updated_at: string
  is_pinned: boolean
  is_locked: boolean
}

export interface ForumComment {
  _id: string
  post_id: string
  content: string
  author: {
    user_id: string
    name: string
    avatar: string
    role: string
  }
  parent_id?: string
  votes: number
  created_at: string
  updated_at: string
}