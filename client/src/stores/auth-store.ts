import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'
import type { User } from '@/types/auth'

interface AuthState {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  token: string | null
}

interface AuthActions {
  setUser: (user: User) => void
  setToken: (token: string) => void
  logout: () => void
  setLoading: (loading: boolean) => void
}

type AuthStore = AuthState & AuthActions

export const useAuthStore = create<AuthStore>()(
  devtools(
    persist(
      (set) => ({
        // State
        user: null,
        isAuthenticated: false,
        isLoading: false,
        token: null,

        // Actions
        setUser: (user) =>
          set(
            { user, isAuthenticated: !!user },
            false,
            'auth/setUser'
          ),

        setToken: (token) =>
          set(
            { token },
            false,
            'auth/setToken'
          ),

        logout: () =>
          set(
            {
              user: null,
              isAuthenticated: false,
              token: null,
            },
            false,
            'auth/logout'
          ),

        setLoading: (isLoading) =>
          set(
            { isLoading },
            false,
            'auth/setLoading'
          ),
      }),
      {
        name: 'syntaxmem-auth',
        partialize: (state) => ({
          user: state.user,
          token: state.token,
          isAuthenticated: state.isAuthenticated,
        }),
      }
    ),
    {
      name: 'auth-store',
    }
  )
)