"use client"

import { useState, useEffect, useCallback } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { MaskedCodeEditor } from './masked-code-editor'
import { Timer } from './timer'
import { ScoreDisplay } from './score-display'
import { Play, Pause, RotateCcw, Send, Target, Code2 } from 'lucide-react'
import { toast } from 'sonner'

interface PracticeSessionProps {
  session: {
    session_id: string
    snippet_id: string
    snippet_title: string
    language: 'python' | 'javascript'
    difficulty: number
    masked_code: string
    answer_count: number
    max_time: number
    created_at: string
  }
  onSubmit: (answers: string[], timeSpent: number) => Promise<void>
  onCancel: () => void
}

type SessionState = 'idle' | 'running' | 'paused' | 'completed' | 'submitting'

export function PracticeSession({ session, onSubmit, onCancel }: PracticeSessionProps) {
  const [sessionState, setSessionState] = useState<SessionState>('idle')
  const [answers, setAnswers] = useState<string[]>([])
  const [timeSpent, setTimeSpent] = useState(0)
  const [isTimerActive, setIsTimerActive] = useState(false)
  const [completionPercentage, setCompletionPercentage] = useState(0)

  // Calculate completion percentage
  useEffect(() => {
    if (session.answer_count === 0) return
    
    const filledAnswers = answers.filter(answer => answer.trim().length > 0).length
    const percentage = (filledAnswers / session.answer_count) * 100
    setCompletionPercentage(percentage)
  }, [answers, session.answer_count])

  // Start session
  const startSession = useCallback(() => {
    setSessionState('running')
    setIsTimerActive(true)
    toast.success('Practice session started!')
  }, [])

  // Pause session
  const pauseSession = useCallback(() => {
    setSessionState('paused')
    setIsTimerActive(false)
    toast.info('Session paused')
  }, [])

  // Resume session
  const resumeSession = useCallback(() => {
    setSessionState('running')
    setIsTimerActive(true)
    toast.success('Session resumed')
  }, [])

  // Reset session
  const resetSession = useCallback(() => {
    setSessionState('idle')
    setIsTimerActive(false)
    setAnswers([])
    setTimeSpent(0)
    setCompletionPercentage(0)
    toast.info('Session reset')
  }, [])

  // Submit session
  const submitSession = useCallback(async () => {
    if (answers.filter(a => a.trim()).length === 0) {
      toast.error('Please fill in at least one answer before submitting')
      return
    }

    setSessionState('submitting')
    setIsTimerActive(false)
    
    try {
      await onSubmit(answers, timeSpent)
      setSessionState('completed')
      toast.success('Practice session submitted!')
    } catch {
      setSessionState('running')
      setIsTimerActive(true)
      toast.error('Failed to submit session. Please try again.')
    }
  }, [answers, timeSpent, onSubmit])

  // Handle timer update
  const handleTimerUpdate = useCallback((time: number) => {
    setTimeSpent(time)
    
    // Auto-submit if time limit reached
    if (time >= session.max_time && sessionState === 'running') {
      toast.warning('Time limit reached! Auto-submitting...')
      submitSession()
    }
  }, [session.max_time, sessionState, submitSession])

  // Handle answers change
  const handleAnswersChange = useCallback((newAnswers: string[]) => {
    setAnswers(newAnswers)
  }, [])

  // Format time display
  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
  }

  // Calculate progress color
  const getProgressColor = () => {
    const timeRatio = timeSpent / session.max_time
    if (timeRatio < 0.5) return 'bg-green-500'
    if (timeRatio < 0.8) return 'bg-yellow-500'
    return 'bg-red-500'
  }

  if (sessionState === 'completed') {
    return (
      <Card className="max-w-4xl mx-auto">
        <CardHeader className="text-center">
          <CardTitle className="text-green-600">Session Completed!</CardTitle>
          <CardDescription>
            Your practice session has been submitted successfully
          </CardDescription>
        </CardHeader>
        <CardContent>
          <ScoreDisplay 
            timeSpent={timeSpent}
            maxTime={session.max_time}
            answersCount={answers.filter(a => a.trim()).length}
            totalAnswers={session.answer_count}
          />
        </CardContent>
      </Card>
    )
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Session Header */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center gap-2">
                <Code2 className="w-5 h-5" />
                {session.snippet_title}
              </CardTitle>
              <CardDescription className="flex items-center gap-4 mt-2">
                <Badge variant="outline" className="flex items-center gap-1">
                  <Target className="w-3 h-3" />
                  Difficulty {session.difficulty}/10
                </Badge>
                <Badge variant="outline">
                  {session.language}
                </Badge>
                <Badge variant="outline">
                  {session.answer_count} blanks
                </Badge>
              </CardDescription>
            </div>
            <div className="text-right space-y-2">
              <Timer
                isActive={isTimerActive}
                maxTime={session.max_time}
                onTimeUpdate={handleTimerUpdate}
                className="text-lg font-mono"
              />
              <div className="text-sm text-muted-foreground">
                {Math.round(completionPercentage)}% complete
              </div>
            </div>
          </div>
        </CardHeader>
      </Card>

      {/* Progress Bar */}
      <div className="space-y-2">
        <div className="flex justify-between text-sm">
          <span>Progress</span>
          <span>{Math.round(completionPercentage)}%</span>
        </div>
        <Progress value={completionPercentage} className="h-2" />
        
        <div className="flex justify-between text-sm">
          <span>Time</span>
          <span className={timeSpent / session.max_time > 0.8 ? 'text-red-500' : ''}>
            {formatTime(timeSpent)} / {formatTime(session.max_time)}
          </span>
        </div>
        <div className="w-full bg-muted rounded-full h-1">
          <div 
            className={`h-1 rounded-full transition-all ${getProgressColor()}`}
            style={{ width: `${Math.min(100, (timeSpent / session.max_time) * 100)}%` }}
          />
        </div>
      </div>

      {/* Code Editor */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Complete the Code</CardTitle>
          <CardDescription>
            Fill in the blanks to complete the code snippet
          </CardDescription>
        </CardHeader>
        <CardContent>
          <MaskedCodeEditor
            maskedCode={session.masked_code}
            language={session.language}
            onAnswersChange={handleAnswersChange}
            readOnly={sessionState === 'submitting'}
          />
        </CardContent>
      </Card>

      {/* Controls */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              {sessionState === 'idle' && (
                <Button onClick={startSession} className="flex items-center gap-2">
                  <Play className="w-4 h-4" />
                  Start Session
                </Button>
              )}
              
              {sessionState === 'running' && (
                <Button onClick={pauseSession} variant="outline" className="flex items-center gap-2">
                  <Pause className="w-4 h-4" />
                  Pause
                </Button>
              )}
              
              {sessionState === 'paused' && (
                <Button onClick={resumeSession} className="flex items-center gap-2">
                  <Play className="w-4 h-4" />
                  Resume
                </Button>
              )}

              {(sessionState === 'running' || sessionState === 'paused') && (
                <Button onClick={resetSession} variant="outline" className="flex items-center gap-2">
                  <RotateCcw className="w-4 h-4" />
                  Reset
                </Button>
              )}
            </div>

            <div className="flex items-center gap-2">
              <Button onClick={onCancel} variant="outline">
                Cancel
              </Button>
              
              {(sessionState === 'running' || sessionState === 'paused' || sessionState === 'submitting') && (
                <Button 
                  onClick={submitSession}
                  disabled={sessionState === 'submitting' || completionPercentage === 0}
                  className="flex items-center gap-2"
                >
                  <Send className="w-4 h-4" />
                  {sessionState === 'submitting' ? 'Submitting...' : 'Submit'}
                </Button>
              )}
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}