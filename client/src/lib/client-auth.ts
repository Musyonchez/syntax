// Client-side auth management using backend JWT

interface User {
  id: string
  googleId: string
  email: string
  name: string
  avatar?: string
  role: string
}

interface AuthState {
  token: string | null
  user: User | null
  isAuthenticated: boolean
}

class ClientAuth {
  private authState: AuthState = {
    token: null,
    user: null,
    isAuthenticated: false
  }

  // Initialize from localStorage on app start
  init() {
    if (typeof window === 'undefined') return

    const token = localStorage.getItem('auth_token')
    const userString = localStorage.getItem('auth_user')
    
    if (token && userString) {
      try {
        const user = JSON.parse(userString)
        this.authState = {
          token,
          user,
          isAuthenticated: true
        }
      } catch (error) {
        console.error('Failed to parse stored user data:', error)
        this.signOut()
      }
    }
  }

  // Store auth data after successful backend authentication
  signIn(token: string, user: User) {
    this.authState = {
      token,
      user,
      isAuthenticated: true
    }
    
    localStorage.setItem('auth_token', token)
    localStorage.setItem('auth_user', JSON.stringify(user))
  }

  // Clear all auth data
  signOut() {
    this.authState = {
      token: null,
      user: null,
      isAuthenticated: false
    }
    
    localStorage.removeItem('auth_token')
    localStorage.removeItem('auth_user')
  }

  // Get current auth state
  getAuthState(): AuthState {
    return { ...this.authState }
  }

  // Get token for API requests
  getToken(): string | null {
    return this.authState.token
  }

  // Get user data
  getUser(): User | null {
    return this.authState.user
  }

  // Check if user is authenticated
  isAuthenticated(): boolean {
    return this.authState.isAuthenticated && !!this.authState.token
  }
}

export const clientAuth = new ClientAuth()

// Auth hook for React components
export function useAuth() {
  return clientAuth.getAuthState()
}