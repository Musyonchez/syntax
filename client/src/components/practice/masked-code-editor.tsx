"use client"

import { useState, useEffect, useCallback } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { Check, X, RotateCcw } from 'lucide-react'

interface MaskedCodeEditorProps {
  maskedCode: string
  language: 'python' | 'javascript'
  onAnswersChange: (answers: string[]) => void
  readOnly?: boolean
  showResults?: boolean
  correctAnswers?: string[]
  userAnswers?: string[]
  className?: string
}

interface BlankInfo {
  id: number
  placeholder: string
  answer: string
  isCorrect?: boolean
  similarity?: number
}

export function MaskedCodeEditor({
  maskedCode,
  language,
  onAnswersChange,
  readOnly = false,
  showResults = false,
  correctAnswers = [],
  userAnswers = [],
  className = ""
}: MaskedCodeEditorProps) {
  const [blanks, setBlanks] = useState<BlankInfo[]>([])
  const [answers, setAnswers] = useState<string[]>([])

  // Parse masked code to find blanks
  useEffect(() => {
    const blankPattern = /_{1,}/g
    const matches = Array.from(maskedCode.matchAll(blankPattern))
    
    const parsedBlanks: BlankInfo[] = matches.map((match, index) => ({
      id: index,
      placeholder: match[0],
      answer: userAnswers[index] || '',
      isCorrect: showResults ? (correctAnswers[index] ? 
        (userAnswers[index]?.toLowerCase().trim() === correctAnswers[index]?.toLowerCase().trim()) : false
      ) : undefined,
      similarity: showResults && correctAnswers[index] ? 
        calculateSimilarity(userAnswers[index] || '', correctAnswers[index]) : undefined
    }))
    
    setBlanks(parsedBlanks)
    setAnswers(userAnswers.length > 0 ? userAnswers : new Array(parsedBlanks.length).fill(''))
  }, [maskedCode, userAnswers, correctAnswers, showResults])

  // Simple similarity calculation
  const calculateSimilarity = (str1: string, str2: string): number => {
    if (!str1 || !str2) return 0
    const a = str1.toLowerCase().trim()
    const b = str2.toLowerCase().trim()
    if (a === b) return 1
    
    // Simple character-based similarity
    const longer = a.length > b.length ? a : b
    const shorter = a.length > b.length ? b : a
    if (longer.length === 0) return 1
    
    let matches = 0
    let j = 0
    for (let i = 0; i < shorter.length; i++) {
      while (j < longer.length && longer[j] !== shorter[i]) j++
      if (j < longer.length) {
        matches++
        j++
      }
    }
    return matches / longer.length
  }

  // Update answer
  const updateAnswer = useCallback((index: number, value: string) => {
    const newAnswers = [...answers]
    newAnswers[index] = value
    setAnswers(newAnswers)
    onAnswersChange(newAnswers)
  }, [answers, onAnswersChange])

  // Clear all answers
  const clearAnswers = useCallback(() => {
    const emptyAnswers = new Array(blanks.length).fill('')
    setAnswers(emptyAnswers)
    onAnswersChange(emptyAnswers)
  }, [blanks.length, onAnswersChange])

  // Render the masked code with input fields
  const renderMaskedCode = () => {
    const parts = maskedCode.split(/_{1,}/)
    const result = []
    
    for (let i = 0; i < parts.length; i++) {
      // Add the code part
      if (parts[i]) {
        result.push(
          <span key={`code-${i}`} className="whitespace-pre">
            {parts[i]}
          </span>
        )
      }
      
      // Add input field for blank (except after the last part)
      if (i < blanks.length) {
        const blank = blanks[i]
        const isCorrect = blank.isCorrect
        const similarity = blank.similarity || 0
        
        result.push(
          <span key={`blank-${i}`} className="inline-block relative">
            <Input
              value={answers[i] || ''}
              onChange={(e) => updateAnswer(i, e.target.value)}
              readOnly={readOnly}
              className={`
                inline-block w-auto min-w-[60px] max-w-[200px] h-8 px-2 text-sm font-mono
                ${showResults ? (
                  isCorrect ? 'border-green-500 bg-green-50 dark:bg-green-950' :
                  similarity > 0.6 ? 'border-yellow-500 bg-yellow-50 dark:bg-yellow-950' :
                  'border-red-500 bg-red-50 dark:bg-red-950'
                ) : 'border-muted-foreground/30'}
              `}
              placeholder={`___`}
              style={{ 
                width: `${Math.max(60, Math.min(200, (answers[i]?.length || 3) * 8 + 20))}px` 
              }}
            />
            {showResults && (
              <div className="absolute -top-6 left-0 flex items-center gap-1">
                {isCorrect ? (
                  <Check className="w-3 h-3 text-green-600" />
                ) : similarity > 0.6 ? (
                  <Badge variant="outline" className="text-xs py-0 px-1">
                    {Math.round(similarity * 100)}%
                  </Badge>
                ) : (
                  <X className="w-3 h-3 text-red-600" />
                )}
              </div>
            )}
          </span>
        )
      }
    }
    
    return result
  }

  return (
    <div className={`space-y-4 ${className}`}>
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Badge variant="outline" className="text-xs">
            {language}
          </Badge>
          <Badge variant="outline" className="text-xs">
            {blanks.length} blank{blanks.length !== 1 ? 's' : ''}
          </Badge>
        </div>
        {!readOnly && !showResults && (
          <Button
            variant="outline"
            size="sm"
            onClick={clearAnswers}
            className="text-xs"
          >
            <RotateCcw className="w-3 h-3 mr-1" />
            Clear
          </Button>
        )}
      </div>
      
      <div className="relative">
        <div className="bg-card border rounded-lg p-4 font-mono text-sm leading-relaxed overflow-x-auto">
          {renderMaskedCode()}
        </div>
      </div>
      
      {showResults && (
        <div className="space-y-2">
          <h4 className="font-medium text-sm">Answer Review:</h4>
          <div className="grid gap-2">
            {blanks.map((blank, index) => (
              <div key={index} className="flex items-center justify-between text-sm border rounded p-2">
                <div className="flex items-center gap-2">
                  <span className="font-medium">#{index + 1}:</span>
                  <span className={`font-mono ${
                    blank.isCorrect ? 'text-green-600' : 'text-red-600'
                  }`}>
                    {answers[index] || '(empty)'}
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  {blank.isCorrect ? (
                    <Badge className="bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200">
                      Correct
                    </Badge>
                  ) : (
                    <div className="flex items-center gap-1">
                      <Badge variant="destructive" className="text-xs">
                        Expected: {correctAnswers[index]}
                      </Badge>
                      {(blank.similarity || 0) > 0.6 && (
                        <Badge variant="outline" className="text-xs">
                          {Math.round((blank.similarity || 0) * 100)}% match
                        </Badge>
                      )}
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}