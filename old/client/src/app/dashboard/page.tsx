"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'
import { usePracticeStats, usePracticeHistory } from '@/hooks/use-practice'
import { useSession } from 'next-auth/react'
import { Trophy, Clock, Target, TrendingUp, Code2, Calendar, Play } from 'lucide-react'
import Link from 'next/link'

export default function DashboardPage() {
  const { data: session } = useSession()
  const { data: stats, isLoading: statsLoading } = usePracticeStats()
  const { data: recentHistory, isLoading: historyLoading } = usePracticeHistory({
    per_page: 5,
    completed_only: true
  })

  if (!session?.user) {
    return (
      <div className="container mx-auto py-8 px-4">
        <div className="max-w-2xl mx-auto text-center">
          <h1 className="text-3xl font-bold mb-4">Dashboard</h1>
          <p className="text-muted-foreground mb-6">Please sign in to view your practice statistics.</p>
          <Link href="/auth/signin">
            <Button>Sign In</Button>
          </Link>
        </div>
      </div>
    )
  }

  const formatTime = (seconds: number) => {
    const hours = Math.floor(seconds / 3600)
    const minutes = Math.floor((seconds % 3600) / 60)
    if (hours > 0) {
      return `${hours}h ${minutes}m`
    }
    return `${minutes}m`
  }

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600'
    if (score >= 60) return 'text-yellow-600'
    return 'text-red-600'
  }

  return (
    <div className="container mx-auto py-8 px-4">
      <div className="max-w-6xl mx-auto space-y-6">
        {/* Header */}
        <div className="space-y-2">
          <h1 className="text-4xl font-bold">Dashboard</h1>
          <p className="text-xl text-muted-foreground">
            Welcome back, {session.user.name}! Here&apos;s your practice progress.
          </p>
        </div>

        {/* Overview Stats */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Sessions</CardTitle>
              <Code2 className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {statsLoading ? '-' : stats?.total_sessions || 0}
              </div>
              <p className="text-xs text-muted-foreground">
                Practice sessions completed
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Average Score</CardTitle>
              <Trophy className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className={`text-2xl font-bold ${getScoreColor(stats?.average_score || 0)}`}>
                {statsLoading ? '-' : Math.round(stats?.average_score || 0)}
              </div>
              <p className="text-xs text-muted-foreground">
                Out of 100 points
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Practice Time</CardTitle>
              <Clock className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {statsLoading ? '-' : formatTime(stats?.total_practice_time || 0)}
              </div>
              <p className="text-xs text-muted-foreground">
                Total time spent
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Accuracy</CardTitle>
              <Target className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-blue-600">
                {statsLoading ? '-' : Math.round((stats?.average_accuracy || 0) * 100)}%
              </div>
              <p className="text-xs text-muted-foreground">
                Average accuracy
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Language Progress */}
        {stats?.languages && Object.keys(stats.languages).length > 0 && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <TrendingUp className="w-5 h-5" />
                Progress by Language
              </CardTitle>
              <CardDescription>
                Your performance across different programming languages
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {Object.entries(stats.languages).map(([language, langStats]) => (
                <div key={language} className="space-y-2">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Badge variant="outline">
                        {language.charAt(0).toUpperCase() + language.slice(1)}
                      </Badge>
                      <span className="text-sm text-muted-foreground">
                        {langStats.sessions} session{langStats.sessions !== 1 ? 's' : ''}
                      </span>
                    </div>
                    <div className="text-right">
                      <div className={`font-medium ${getScoreColor(langStats.avg_score)}`}>
                        {Math.round(langStats.avg_score)} pts
                      </div>
                      <div className="text-sm text-muted-foreground">
                        {Math.round(langStats.avg_accuracy * 100)}% acc
                      </div>
                    </div>
                  </div>
                  <Progress value={langStats.avg_score} className="h-2" />
                </div>
              ))}
            </CardContent>
          </Card>
        )}

        {/* Recent Activity */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Calendar className="w-5 h-5" />
                Recent Sessions
              </CardTitle>
              <CardDescription>
                Your latest practice activity
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              {historyLoading ? (
                <div className="space-y-3">
                  {Array.from({ length: 3 }).map((_, i) => (
                    <div key={i} className="animate-pulse space-y-2">
                      <div className="h-4 bg-muted rounded w-3/4"></div>
                      <div className="h-3 bg-muted rounded w-1/2"></div>
                    </div>
                  ))}
                </div>
              ) : recentHistory?.sessions?.length === 0 ? (
                <div className="text-center py-6">
                  <Code2 className="w-8 h-8 mx-auto text-muted-foreground mb-2" />
                  <p className="text-sm text-muted-foreground">No practice sessions yet</p>
                  <Link href="/practice">
                    <Button size="sm" className="mt-2">
                      <Play className="w-4 h-4 mr-2" />
                      Start Practicing
                    </Button>
                  </Link>
                </div>
              ) : (
                recentHistory?.sessions?.map((session) => (
                  <div key={session.session_id} className="border rounded-lg p-3 space-y-2">
                    <div className="flex items-center justify-between">
                      <h4 className="font-medium line-clamp-1">{session.snippet_title}</h4>
                      <Badge variant="outline" className="flex items-center gap-1">
                        <Target className="w-3 h-3" />
                        {session.difficulty}/10
                      </Badge>
                    </div>
                    <div className="flex items-center justify-between text-sm">
                      <div className="flex items-center gap-2">
                        <Badge variant="secondary">{session.language}</Badge>
                        {session.snippet_type === 'official' && (
                          <Badge className="bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200">
                            Official
                          </Badge>
                        )}
                      </div>
                      {session.total_score && (
                        <span className={`font-medium ${getScoreColor(session.total_score)}`}>
                          {Math.round(session.total_score)} pts
                        </span>
                      )}
                    </div>
                    <div className="flex items-center justify-between text-xs text-muted-foreground">
                      <span>
                        {session.time_taken ? formatTime(session.time_taken) : 'N/A'}
                      </span>
                      <span>
                        {new Date(session.completed_at || session.created_at).toLocaleDateString()}
                      </span>
                    </div>
                  </div>
                ))
              )}
              
              {recentHistory?.sessions && recentHistory.sessions.length > 0 && (
                <div className="pt-3 border-t">
                  <Link href="/practice/history">
                    <Button variant="outline" size="sm" className="w-full">
                      View All Sessions
                    </Button>
                  </Link>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Quick Actions */}
          <Card>
            <CardHeader>
              <CardTitle>Quick Actions</CardTitle>
              <CardDescription>
                Jump into practice or explore your progress
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              <Link href="/practice">
                <Button className="w-full justify-start">
                  <Play className="w-4 h-4 mr-2" />
                  Start Practice Session
                </Button>
              </Link>
              
              <Link href="/leaderboard">
                <Button variant="outline" className="w-full justify-start">
                  <Trophy className="w-4 h-4 mr-2" />
                  View Leaderboard
                </Button>
              </Link>
              
              <Link href="/snippets">
                <Button variant="outline" className="w-full justify-start">
                  <Code2 className="w-4 h-4 mr-2" />
                  Browse Snippets
                </Button>
              </Link>
              
              {stats && stats.total_sessions > 0 && (
                <div className="pt-3 border-t space-y-2">
                  <h4 className="font-medium text-sm">Next Goal</h4>
                  <div className="space-y-1">
                    {stats.average_score < 80 ? (
                      <>
                        <p className="text-sm text-muted-foreground">
                          Reach 80+ average score
                        </p>
                        <Progress value={(stats.average_score / 80) * 100} className="h-2" />
                      </>
                    ) : stats.total_sessions < 50 ? (
                      <>
                        <p className="text-sm text-muted-foreground">
                          Complete 50 practice sessions
                        </p>
                        <Progress value={(stats.total_sessions / 50) * 100} className="h-2" />
                      </>
                    ) : (
                      <p className="text-sm text-green-600 font-medium">
                        🎉 You&apos;re doing great! Keep practicing to maintain your skills.
                      </p>
                    )}
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* No Stats Encouragement */}
        {!statsLoading && (!stats || stats.total_sessions === 0) && (
          <Card>
            <CardContent className="py-12 text-center">
              <Code2 className="w-16 h-16 mx-auto text-muted-foreground mb-4" />
              <h3 className="text-xl font-semibold mb-2">Ready to Start Your Coding Journey?</h3>
              <p className="text-muted-foreground mb-6 max-w-md mx-auto">
                Complete your first practice session to see your statistics and track your progress over time.
              </p>
              <Link href="/practice">
                <Button size="lg" className="px-8">
                  <Play className="w-5 h-5 mr-2" />
                  Start Your First Session
                </Button>
              </Link>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  )
}