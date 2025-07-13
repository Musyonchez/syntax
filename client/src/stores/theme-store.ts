import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'

interface ThemeState {
  theme: 'light' | 'dark' | 'system'
  resolvedTheme: 'light' | 'dark'
}

interface ThemeActions {
  setTheme: (theme: 'light' | 'dark' | 'system') => void
  setResolvedTheme: (theme: 'light' | 'dark') => void
  toggleTheme: () => void
}

type ThemeStore = ThemeState & ThemeActions

export const useThemeStore = create<ThemeStore>()(
  devtools(
    persist(
      (set, get) => ({
        // State
        theme: 'system',
        resolvedTheme: 'dark',

        // Actions
        setTheme: (theme) =>
          set(
            { theme },
            false,
            'theme/setTheme'
          ),

        setResolvedTheme: (resolvedTheme) =>
          set(
            { resolvedTheme },
            false,
            'theme/setResolvedTheme'
          ),

        toggleTheme: () => {
          const { resolvedTheme } = get()
          set(
            {
              theme: resolvedTheme === 'dark' ? 'light' : 'dark',
              resolvedTheme: resolvedTheme === 'dark' ? 'light' : 'dark',
            },
            false,
            'theme/toggleTheme'
          )
        },
      }),
      {
        name: 'syntaxmem-theme',
        partialize: (state) => ({
          theme: state.theme,
        }),
      }
    ),
    {
      name: 'theme-store',
    }
  )
)