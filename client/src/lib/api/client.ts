
export interface ApiResponse<T = unknown> {
  success: boolean
  data?: T
  message?: string
  error?: string
}

export class ApiClient {
  private baseUrl: string
  private defaultHeaders: Record<string, string>

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl
    this.defaultHeaders = {
      "Content-Type": "application/json",
    }
  }

  private async getAuthToken(): Promise<string | null> {
    try {
      // Get session from NextAuth API route (works in browser)
      const response = await fetch('/api/auth/session')
      if (response.ok) {
        const session = await response.json()
        if (session?.accessToken) {
          return session.accessToken
        }
      }
    } catch {
      // Failed to get auth token
    }
    return null
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    try {
      const token = await this.getAuthToken()
      const headers: Record<string, string> = {
        ...this.defaultHeaders,
        ...(options.headers as Record<string, string> || {}),
      }

      if (token) {
        headers.Authorization = `Bearer ${token}`
      }

      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        ...options,
        headers,
      })

      const data = await response.json()

      if (!response.ok) {
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
        error: error instanceof Error ? error.message : "Unknown error occurred",
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

// Service-specific API base URLs for local development
const AUTH_URL = process.env.NEXT_PUBLIC_AUTH_API_URL || 'http://localhost:8080'
const SNIPPETS_URL = process.env.NEXT_PUBLIC_SNIPPETS_API_URL || 'http://localhost:8081'
const PRACTICE_URL = process.env.NEXT_PUBLIC_PRACTICE_API_URL || 'http://localhost:8082'
const LEADERBOARD_URL = process.env.NEXT_PUBLIC_LEADERBOARD_API_URL || 'http://localhost:8083'
const FORUM_URL = process.env.NEXT_PUBLIC_FORUM_API_URL || 'http://localhost:8084'

// Main API client instance (defaults to auth service for general use)
export const apiClient = new ApiClient(AUTH_URL)

// Service-specific API client instances
export const authApi = new ApiClient(AUTH_URL)
export const snippetsApi = new ApiClient(SNIPPETS_URL)
export const practiceApi = new ApiClient(PRACTICE_URL)
export const leaderboardApi = new ApiClient(LEADERBOARD_URL)
export const forumApi = new ApiClient(FORUM_URL)