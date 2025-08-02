'use client'

import { useState } from 'react'
import type { PersonalSnippet, OfficialSnippet } from '@/lib/api-client'

interface ViewSnippetModalProps {
  snippet: PersonalSnippet | OfficialSnippet
  type: 'personal' | 'official'
  onClose: () => void
}

const LANGUAGE_COLORS: Record<string, string> = {
  javascript: 'bg-yellow-500',
  typescript: 'bg-blue-500',
  python: 'bg-green-500',
  java: 'bg-orange-500',
  c: 'bg-gray-500',
  cpp: 'bg-purple-500',
  csharp: 'bg-purple-600',
  php: 'bg-indigo-500',
  ruby: 'bg-red-500',
  go: 'bg-cyan-500',
  rust: 'bg-orange-600',
  swift: 'bg-orange-400',
  kotlin: 'bg-purple-400',
  html: 'bg-orange-500',
  css: 'bg-blue-400',
  scss: 'bg-pink-500',
  sql: 'bg-blue-600',
  bash: 'bg-gray-700',
  json: 'bg-gray-400',
  markdown: 'bg-gray-600',
}

const DIFFICULTY_COLORS: Record<string, string> = {
  easy: 'bg-green-100 text-green-800',
  medium: 'bg-yellow-100 text-yellow-800',
  hard: 'bg-red-100 text-red-800',
}

export function ViewSnippetModal({ snippet, type, onClose }: ViewSnippetModalProps) {
  const [copied, setCopied] = useState(false)

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(snippet.code)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (err) {
      console.error('Failed to copy code:', err)
    }
  }

  const isOfficial = type === 'official'
  const officialSnippet = isOfficial ? snippet as OfficialSnippet : null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div className="bg-background border border-border rounded-xl p-6 w-full max-w-4xl max-h-[90vh] overflow-y-auto m-4">
        <div className="flex items-start justify-between mb-6">
          <div className="flex-1 min-w-0">
            <h2 className="text-2xl font-semibold text-foreground mb-2">{snippet.title}</h2>
            {snippet.description && (
              <p className="text-muted-foreground">{snippet.description}</p>
            )}
          </div>
          <button
            onClick={onClose}
            className="p-2 text-muted-foreground hover:text-foreground transition-colors ml-4"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Metadata */}
        <div className="flex flex-wrap items-center gap-3 mb-6 pb-4 border-b border-border">
          {/* Language */}
          <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium text-white ${
            LANGUAGE_COLORS[snippet.language] || 'bg-gray-500'
          }`}>
            {snippet.language}
          </span>

          {/* Difficulty */}
          <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
            DIFFICULTY_COLORS[snippet.difficulty] || 'bg-gray-100 text-gray-800'
          }`}>
            {snippet.difficulty}
          </span>

          {/* Category (Official snippets only) */}
          {isOfficial && officialSnippet?.category && (
            <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800">
              {officialSnippet.category}
            </span>
          )}

          {/* Estimated Time (Official snippets only) */}
          {isOfficial && officialSnippet?.estimatedTime && (
            <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-purple-100 text-purple-800">
              ~{officialSnippet.estimatedTime} min
            </span>
          )}

          {/* Created Date */}
          <span className="text-sm text-muted-foreground">
            Created {new Date(snippet.createdAt).toLocaleDateString()}
          </span>
        </div>

        {/* Tags */}
        {snippet.tags && snippet.tags.length > 0 && (
          <div className="mb-6">
            <h3 className="text-sm font-medium text-foreground mb-2">Tags</h3>
            <div className="flex flex-wrap gap-2">
              {snippet.tags.map((tag, index) => (
                <span
                  key={index}
                  className="inline-flex items-center px-2 py-1 rounded-md text-xs bg-foreground/10 text-foreground"
                >
                  #{tag}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Learning Objectives (Official snippets only) */}
        {isOfficial && officialSnippet?.learningObjectives && officialSnippet.learningObjectives.length > 0 && (
          <div className="mb-6">
            <h3 className="text-sm font-medium text-foreground mb-2">Learning Objectives</h3>
            <ul className="list-disc list-inside space-y-1 text-sm text-muted-foreground">
              {officialSnippet.learningObjectives.map((objective, index) => (
                <li key={index}>{objective}</li>
              ))}
            </ul>
          </div>
        )}

        {/* Hints (Official snippets only) */}
        {isOfficial && officialSnippet?.hints && (
          <div className="mb-6">
            <h3 className="text-sm font-medium text-foreground mb-2">Hints</h3>
            <p className="text-sm text-muted-foreground bg-blue-50 p-3 rounded-md border border-blue-200">
              {officialSnippet.hints}
            </p>
          </div>
        )}

        {/* Code */}
        <div className="mb-6">
          <div className="flex items-center justify-between mb-3">
            <h3 className="text-sm font-medium text-foreground">Code</h3>
            <button
              onClick={copyToClipboard}
              className="flex items-center space-x-2 px-3 py-1 text-sm bg-foreground/10 hover:bg-foreground/20 text-foreground rounded-md transition-colors"
            >
              {copied ? (
                <>
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <span>Copied!</span>
                </>
              ) : (
                <>
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                  </svg>
                  <span>Copy</span>
                </>
              )}
            </button>
          </div>
          <div className="bg-muted/50 rounded-lg p-4 border border-border">
            <pre className="text-sm text-foreground font-mono overflow-x-auto">
              <code>{snippet.code}</code>
            </pre>
          </div>
        </div>

        {/* Solution (Official snippets only) */}
        {isOfficial && officialSnippet?.solution && (
          <div className="mb-6">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-sm font-medium text-foreground">Solution</h3>
              <button
                onClick={() => navigator.clipboard.writeText(officialSnippet.solution)}
                className="flex items-center space-x-2 px-3 py-1 text-sm bg-foreground/10 hover:bg-foreground/20 text-foreground rounded-md transition-colors"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                </svg>
                <span>Copy Solution</span>
              </button>
            </div>
            <div className="bg-green-50 rounded-lg p-4 border border-green-200">
              <pre className="text-sm text-foreground font-mono overflow-x-auto">
                <code>{officialSnippet.solution}</code>
              </pre>
            </div>
          </div>
        )}

        {/* Statistics (Official snippets only) */}
        {isOfficial && (
          <div className="mb-6">
            <h3 className="text-sm font-medium text-foreground mb-3">Statistics</h3>
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-muted/30 rounded-lg p-3">
                <div className="text-lg font-semibold text-foreground">
                  {officialSnippet?.practiceCount || 0}
                </div>
                <div className="text-sm text-muted-foreground">Practice attempts</div>
              </div>
              <div className="bg-muted/30 rounded-lg p-3">
                <div className="text-lg font-semibold text-foreground">
                  {officialSnippet?.averageScore || 0}%
                </div>
                <div className="text-sm text-muted-foreground">Average score</div>
              </div>
            </div>
          </div>
        )}

        {/* Actions */}
        <div className="flex justify-end space-x-3 pt-4 border-t border-border">
          <button
            onClick={onClose}
            className="px-4 py-2 text-foreground border border-border rounded-md hover:bg-foreground/5 transition-colors"
          >
            Close
          </button>
          {isOfficial && (
            <button
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
              onClick={() => {
                // TODO: Implement practice mode
                alert('Practice mode coming in Phase 3!')
              }}
            >
              Start Practice
            </button>
          )}
        </div>
      </div>
    </div>
  )
}