'use server'

import { cookies } from 'next/headers'
import { auth } from './auth'

// Server-side token management using secure HTTP-only cookies
// Simple, Uniform, Consistent

const AUTH_API_URL = process.env.NEXT_PUBLIC_AUTH_API_URL || 'http://localhost:8081'

/**
 * Get backend access token for authenticated user
 * Tokens are stored in secure HTTP-only cookies, not exposed to client
 */
export async function getBackendToken(): Promise<string | null> {
  const session = await auth()
  if (!session?.user?.id) {
    return null
  }

  // Check if we have a valid token in cookies
  const cookieStore = cookies()
  const backendToken = cookieStore.get(`backend_token_${session.user.id}`)
  
  if (backendToken?.value) {
    return backendToken.value
  }

  // If no token in cookies, we need to get a fresh one
  // This would happen on initial login or token expiry
  return null
}

/**
 * Store backend tokens securely in HTTP-only cookies
 */
export async function storeBackendTokens(userId: string, accessToken: string, refreshToken: string) {
  const cookieStore = cookies()
  
  // Store access token (1 hour expiry)
  cookieStore.set(`backend_token_${userId}`, accessToken, {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'lax',
    maxAge: 60 * 60, // 1 hour
    path: '/'
  })
  
  // Store refresh token (30 days expiry)
  cookieStore.set(`refresh_token_${userId}`, refreshToken, {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'lax',
    maxAge: 30 * 24 * 60 * 60, // 30 days
    path: '/'
  })
}

/**
 * Revoke tokens on backend and clear cookies
 */
export async function serverLogout(): Promise<void> {
  const session = await auth()
  if (!session?.user?.id) {
    return
  }

  const cookieStore = cookies()
  const refreshToken = cookieStore.get(`refresh_token_${session.user.id}`)
  
  try {
    // Call backend logout endpoint if we have a refresh token
    if (refreshToken?.value) {
      await fetch(`${AUTH_API_URL}/logout`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          refreshToken: refreshToken.value,
        }),
      })
    }
  } catch (error) {
    // Log error but continue with cookie cleanup
    if (process.env.NODE_ENV === 'development') {
      console.error('Backend logout failed:', error)
    }
  }

  // Clear cookies regardless of backend call success
  cookieStore.delete(`backend_token_${session.user.id}`)
  cookieStore.delete(`refresh_token_${session.user.id}`)
}

/**
 * Logout from all devices
 */
export async function serverLogoutAll(): Promise<{ message: string; revokedTokens: number }> {
  const backendToken = await getBackendToken()
  const session = await auth()
  
  if (!backendToken || !session?.user?.id) {
    throw new Error('Not authenticated')
  }

  try {
    const response = await fetch(`${AUTH_API_URL}/logout-all`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${backendToken}`,
        'Content-Type': 'application/json',
      },
    })

    if (!response.ok) {
      throw new Error('Failed to logout all devices')
    }

    const data = await response.json()
    
    // Clear local cookies
    const cookieStore = cookies()
    cookieStore.delete(`backend_token_${session.user.id}`)
    cookieStore.delete(`refresh_token_${session.user.id}`)
    
    return data.data || { message: 'Logged out from all devices', revokedTokens: 0 }
  } catch (error) {
    if (process.env.NODE_ENV === 'development') {
      console.error('Logout all devices failed:', error)
    }
    throw error
  }
}

/**
 * Make authenticated API calls to backend services
 */
export async function makeAuthenticatedRequest(url: string, options: RequestInit = {}): Promise<Response> {
  const backendToken = await getBackendToken()
  
  if (!backendToken) {
    throw new Error('No authentication token available')
  }

  return fetch(url, {
    ...options,
    headers: {
      ...options.headers,
      'Authorization': `Bearer ${backendToken}`,
      'Content-Type': 'application/json',
    },
  })
}