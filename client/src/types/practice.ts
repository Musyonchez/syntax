export interface CodeSnippet {
  _id: string
  title: string
  description: string
  language: string
  difficulty: number
  original_code: string
  masked_code: string
  solution_keys: string[]
  type: "official" | "personal"
  author: string
  tags: string[]
  stats: SnippetStats
  created_at: string
  status?: "pending" | "approved" | "rejected"
}

export interface SnippetStats {
  attempts: number
  completions: number
  avg_score: number
  avg_time: number
}

export interface PracticeSession {
  session_id: string
  user_id: string
  snippet_id: string
  start_time: string
  end_time?: string
  score?: number
  completed: boolean
  user_code: string
  time_taken?: number
}

export interface PracticeResult {
  session_id: string
  score: number
  time_taken: number
  mistakes: string[]
  completion_rate: number
  feedback: string
}