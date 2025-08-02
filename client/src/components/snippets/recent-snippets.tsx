'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { apiClient, type PersonalSnippet } from '@/lib/api-client'

interface RecentSnippetsProps {
  accessToken: string
  refreshToken: string
}

export function RecentSnippets({ accessToken, refreshToken }: RecentSnippetsProps) {
  const [snippets, setSnippets] = useState<PersonalSnippet[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function fetchRecentSnippets() {
      try {
        setLoading(true)
        setError(null)
        const data = await apiClient.getPersonalSnippets(accessToken, refreshToken)
        // Get the 3 most recent snippets
        setSnippets(data.snippets.slice(0, 3))
      } catch (err) {
        // Don't show error if it's a session expiration (user will be redirected)
        if (err instanceof Error && err.message.includes('Session expired')) {
          // User will be redirected to login, don't show error
          return
        }
        setError(err instanceof Error ? err.message : 'Failed to load snippets')
      } finally {
        setLoading(false)
      }
    }

    fetchRecentSnippets()
  }, [accessToken, refreshToken])

  if (loading) {
    return (
      <div className="bg-background border border-border rounded-xl p-6 space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="font-semibold text-foreground">Recent Snippets</h3>
          <div className="w-16 h-4 bg-foreground/10 rounded animate-pulse"></div>
        </div>
        <div className="space-y-3">
          {[1, 2, 3].map((i) => (
            <div key={i} className="p-3 bg-foreground/5 rounded-lg">
              <div className="w-32 h-4 bg-foreground/10 rounded animate-pulse mb-2"></div>
              <div className="w-24 h-3 bg-foreground/10 rounded animate-pulse"></div>
            </div>
          ))}
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-background border border-border rounded-xl p-6 space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="font-semibold text-foreground">Recent Snippets</h3>
          <Link 
            href="/snippets"
            className="text-sm text-muted-foreground hover:text-foreground transition-colors"
          >
            View all
          </Link>
        </div>
        <div className="text-center py-4">
          <p className="text-sm text-muted-foreground">Unable to load snippets</p>
          <p className="text-xs text-muted-foreground mt-1">{error}</p>
        </div>
      </div>
    )
  }

  if (snippets.length === 0) {
    return (
      <div className="bg-background border border-border rounded-xl p-6 space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="font-semibold text-foreground">Recent Snippets</h3>
          <Link 
            href="/snippets"
            className="text-sm text-muted-foreground hover:text-foreground transition-colors"
          >
            Create first
          </Link>
        </div>
        <div className="text-center py-8">
          <div className="w-16 h-16 bg-foreground/10 rounded-full flex items-center justify-center mx-auto mb-3">
            📝
          </div>
          <p className="text-sm font-medium text-foreground">No snippets yet</p>
          <p className="text-xs text-muted-foreground mt-1">
            Create your first code snippet to get started
          </p>
          <Link 
            href="/snippets"
            className="inline-block mt-3 text-sm text-foreground hover:text-foreground/80 transition-colors"
          >
            Create Snippet →
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="bg-background border border-border rounded-xl p-6 space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="font-semibold text-foreground">Recent Snippets</h3>
        <Link 
          href="/snippets"
          className="text-sm text-muted-foreground hover:text-foreground transition-colors"
        >
          View all
        </Link>
      </div>
      
      <div className="space-y-3">
        {snippets.map((snippet) => (
          <div key={snippet._id} className="p-3 bg-foreground/5 rounded-lg hover:bg-foreground/10 transition-colors">
            <div className="flex items-start justify-between">
              <div className="flex-1 min-w-0">
                <h4 className="text-sm font-medium text-foreground truncate">
                  {snippet.title}
                </h4>
                <p className="text-xs text-muted-foreground mt-1 line-clamp-2">
                  {snippet.description}
                </p>
                <div className="flex items-center space-x-2 mt-2">
                  <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-foreground/10 text-foreground">
                    {snippet.language}
                  </span>
                  <span className="text-xs text-muted-foreground">
                    {snippet.difficulty}
                  </span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}