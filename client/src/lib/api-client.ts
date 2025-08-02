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
  userId: string
  title: string
  description?: string
  code: string
  language: string
  tags?: string[]
  difficulty: 'easy' | 'medium' | 'hard'
  isPrivate?: boolean
  usageCount?: number
  lastUsed?: string
  isActive?: boolean
  createdAt: string
  updatedAt: string
}

interface SnippetsResponse {
  snippets: PersonalSnippet[]
  count: number
}

interface OfficialSnippetsResponse {
  snippets: OfficialSnippet[]
  count: number
}

interface OfficialSnippet {
  _id: string
  title: string
  description: string
  code: string
  language: string
  category: string
  tags: string[]
  difficulty: 'easy' | 'medium' | 'hard'
  learningObjectives: string[]
  hints: string
  solution: string
  createdBy: string
  approvedBy: string
  estimatedTime: number
  isPublished: boolean
  isActive: boolean
  practiceCount: number
  averageScore: number
  createdAt: string
  updatedAt: string
}

interface CreatePersonalSnippetData {
  title: string
  description?: string
  code: string
  language: string
  tags?: string[]
  difficulty?: 'easy' | 'medium' | 'hard'
  isPrivate?: boolean
}

interface UpdatePersonalSnippetData {
  title?: string
  description?: string
  code?: string
  language?: string
  tags?: string[]
  difficulty?: 'easy' | 'medium' | 'hard'
  isPrivate?: boolean
}

interface CreateOfficialSnippetData {
  title: string
  description?: string
  code: string
  language: string
  category: string
  tags?: string[]
  difficulty?: 'easy' | 'medium' | 'hard'
  learningObjectives?: string[]
  hints?: string
  solution: string
  estimatedTime?: number
}

interface SnippetFilters {
  language?: string
  difficulty?: string
  tag?: string
  search?: string
}

interface CacheEntry<T> {
  data: T
  timestamp: number
  ttl: number
}

class ApiClient {
  private cache = new Map<string, CacheEntry<unknown>>()
  
  private async getCacheKey(endpoint: string, token: string): Promise<string> {
    // Use Web Crypto API to create a secure hash of the token
    const encoder = new TextEncoder()
    const data = encoder.encode(token)
    const hashBuffer = await crypto.subtle.digest('SHA-256', data)
    const hashArray = Array.from(new Uint8Array(hashBuffer))
    const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('')
    return `${endpoint}_${hashHex.substring(0, 16)}` // Use first 16 chars of secure hash
  }
  
  private getFromCache<T>(key: string): T | null {
    const cached = this.cache.get(key)
    if (!cached) return null
    
    if (Date.now() - cached.timestamp > cached.ttl) {
      this.cache.delete(key)
      return null
    }
    
    return cached.data as T
  }
  
  private setCache<T>(key: string, data: T, ttlMs: number = 60000): void {
    this.cache.set(key, {
      data,
      timestamp: Date.now(),
      ttl: ttlMs
    })
  }
  
