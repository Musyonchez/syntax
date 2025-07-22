import { practiceApi as practiceApiClient } from './client'

export interface PracticeSession {
  session_id: string
  snippet_id: string
  snippet_title: string
  language: 'python' | 'javascript'
  difficulty: number
  masked_code: string
  answer_count: number
  max_time: number
  created_at: string
}

export interface PracticeScore {
  session_id: string
  total_score: number
  accuracy: number
  time_bonus: number
  mistakes: number
  time_taken: number
  detailed_results: Array<{
    position: number
    user_answer: string
    correct_answer: string
    similarity: number
    is_correct: boolean
  }>
  leaderboard_eligible: boolean
}

export interface PracticeHistoryItem {
  session_id: string
  snippet_id: string
  snippet_title: string
  snippet_type: 'official' | 'personal'
  language: string
  difficulty: number
  completed: boolean
  created_at: string
  total_score?: number
  accuracy?: number
  time_taken?: number
  mistakes?: number
  completed_at?: string
}

export interface PracticeStats {
  total_sessions: number
  average_score: number
  average_accuracy: number
  total_practice_time: number
  total_mistakes: number
  languages: Record<string, {
    sessions: number
    avg_score: number
    avg_accuracy: number
  }>
}

export interface StartPracticeRequest {
  snippet_id: string
  difficulty?: number
}

export interface SubmitPracticeRequest {
  session_id: string
  user_answers: string[]
  time_taken: number
}

export const practiceApi = {
  // Start a new practice session
  async startSession(request: StartPracticeRequest): Promise<PracticeSession> {
    const response = await practiceApiClient.post<PracticeSession>('/practice/start', request)
    if (!response.success || !response.data) {
      throw new Error(response.error || 'Failed to start practice session')
    }
    return response.data
  },

  // Submit practice attempt
  async submitSession(request: SubmitPracticeRequest): Promise<PracticeScore> {
    const response = await practiceApiClient.post<PracticeScore>('/practice/submit', request)
    if (!response.success || !response.data) {
      throw new Error(response.error || 'Failed to submit practice session')
    }
    return response.data
  },

  // Get practice session details
  async getSession(sessionId: string): Promise<PracticeSession> {
    const response = await practiceApiClient.get<PracticeSession>(`/practice/session/${sessionId}`)
    if (!response.success || !response.data) {
      throw new Error(response.error || 'Failed to get practice session')
    }
    return response.data
  },

  // Get practice history
  async getHistory(params?: {
    page?: number
    per_page?: number
    language?: string
    completed_only?: boolean
  }) {
    const searchParams = new URLSearchParams()
    
    if (params?.page) searchParams.set('page', params.page.toString())
    if (params?.per_page) searchParams.set('per_page', params.per_page.toString())
    if (params?.language) searchParams.set('language', params.language)
    if (params?.completed_only !== undefined) {
      searchParams.set('completed_only', params.completed_only.toString())
    }

    const response = await practiceApiClient.get<{
      sessions: PracticeHistoryItem[]
      pagination: {
        page: number
        per_page: number
        total_count: number
        total_pages: number
        has_next: boolean
        has_prev: boolean
      }
    }>(`/practice/history?${searchParams}`)
    
    if (!response.success || !response.data) {
      throw new Error(response.error || 'Failed to get practice history')
    }
    return response.data
  },

  // Get practice statistics
  async getStats(): Promise<PracticeStats> {
    const response = await practiceApiClient.get<PracticeStats>('/practice/stats')
    if (!response.success || !response.data) {
      throw new Error(response.error || 'Failed to get practice statistics')
    }
    return response.data
  }
}