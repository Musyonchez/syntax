'use client'

import { useEffect, useState } from 'react'
import { apiClient, type UserStats } from '@/lib/api-client'

interface DashboardStatsProps {
  accessToken: string
  refreshToken: string
}

export function DashboardStats({ accessToken, refreshToken }: DashboardStatsProps) {
  const [stats, setStats] = useState<UserStats | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function fetchStats() {
      try {
        setLoading(true)
        setError(null)
        const userStats = await apiClient.getUserStats(accessToken, refreshToken)
        setStats(userStats)
      } catch (err) {
        // Don't show error if it's a session expiration (user will be redirected)
        if (err instanceof Error && err.message.includes('Session expired')) {
          // User will be redirected to login, don't show error
          return
        }
        console.error('Dashboard: Error fetching stats:', err)
        setError(err instanceof Error ? err.message : 'Failed to load stats')
      } finally {
        setLoading(false)
      }
    }

    if (accessToken) {
      fetchStats()
    } else {
      setError('No access token available')
      setLoading(false)
    }
  }, [accessToken, refreshToken])

  if (loading) {
    return (
      <div className="bg-background border border-border rounded-xl p-6 space-y-4">
        <h3 className="font-semibold text-foreground">Your Progress</h3>
        <div className="space-y-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-foreground/10 rounded-lg animate-pulse"></div>
                <div className="w-24 h-4 bg-foreground/10 rounded animate-pulse"></div>
              </div>
              <div className="w-8 h-6 bg-foreground/10 rounded animate-pulse"></div>
            </div>
          ))}
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-background border border-border rounded-xl p-6 space-y-4">
        <h3 className="font-semibold text-foreground">Your Progress</h3>
        <div className="text-center py-4">
          <p className="text-sm text-muted-foreground">Unable to load stats</p>
          <p className="text-xs text-muted-foreground mt-1">{error}</p>
        </div>
      </div>
    )
  }

  return (
    <div className="bg-background border border-border rounded-xl p-6 space-y-4">
      <h3 className="font-semibold text-foreground">Your Progress</h3>
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-foreground/10 rounded-lg flex items-center justify-center">
              🎯
            </div>
            <span className="text-sm font-medium">Practice Sessions</span>
          </div>
          <span className="text-lg font-bold text-foreground">
            {stats?.practiceStats?.sessionsCompleted || 0}
          </span>
        </div>
        
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-foreground/10 rounded-lg flex items-center justify-center">
              📝
            </div>
            <span className="text-sm font-medium">Snippets Created</span>
          </div>
          <span className="text-lg font-bold text-foreground">
            {stats?.personalSnippets || 0}
          </span>
        </div>
        
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-foreground/10 rounded-lg flex items-center justify-center">
              📊
            </div>
            <span className="text-sm font-medium">Average Score</span>
          </div>
          <span className="text-lg font-bold text-foreground">
            {stats?.practiceStats?.averageScore || 0}%
          </span>
        </div>
      </div>
    </div>
  )
}