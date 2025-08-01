"use client"

import { createContext, useContext, useEffect, useState } from 'react'

type Theme = 'light' | 'dark'

interface ThemeContextType {
  theme: Theme
  toggleTheme: () => void
  mounted: boolean
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined)

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<Theme>('light')
  const [mounted, setMounted] = useState(false)

  // Load theme from localStorage on mount
  useEffect(() => {
    const savedTheme = localStorage.getItem('theme') as Theme
    const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
    
    setTheme(savedTheme || systemTheme)
    setMounted(true)
  }, [])

  // Apply theme to document root
  useEffect(() => {
    if (mounted) {
      const root = document.documentElement
      
      if (theme === 'dark') {
        root.style.setProperty('--background', '#0a0a0a')
        root.style.setProperty('--foreground', '#ededed')
        root.style.setProperty('--muted-foreground', '#a1a1aa')
        root.style.setProperty('--border', '#27272a')
      } else {
        root.style.setProperty('--background', '#ffffff')
        root.style.setProperty('--foreground', '#171717')
        root.style.setProperty('--muted-foreground', '#71717a')
        root.style.setProperty('--border', '#e4e4e7')
      }
      
      localStorage.setItem('theme', theme)
    }
  }, [theme, mounted])

  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light')
  }

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme, mounted }}>
      {children}
    </ThemeContext.Provider>
  )
}

export function useTheme() {
  const context = useContext(ThemeContext)
  if (context === undefined) {
    // During SSR or if provider is missing, return default values
    if (typeof window === 'undefined') {
      return { theme: 'light' as Theme, toggleTheme: () => {}, mounted: false }
    }
    throw new Error('useTheme must be used within a ThemeProvider')
  }
  return context
}