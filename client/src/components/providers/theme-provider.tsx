"use client"

import { ThemeProvider as NextThemesProvider } from "next-themes"
import { ReactNode, useEffect } from "react"
import { useThemeStore } from "@/stores/theme-store"

interface ThemeProviderProps {
  children: ReactNode
  attribute?: string
  defaultTheme?: string
  enableSystem?: boolean
  disableTransitionOnChange?: boolean
}

export function ThemeProvider({ children }: ThemeProviderProps) {
  const { setResolvedTheme } = useThemeStore()

  useEffect(() => {
    const updateResolvedTheme = () => {
      const isDark = document.documentElement.classList.contains('dark')
      setResolvedTheme(isDark ? 'dark' : 'light')
    }

    updateResolvedTheme()
    
    const observer = new MutationObserver(updateResolvedTheme)
    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ['class'],
    })

    return () => observer.disconnect()
  }, [setResolvedTheme])

  return (
    <NextThemesProvider
      attribute="class"
      defaultTheme="system"
      enableSystem
      disableTransitionOnChange
    >
      {children}
    </NextThemesProvider>
  )
}