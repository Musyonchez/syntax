export interface ApiResponse<T = unknown> {
  success: boolean
  data?: T
  message?: string
  error?: string
}

export class ApiClient {
  private baseUrl: string

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl
  }

  private async getAuthToken(): Promise<string | null> {
    try {
      const response = await fetch('/api/auth/session')
      if (response.ok) {
        const session = await response.json()
        console.log('[DEBUG] Session from /api/auth/session:', session)
        console.log('[DEBUG] AccessToken:', session?.accessToken ? 'present' : 'missing')
        return session?.accessToken || null
      }
      console.log('[DEBUG] Session request failed:', response.status)
    } catch (error) {
      console.log('[DEBUG] Session request error:', error)
      // Silently fail - auth is optional for some endpoints
    }
    return null
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    try {
      const token = await this.getAuthToken()
      console.log('[DEBUG] Token for request:', token ? 'present' : 'missing')
      const headers: Record<string, string> = {
        "Content-Type": "application/json",
        ...(options.headers as Record<string, string> || {}),
      }

      if (token) {
        headers.Authorization = `Bearer ${token}`
        console.log('[DEBUG] Authorization header set')
      } else {
        console.log('[DEBUG] No token available, Authorization header not set')
      }

      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        ...options,
        headers,
      })

      const data = await response.json()

      if (!response.ok) {
        // Let NextAuth handle auth errors - just return the error
        return {
          success: false,
          error: data.message || `HTTP ${response.status}: ${response.statusText}`,
        }
      }

      return {
        success: true,
        data: data.data || data,
        message: data.message,
      }
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : "Network error",
      }
    }
  }

  async get<T>(endpoint: string): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, { method: "GET" })
  }

  async post<T>(endpoint: string, data?: unknown): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, {
      method: "POST",
      body: data ? JSON.stringify(data) : undefined,
    })
  }

  async put<T>(endpoint: string, data?: unknown): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, {
      method: "PUT",
      body: data ? JSON.stringify(data) : undefined,
    })
  }

  async delete<T>(endpoint: string): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, { method: "DELETE" })
  }
}

// Service-specific URLs
const API_URLS = {
  auth: process.env.NEXT_PUBLIC_AUTH_API_URL || 'http://localhost:8081',
  snippets: process.env.NEXT_PUBLIC_SNIPPETS_API_URL || 'http://localhost:8082',
  practice: process.env.NEXT_PUBLIC_PRACTICE_API_URL || 'http://localhost:8083',
  leaderboard: process.env.NEXT_PUBLIC_LEADERBOARD_API_URL || 'http://localhost:8084',
  forum: process.env.NEXT_PUBLIC_FORUM_API_URL || 'http://localhost:8085',
}

// Service-specific API client instances
export const authApi = new ApiClient(API_URLS.auth)
export const snippetsApi = new ApiClient(API_URLS.snippets)
export const practiceApi = new ApiClient(API_URLS.practice)
export const leaderboardApi = new ApiClient(API_URLS.leaderboard)
export const forumApi = new ApiClient(API_URLS.forum)