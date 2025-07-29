"use client"

import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Input } from '@/components/ui/input'
import { useOfficialSnippets, usePersonalSnippets, useSnippetFilters } from '@/hooks/use-snippets'
import { usePracticeWorkflow } from '@/hooks/use-practice'
import { PracticeSession } from '@/components/practice/practice-session'
import { ScoreDisplay } from '@/components/practice/score-display'
import { Search, Code2, Trophy, User, Filter, Play, Target } from 'lucide-react'
import type { Snippet } from '@/lib/api/snippets'
import type { PracticeSession as PracticeSessionType, PracticeScore } from '@/lib/api/practice'

export default function PracticePage() {
  const [selectedSnippet, setSelectedSnippet] = useState<Snippet | null>(null)
  const [currentSession, setCurrentSession] = useState<PracticeSessionType | null>(null)
  const [sessionResult, setSessionResult] = useState<PracticeScore | null>(null)
  const [practiceMode, setPracticeMode] = useState<'selection' | 'session' | 'results'>('selection')
  
  // Filters
  const [snippetType, setSnippetType] = useState<'official' | 'personal'>('official')
  const [languageFilter, setLanguageFilter] = useState<string>('all')
  const [difficultyFilter, setDifficultyFilter] = useState<string>('all')
  const [searchQuery, setSearchQuery] = useState('')
  
  const { languages, difficulties } = useSnippetFilters()
  const practiceWorkflow = usePracticeWorkflow()
  
  // Fetch snippets based on type and filters
  const officialSnippets = useOfficialSnippets({
    language: languageFilter === 'all' ? undefined : languageFilter,
    difficulty: difficultyFilter === 'all' ? undefined : parseInt(difficultyFilter),
    per_page: 20
  })
  
  const personalSnippets = usePersonalSnippets({
    per_page: 20
  })
  
  const snippetsQuery = snippetType === 'official' ? officialSnippets : personalSnippets
  const snippets = snippetsQuery.data?.snippets || []
  
  // Handle loading and error states
  const isLoading = snippetsQuery.isLoading
  const isError = snippetsQuery.isError
  
  // Filter snippets by search query
  const filteredSnippets = snippets.filter(snippet => 
    snippet.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    snippet.language.toLowerCase().includes(searchQuery.toLowerCase())
  )

  const startPractice = async (snippet: Snippet, customDifficulty?: number) => {
    try {
      setSelectedSnippet(snippet)
      const session = await practiceWorkflow.startSession(
        snippet.id,
        customDifficulty || snippet.difficulty
      )
      setCurrentSession(session)
      setPracticeMode('session')
    } catch (error) {
      console.error('Failed to start practice:', error)
    }
  }

  const submitPractice = async (answers: string[], timeSpent: number) => {
    if (!currentSession) return
    
    try {
      const result = await practiceWorkflow.submitSession(
        currentSession.session_id,
        answers,
        timeSpent
      )
      setSessionResult(result)
      setPracticeMode('results')
    } catch (error) {
      console.error('Failed to submit practice:', error)
      throw error
    }
  }

  const resetPractice = () => {
    setSelectedSnippet(null)
    setCurrentSession(null)
    setSessionResult(null)
    setPracticeMode('selection')
  }

  // Results view
  if (practiceMode === 'results' && sessionResult) {
    return (
      <div className="container mx-auto py-8 px-4">
        <div className="max-w-4xl mx-auto space-y-6">
          <div className="text-center space-y-2">
            <h1 className="text-3xl font-bold">Practice Complete!</h1>
            <p className="text-muted-foreground">
              Great job completing &ldquo;{selectedSnippet?.title}&rdquo;
            </p>
          </div>
          
          <ScoreDisplay
            score={sessionResult}
            timeSpent={sessionResult.time_taken}
            maxTime={currentSession?.max_time || 300}
            answersCount={sessionResult.detailed_results.filter(r => r.user_answer.trim()).length}
            totalAnswers={sessionResult.detailed_results.length}
            detailedResults={sessionResult.detailed_results}
            leaderboardEligible={sessionResult.leaderboard_eligible}
          />
          
          <div className="flex justify-center gap-4">
            <Button onClick={resetPractice}>
              Practice Another
            </Button>
            <Button variant="outline" onClick={() => window.location.href = '/leaderboard'}>
              View Leaderboard
            </Button>
          </div>
        </div>
      </div>
    )
  }

  // Practice session view
  if (practiceMode === 'session' && currentSession) {
    return (
      <div className="container mx-auto py-8 px-4">
        <PracticeSession
          session={currentSession}
          onSubmit={submitPractice}
          onCancel={resetPractice}
        />
      </div>
    )
  }

  // Snippet selection view
  return (
    <div className="container mx-auto py-8 px-4">
      <div className="max-w-6xl mx-auto space-y-6">
        {/* Header */}
        <div className="text-center space-y-4">
          <h1 className="text-4xl font-bold">Practice Mode</h1>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Choose a code snippet to practice with. Fill in the blanks to complete the code and improve your programming skills.
          </p>
        </div>

        {/* Filters */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Filter className="w-5 h-5" />
              Find Your Challenge
            </CardTitle>
            <CardDescription>
              Filter snippets by type, language, and difficulty to find the perfect practice session
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {/* Snippet Type */}
              <div className="space-y-2">
                <label className="text-sm font-medium">Type</label>
                <Select value={snippetType} onValueChange={(value: 'official' | 'personal') => setSnippetType(value)}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="official">
                      <div className="flex items-center gap-2">
                        <Trophy className="w-4 h-4" />
                        Official Snippets
                      </div>
                    </SelectItem>
                    <SelectItem value="personal">
                      <div className="flex items-center gap-2">
                        <User className="w-4 h-4" />
                        Personal Snippets
                      </div>
                    </SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {/* Language and Difficulty - Combined on sm-md, separate on max-sm and md+ */}
              <div className="contents max-sm:contents sm:grid sm:grid-cols-2 sm:gap-4 md:contents">
                {/* Language Filter */}
                <div className="space-y-2">
                  <label className="text-sm font-medium">Language</label>
                  <Select value={languageFilter} onValueChange={setLanguageFilter}>
                    <SelectTrigger>
                      <SelectValue placeholder="All languages" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all">All languages</SelectItem>
                      {languages.map(lang => (
                        <SelectItem key={lang} value={lang}>
                          {lang.charAt(0).toUpperCase() + lang.slice(1)}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                {/* Difficulty Filter */}
                <div className="space-y-2">
                  <label className="text-sm font-medium">Difficulty</label>
                  <Select value={difficultyFilter} onValueChange={setDifficultyFilter}>
                    <SelectTrigger>
                      <SelectValue placeholder="All difficulties" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all">All difficulties</SelectItem>
                      {difficulties.map(diff => (
                        <SelectItem key={diff} value={diff.toString()}>
                          Level {diff}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              </div>

              {/* Search */}
              <div className="space-y-2">
                <label className="text-sm font-medium">Search</label>
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                  <Input
                    placeholder="Search snippets..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="pl-10"
                  />
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Snippets Grid */}
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-semibold">
              {snippetType === 'official' ? 'Official' : 'Personal'} Snippets
            </h2>
            <Badge variant="outline">
              {filteredSnippets.length} snippet{filteredSnippets.length !== 1 ? 's' : ''}
            </Badge>
          </div>

          {isError ? (
            <Card>
              <CardContent className="py-12 text-center">
                <Code2 className="w-12 h-12 mx-auto text-muted-foreground mb-4" />
                <h3 className="text-lg font-medium mb-2">Unable to load snippets</h3>
                <p className="text-muted-foreground mb-4">
                  {snippetType === 'personal' 
                    ? 'Sign in to access your personal code snippets and track your progress.'
                    : 'We\'re having trouble loading the practice snippets right now.'
                  }
                </p>
                <div className="space-y-2 text-sm text-muted-foreground">
                  {snippetType === 'personal' ? (
                    <p>Sign in with your Google account to view and create your own snippets</p>
                  ) : (
                    <p>Please try again in a moment. If the problem persists, our team has been notified.</p>
                  )}
                </div>
                <Button 
                  variant="outline" 
                  onClick={() => snippetsQuery.refetch()}
                  className="mt-4"
                >
                  Try Again
                </Button>
              </CardContent>
            </Card>
          ) : isLoading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {Array.from({ length: 6 }).map((_, i) => (
                <Card key={i} className="animate-pulse">
                  <CardHeader>
                    <div className="h-4 bg-muted rounded w-3/4"></div>
                    <div className="h-3 bg-muted rounded w-1/2"></div>
                  </CardHeader>
                  <CardContent>
                    <div className="h-20 bg-muted rounded"></div>
                  </CardContent>
                </Card>
              ))}
            </div>
          ) : filteredSnippets.length === 0 ? (
            <Card>
              <CardContent className="py-12 text-center">
                <Code2 className="w-12 h-12 mx-auto text-muted-foreground mb-4" />
                <h3 className="text-lg font-medium mb-2">No snippets found</h3>
                <p className="text-muted-foreground">
                  Try adjusting your filters or {snippetType === 'personal' ? 'create a personal snippet' : 'browse different categories'}
                </p>
              </CardContent>
            </Card>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {filteredSnippets.map((snippet) => (
                <Card key={snippet.id} className="hover:shadow-md transition-shadow">
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <CardTitle className="text-lg line-clamp-1">{snippet.title}</CardTitle>
                      <Badge variant="outline" className="flex items-center gap-1">
                        <Target className="w-3 h-3" />
                        {snippet.difficulty}/10
                      </Badge>
                    </div>
                    <CardDescription className="flex items-center gap-2">
                      <Badge variant="secondary">{snippet.language}</Badge>
                      {snippet.type === 'official' && (
                        <Badge className="bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200">
                          <Trophy className="w-3 h-3 mr-1" />
                          Official
                        </Badge>
                      )}
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      <div className="flex items-center justify-between text-sm text-muted-foreground">
                        <span>By {snippet.author_name}</span>
                        <span>{snippet.solve_count} solves</span>
                      </div>
                      
                      <Button
                        onClick={() => startPractice(snippet)}
                        disabled={practiceWorkflow.isStarting}
                        className="w-full"
                      >
                        <Play className="w-4 h-4 mr-2" />
                        {practiceWorkflow.isStarting ? 'Starting...' : 'Start Practice'}
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}