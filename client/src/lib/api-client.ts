/**
 * API Client for SyntaxMem
 * Centralized API calls following Simple, Uniform, Consistent principle
 */

const API_ENDPOINTS = {
  auth: process.env.NEXT_PUBLIC_AUTH_API_URL || 'http://localhost:8081',
  snippets: process.env.NEXT_PUBLIC_SNIPPETS_API_URL || 'http://localhost:8082',
  practice: process.env.NEXT_PUBLIC_PRACTICE_API_URL || 'http://localhost:8083'
}

interface ApiResponse<T> {
  success: boolean
  message: string
  data: T
}

interface UserStats {
  personalSnippets: number
  practiceStats?: {
    sessionsCompleted: number
    averageScore: number
  }
}

interface PersonalSnippet {
  _id: string
  title: string
  description: string
  language: string
  difficulty: string
  tags: string[]
  code: string
  createdAt: string
  updatedAt: string
}

interface SnippetsResponse {
  snippets: PersonalSnippet[]
  count: number
}

class ApiClient {
  private cache = new Map<string, { data: any; timestamp: number; ttl: number }>()
  
  private getCacheKey(endpoint: string, token: string): string {
    return `${endpoint}_${token.substring(0, 20)}`
  }
  
  private getFromCache<T>(key: string): T | null {
    const cached = this.cache.get(key)
    if (!cached) return null
    
    if (Date.now() - cached.timestamp > cached.ttl) {
      this.cache.delete(key)
      return null
    }
    
    return cached.data
  }
  
  private setCache(key: string, data: any, ttlMs: number = 60000): void {
    this.cache.set(key, {
      data,
      timestamp: Date.now(),
      ttl: ttlMs
    })
  }
  
  clearSnippetsCache(): void {
    // Clear all snippet-related cache when data changes
    for (const key of this.cache.keys()) {
      if (key.includes('personal_snippets')) {
        this.cache.delete(key)
      }
    }
  }
  private async request<T>(
    url: string, 
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    try {
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
        ...options,
      })

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`)
      }

      const data = await response.json()
      return data
    } catch (error) {
      console.error('API Request failed:', error)
      throw error
    }
  }

  async getPersonalSnippets(token: string, refreshToken?: string): Promise<SnippetsResponse> {
    const cacheKey = this.getCacheKey('personal_snippets', token)
    
    // Check cache first
    const cached = this.getFromCache<SnippetsResponse>(cacheKey)
    if (cached) {
      return cached
    }
    
    try {
      const response = await this.request<SnippetsResponse>(
        `${API_ENDPOINTS.snippets}/personal`,
        {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        }
      )

      if (!response.success) {
        throw new Error(response.message)
      }

      // Cache the result for 1 minute
      this.setCache(cacheKey, response.data, 60000)
      return response.data
    } catch (error) {
      // If 401 and we have refresh token, try to refresh and retry
      if (error.message?.includes('401') && refreshToken) {
        try {
          const newToken = await this.refreshToken(refreshToken)
          
          // Retry with new token
          const response = await this.request<SnippetsResponse>(
            `${API_ENDPOINTS.snippets}/personal`,
            {
              headers: {
                'Authorization': `Bearer ${newToken}`,
              },
            }
          )

          if (!response.success) {
            throw new Error(response.message)
          }

          // Cache the refreshed result
          this.setCache(cacheKey, response.data, 60000)
          return response.data
        } catch (refreshError) {
          // Both tokens expired - sign out and redirect
          await this.handleSessionExpired()
          throw new Error('Session expired. Please log in again.')
        }
      }
      
      throw error
    }
  }

  private async refreshToken(refreshToken: string): Promise<string> {
    const response = await fetch(`${API_ENDPOINTS.auth}/refresh`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ refreshToken }),
    })

    if (!response.ok) {
      throw new Error(`Token refresh failed: ${response.status}`)
    }

    const data = await response.json()
    if (!data.success) {
      throw new Error(data.message)
    }

    return data.data.token
  }

  private async handleSessionExpired(): Promise<void> {
    try {
      // Call server logout endpoint to clean up refresh token
      const refreshTokenResponse = await fetch('/api/auth/session')
      if (refreshTokenResponse.ok) {
        const session = await refreshTokenResponse.json()
        if (session?.user?.refreshToken) {
          // Try to revoke refresh token on server
          await fetch(`${API_ENDPOINTS.auth}/logout`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ refreshToken: session.user.refreshToken }),
          }).catch(() => {
            // Ignore errors - token might already be expired/invalid
          })
        }
      }
      
      // Sign out from NextAuth and redirect to login
      const { signOut } = await import('next-auth/react')
      await signOut({ 
        callbackUrl: '/login',
        redirect: true 
      })
    } catch (error) {
      // If all else fails, force redirect to login
      window.location.href = '/login'
    }
  }

  async getUserStats(token: string, refreshToken?: string): Promise<UserStats> {
    try {
      // Get personal snippets count
      const snippetsData = await this.getPersonalSnippets(token, refreshToken)
      
      // Note: Practice stats will be implemented in Phase 3
      // For now, return basic stats with snippets count
      return {
        personalSnippets: snippetsData.count,
        practiceStats: {
          sessionsCompleted: 0,
          averageScore: 0
        }
      }
    } catch (error) {
      console.error('Failed to fetch user stats:', error)
      return {
        personalSnippets: 0,
        practiceStats: {
          sessionsCompleted: 0,
          averageScore: 0
        }
      }
    }
  }
}

export const apiClient = new ApiClient()
export type { UserStats, PersonalSnippet, SnippetsResponse }