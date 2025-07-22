"use client"

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { Trophy, Clock, Target, CheckCircle, XCircle } from 'lucide-react'

interface ScoreDisplayProps {
  score?: {
    total_score: number
    accuracy: number
    time_bonus: number
    mistakes: number
    time_taken: number
  }
  timeSpent: number
  maxTime: number
  answersCount: number
  totalAnswers: number
  detailedResults?: Array<{
    position: number
    user_answer: string
    correct_answer: string
    similarity: number
    is_correct: boolean
  }>
  leaderboardEligible?: boolean
}

export function ScoreDisplay({
  score,
  timeSpent,
  maxTime,
  answersCount,
  totalAnswers,
  detailedResults = [],
  leaderboardEligible = false
}: ScoreDisplayProps) {
  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
  }

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600'
    if (score >= 60) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getScoreBadgeVariant = (score: number) => {
    if (score >= 80) return 'default'
    if (score >= 60) return 'secondary'
    return 'destructive'
  }

  return (
    <div className="space-y-6">
      {/* Overall Score */}
      {score && (
        <Card>
          <CardHeader className="text-center">
            <CardTitle className="flex items-center justify-center gap-2">
              <Trophy className="w-5 h-5" />
              Practice Results
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Total Score */}
            <div className="text-center space-y-2">
              <div className={`text-4xl font-bold ${getScoreColor(score.total_score)}`}>
                {Math.round(score.total_score)}
              </div>
              <div className="text-sm text-muted-foreground">out of 100 points</div>
              <Badge variant={getScoreBadgeVariant(score.total_score)} className="text-lg px-3 py-1">
                {score.total_score >= 90 ? 'Excellent!' :
                 score.total_score >= 80 ? 'Great Job!' :
                 score.total_score >= 70 ? 'Good Work!' :
                 score.total_score >= 60 ? 'Not Bad!' :
                 'Keep Practicing!'}
              </Badge>
            </div>

            {/* Score Breakdown */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="text-center space-y-1">
                <div className="text-2xl font-semibold text-blue-600">
                  {Math.round(score.accuracy * 100)}%
                </div>
                <div className="text-xs text-muted-foreground">Accuracy</div>
              </div>
              
              <div className="text-center space-y-1">
                <div className="text-2xl font-semibold text-purple-600">
                  +{Math.round(score.time_bonus * 100)}
                </div>
                <div className="text-xs text-muted-foreground">Time Bonus</div>
              </div>
              
              <div className="text-center space-y-1">
                <div className="text-2xl font-semibold text-green-600">
                  {totalAnswers - score.mistakes}
                </div>
                <div className="text-xs text-muted-foreground">Correct</div>
              </div>
              
              <div className="text-center space-y-1">
                <div className="text-2xl font-semibold text-red-600">
                  {score.mistakes}
                </div>
                <div className="text-xs text-muted-foreground">Mistakes</div>
              </div>
            </div>

            {/* Progress Bars */}
            <div className="space-y-3">
              <div className="space-y-1">
                <div className="flex justify-between text-sm">
                  <span>Accuracy</span>
                  <span>{Math.round(score.accuracy * 100)}%</span>
                </div>
                <Progress value={score.accuracy * 100} className="h-2" />
              </div>
              
              <div className="space-y-1">
                <div className="flex justify-between text-sm">
                  <span>Time Efficiency</span>
                  <span>{Math.round((1 - score.time_taken / maxTime) * 100)}%</span>
                </div>
                <Progress 
                  value={Math.max(0, (1 - score.time_taken / maxTime) * 100)} 
                  className="h-2" 
                />
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Session Summary */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Session Summary</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="flex items-center gap-2">
              <Clock className="w-4 h-4 text-muted-foreground" />
              <div>
                <div className="font-medium">{formatTime(timeSpent)}</div>
                <div className="text-xs text-muted-foreground">Time Taken</div>
              </div>
            </div>
            
            <div className="flex items-center gap-2">
              <Target className="w-4 h-4 text-muted-foreground" />
              <div>
                <div className="font-medium">{answersCount}/{totalAnswers}</div>
                <div className="text-xs text-muted-foreground">Answered</div>
              </div>
            </div>
            
            <div className="flex items-center gap-2">
              <CheckCircle className="w-4 h-4 text-green-600" />
              <div>
                <div className="font-medium">{score ? totalAnswers - score.mistakes : 0}</div>
                <div className="text-xs text-muted-foreground">Correct</div>
              </div>
            </div>
            
            <div className="flex items-center gap-2">
              <XCircle className="w-4 h-4 text-red-600" />
              <div>
                <div className="font-medium">{score?.mistakes || 0}</div>
                <div className="text-xs text-muted-foreground">Incorrect</div>
              </div>
            </div>
          </div>

          {leaderboardEligible && (
            <div className="mt-4 p-3 bg-green-50 dark:bg-green-950 rounded-lg border border-green-200 dark:border-green-800">
              <div className="flex items-center gap-2 text-green-700 dark:text-green-300">
                <Trophy className="w-4 h-4" />
                <span className="text-sm font-medium">
                  This score counts towards the leaderboard!
                </span>
              </div>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Detailed Results */}
      {detailedResults.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Answer Review</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {detailedResults.map((result) => (
                <div
                  key={result.position}
                  className={`p-3 rounded-lg border ${
                    result.is_correct
                      ? 'bg-green-50 border-green-200 dark:bg-green-950 dark:border-green-800'
                      : result.similarity > 0.6
                      ? 'bg-yellow-50 border-yellow-200 dark:bg-yellow-950 dark:border-yellow-800'
                      : 'bg-red-50 border-red-200 dark:bg-red-950 dark:border-red-800'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      {result.is_correct ? (
                        <CheckCircle className="w-4 h-4 text-green-600" />
                      ) : (
                        <XCircle className="w-4 h-4 text-red-600" />
                      )}
                      <span className="font-medium">Blank #{result.position + 1}</span>
                    </div>
                    <div className="text-right">
                      <div className="font-mono text-sm">
                        Your answer: <span className="font-semibold">{result.user_answer || '(empty)'}</span>
                      </div>
                      {!result.is_correct && (
                        <div className="font-mono text-sm text-muted-foreground">
                          Expected: <span className="font-semibold">{result.correct_answer}</span>
                        </div>
                      )}
                      {!result.is_correct && result.similarity > 0.6 && (
                        <Badge variant="outline" className="text-xs">
                          {Math.round(result.similarity * 100)}% match
                        </Badge>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}