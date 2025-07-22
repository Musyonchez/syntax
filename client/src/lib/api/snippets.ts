import { snippetsApi as snippetsApiClient } from './client'

export interface Snippet {
  id: string
  title: string
  content?: string
  language: string
  difficulty: number
  type: 'official' | 'personal'
  status: 'active' | 'pending' | 'rejected'
  author_name: string
  solve_count: number
  avg_score: number
  created_at: string
}

export interface MaskedSnippet {
  snippet_id: string
  title: string
  language: string
  difficulty: number
  masked_code: string
  answer_count: number
  type: 'official' | 'personal'
}

export interface CreateSnippetRequest {
  title: string
  content: string
  language: 'python' | 'javascript'
  difficulty: number
  is_public?: boolean
}

export interface SubmitSnippetRequest {
  title: string
  content: string
  language: 'python' | 'javascript'
  difficulty: number
  description?: string
}

export interface SnippetSubmission {
  id: string
  title: string
  language: string
  difficulty: number
  status: 'pending' | 'active' | 'rejected'
  submitted_at: string
  reviewed_at?: string
  review_notes?: string
}

export const snippetsApi = {
  // Get official snippets (curated, count towards leaderboard)
  async getOfficial(params?: {
    language?: string
    difficulty?: number
    page?: number
    per_page?: number
  }) {
    const searchParams = new URLSearchParams()
    
    if (params?.language) searchParams.set('language', params.language)
    if (params?.difficulty) searchParams.set('difficulty', params.difficulty.toString())
    if (params?.page) searchParams.set('page', params.page.toString())
    if (params?.per_page) searchParams.set('per_page', params.per_page.toString())

    const response = await snippetsApiClient.get<{
      snippets: Snippet[]
      pagination: {
        page: number
        per_page: number
        total_count: number
        total_pages: number
        has_next: boolean
        has_prev: boolean
      }
    }>(`/snippets/official?${searchParams}`)
    
    if (!response.success || !response.data) {
      throw new Error(response.error || 'Failed to get official snippets')
    }
    return response.data
  },

  // Get user's personal snippets
  async getPersonal(params?: {
    page?: number
    per_page?: number
  }) {
    const searchParams = new URLSearchParams()
    
    if (params?.page) searchParams.set('page', params.page.toString())
    if (params?.per_page) searchParams.set('per_page', params.per_page.toString())

    const response = await snippetsApiClient.get<{
      snippets: Snippet[]
      pagination: {
        page: number
        per_page: number
        total_count: number
        total_pages: number
        has_next: boolean
        has_prev: boolean
      }
    }>(`/snippets/personal?${searchParams}`)
    
    if (!response.success || !response.data) {
      throw new Error(response.error || 'Failed to get personal snippets')
    }
    return response.data
  },

  // Get specific snippet by ID
  async getById(snippetId: string): Promise<Snippet> {
    const response = await snippetsApiClient.get<Snippet>(`/snippets/${snippetId}`)
    if (!response.success || !response.data) {
      throw new Error(response.error || 'Failed to get snippet')
    }
    return response.data
  },

  // Get masked version for practice
  async getMasked(snippetId: string, difficulty?: number): Promise<MaskedSnippet> {
    const response = await snippetsApiClient.post<MaskedSnippet>(`/snippets/${snippetId}/mask`, {
      snippet_id: snippetId,
      difficulty
    })
    if (!response.success || !response.data) {
      throw new Error(response.error || 'Failed to get masked snippet')
    }
    return response.data
  },

  // Create personal snippet
  async create(request: CreateSnippetRequest): Promise<Snippet> {
    const response = await snippetsApiClient.post<Snippet>('/snippets/create', request)
    if (!response.success || !response.data) {
      throw new Error(response.error || 'Failed to create snippet')
    }
    return response.data
  },

  // Submit snippet for review (to become official)
  async submit(request: SubmitSnippetRequest): Promise<SnippetSubmission> {
    const response = await snippetsApiClient.post<SnippetSubmission>('/snippets/submit', request)
    if (!response.success || !response.data) {
      throw new Error(response.error || 'Failed to submit snippet')
    }
    return response.data
  },

  // Get user's submissions
  async getSubmissions(): Promise<SnippetSubmission[]> {
    const response = await snippetsApiClient.get<{ submissions: SnippetSubmission[] }>('/snippets/submissions')
    if (!response.success || !response.data) {
      throw new Error(response.error || 'Failed to get submissions')
    }
    return response.data.submissions
  }
}