  async clearSnippetsCache(token?: string): Promise<void> {
    if (token) {
      // Clear cache for specific user's snippets
      const cacheKey = await this.getCacheKey('personal_snippets', token)
      this.cache.delete(cacheKey)
    } else {
      // Clear all snippet-related cache when token not provided
      for (const key of this.cache.keys()) {
        if (key.startsWith('personal_snippets_')) {
          this.cache.delete(key)
        }
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
    const cacheKey = await this.getCacheKey('personal_snippets', token)
    
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
      if (error instanceof Error && error.message?.includes('401') && refreshToken) {
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
        } catch {
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

    const newToken = data.data.token
    
    // Update NextAuth session with new token
    await this.updateNextAuthSession(newToken)
    
    return newToken
  }

  private async updateNextAuthSession(newToken: string): Promise<void> {
    try {
      // Update the NextAuth session with the new backend token
      const response = await fetch('/api/auth/update-session', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          backendToken: newToken,
        }),
      })
      
      if (!response.ok) {
        throw new Error(`Session update failed: ${response.status}`)
      }
      
      console.log('Successfully updated NextAuth session with new token')
    } catch (error) {
      console.warn('Failed to update NextAuth session with new token:', error)
      // Don't throw - the token refresh itself succeeded
    }
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
    } catch {
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

  async createPersonalSnippet(data: CreatePersonalSnippetData, token: string, refreshToken?: string): Promise<PersonalSnippet> {
    try {
      const response = await this.request<PersonalSnippet>(
        `${API_ENDPOINTS.snippets}/personal`,
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
          },
          body: JSON.stringify(data),
        }
      )

      if (!response.success) {
        throw new Error(response.message)
      }

      // Clear snippets cache after creation
      await this.clearSnippetsCache(token)
      return response.data
    } catch (error) {
      if (error instanceof Error && error.message?.includes('401') && refreshToken) {
        try {
          const newToken = await this.refreshToken(refreshToken)
          const response = await this.request<PersonalSnippet>(
            `${API_ENDPOINTS.snippets}/personal`,
            {
              method: 'POST',
              headers: {
                'Authorization': `Bearer ${newToken}`,
              },
              body: JSON.stringify(data),
            }
          )

          if (!response.success) {
            throw new Error(response.message)
          }

          await this.clearSnippetsCache(newToken)
          return response.data
        } catch {
          await this.handleSessionExpired()
          throw new Error('Session expired. Please log in again.')
        }
      }
      throw error
    }
  }

  async updatePersonalSnippet(id: string, data: UpdatePersonalSnippetData, token: string, refreshToken?: string): Promise<PersonalSnippet> {
    try {
      const response = await this.request<PersonalSnippet>(
        `${API_ENDPOINTS.snippets}/personal/${id}`,
        {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${token}`,
          },
          body: JSON.stringify(data),
        }
      )

      if (!response.success) {
        throw new Error(response.message)
      }

      await this.clearSnippetsCache(token)
      return response.data
    } catch (error) {
      if (error instanceof Error && error.message?.includes('401') && refreshToken) {
        try {
          const newToken = await this.refreshToken(refreshToken)
          const response = await this.request<PersonalSnippet>(
            `${API_ENDPOINTS.snippets}/personal/${id}`,
            {
              method: 'PUT',
              headers: {
                'Authorization': `Bearer ${newToken}`,
              },
              body: JSON.stringify(data),
            }
          )

          if (!response.success) {
            throw new Error(response.message)
          }

          await this.clearSnippetsCache(newToken)
          return response.data
        } catch {
          await this.handleSessionExpired()
          throw new Error('Session expired. Please log in again.')
        }
      }
      throw error
    }
  }

  async deletePersonalSnippet(id: string, token: string, refreshToken?: string): Promise<{ deleted: boolean }> {
    try {
      const response = await this.request<{ deleted: boolean }>(
        `${API_ENDPOINTS.snippets}/personal/${id}`,
        {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        }
      )

      if (!response.success) {
        throw new Error(response.message)
      }

      await this.clearSnippetsCache(token)
      return response.data
    } catch (error) {
      if (error instanceof Error && error.message?.includes('401') && refreshToken) {
        try {
          const newToken = await this.refreshToken(refreshToken)
          const response = await this.request<{ deleted: boolean }>(
            `${API_ENDPOINTS.snippets}/personal/${id}`,
            {
              method: 'DELETE',
              headers: {
                'Authorization': `Bearer ${newToken}`,
              },
            }
          )

          if (!response.success) {
            throw new Error(response.message)
          }

          await this.clearSnippetsCache(newToken)
          return response.data
        } catch {
          await this.handleSessionExpired()
          throw new Error('Session expired. Please log in again.')
        }
      }
      throw error
    }
  }

  async getOfficialSnippets(filters?: SnippetFilters): Promise<OfficialSnippetsResponse> {
    const cacheKey = `official_snippets_${JSON.stringify(filters || {})}`
    
    const cached = this.getFromCache<OfficialSnippetsResponse>(cacheKey)
    if (cached) {
      return cached
    }
    
    const queryParams = new URLSearchParams()
    if (filters?.language) queryParams.set('language', filters.language)
    if (filters?.difficulty) queryParams.set('difficulty', filters.difficulty)
    if (filters?.tag) queryParams.set('tag', filters.tag)
    if (filters?.search) queryParams.set('search', filters.search)
    
    const url = `${API_ENDPOINTS.snippets}/official${queryParams.toString() ? `?${queryParams.toString()}` : ''}`
    
    try {
      const response = await this.request<OfficialSnippetsResponse>(url)

      if (!response.success) {
        throw new Error(response.message)
      }

      this.setCache(cacheKey, response.data, 300000) // Cache for 5 minutes
      return response.data
    } catch (error) {
      console.error('Failed to fetch official snippets:', error)
      throw error
    }
  }
}

export const apiClient = new ApiClient()
export type { 
  UserStats, 
  PersonalSnippet, 
  SnippetsResponse,
  OfficialSnippet,
  OfficialSnippetsResponse,
  CreatePersonalSnippetData,
  UpdatePersonalSnippetData,
  CreateOfficialSnippetData,
  SnippetFilters
}