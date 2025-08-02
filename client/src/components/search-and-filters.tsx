'use client'

import { useState } from 'react'
import type { SnippetFilters } from '@/lib/api-client'

interface SearchAndFiltersProps {
  filters: SnippetFilters
  onFiltersChange: (filters: SnippetFilters) => void
  showCategory?: boolean
}

const LANGUAGES = [
  'javascript', 'typescript', 'python', 'java', 'c', 'cpp', 'csharp',
  'php', 'ruby', 'go', 'rust', 'swift', 'kotlin', 'html', 'css',
  'scss', 'sql', 'bash', 'json', 'markdown'
]

const DIFFICULTIES = ['easy', 'medium', 'hard']

const CATEGORIES = [
  'algorithms', 'data-structures', 'frontend', 'backend', 'database',
  'api', 'testing', 'deployment', 'security', 'utilities'
]

export function SearchAndFilters({ filters, onFiltersChange, showCategory = false }: SearchAndFiltersProps) {
  const [isExpanded, setIsExpanded] = useState(false)

  const updateFilter = (key: keyof SnippetFilters, value: string) => {
    const newFilters = { ...filters }
    if (value === '') {
      delete newFilters[key]
    } else {
      newFilters[key] = value
    }
    onFiltersChange(newFilters)
  }

  const clearFilters = () => {
    onFiltersChange({})
  }

  const hasActiveFilters = Object.keys(filters).length > 0

  return (
    <div className="space-y-4">
      {/* Search Bar */}
      <div className="relative">
        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <svg className="h-5 w-5 text-muted-foreground" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
        <input
          type="text"
          placeholder="Search snippets by title or description..."
          value={filters.search || ''}
          onChange={(e) => updateFilter('search', e.target.value)}
          className="block w-full pl-10 pr-12 py-3 border border-border rounded-lg bg-background text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-foreground/20 focus:border-foreground/20"
        />
        {filters.search && (
          <button
            onClick={() => updateFilter('search', '')}
            className="absolute inset-y-0 right-0 pr-3 flex items-center text-muted-foreground hover:text-foreground"
          >
            <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        )}
      </div>

      {/* Filter Toggle */}
      <div className="flex items-center justify-between">
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="flex items-center space-x-2 text-sm text-muted-foreground hover:text-foreground transition-colors"
        >
          <svg 
            className={`w-4 h-4 transition-transform ${isExpanded ? 'rotate-180' : ''}`} 
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
          <span>Filters</span>
          {hasActiveFilters && (
            <span className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-foreground text-background">
              {Object.keys(filters).length}
            </span>
          )}
        </button>

        {hasActiveFilters && (
          <button
            onClick={clearFilters}
            className="text-sm text-muted-foreground hover:text-foreground transition-colors"
          >
            Clear all
          </button>
        )}
      </div>

      {/* Filter Controls */}
      {isExpanded && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 p-4 bg-muted/30 rounded-lg">
          {/* Language Filter */}
          <div>
            <label className="block text-sm font-medium text-foreground mb-2">
              Language
            </label>
            <select
              value={filters.language || ''}
              onChange={(e) => updateFilter('language', e.target.value)}
              className="w-full px-3 py-2 border border-border rounded-md bg-background text-foreground text-sm focus:outline-none focus:ring-2 focus:ring-foreground/20"
            >
              <option value="">All languages</option>
              {LANGUAGES.map((lang) => (
                <option key={lang} value={lang}>
                  {lang}
                </option>
              ))}
            </select>
          </div>

          {/* Difficulty Filter */}
          <div>
            <label className="block text-sm font-medium text-foreground mb-2">
              Difficulty
            </label>
            <select
              value={filters.difficulty || ''}
              onChange={(e) => updateFilter('difficulty', e.target.value)}
              className="w-full px-3 py-2 border border-border rounded-md bg-background text-foreground text-sm focus:outline-none focus:ring-2 focus:ring-foreground/20"
            >
              <option value="">All difficulties</option>
              {DIFFICULTIES.map((diff) => (
                <option key={diff} value={diff}>
                  {diff}
                </option>
              ))}
            </select>
          </div>

          {/* Category Filter (only for official snippets) */}
          {showCategory && (
            <div>
              <label className="block text-sm font-medium text-foreground mb-2">
                Category
              </label>
              <select
                value={filters.tag || ''}
                onChange={(e) => updateFilter('tag', e.target.value)}
                className="w-full px-3 py-2 border border-border rounded-md bg-background text-foreground text-sm focus:outline-none focus:ring-2 focus:ring-foreground/20"
              >
                <option value="">All categories</option>
                {CATEGORIES.map((cat) => (
                  <option key={cat} value={cat}>
                    {cat}
                  </option>
                ))}
              </select>
            </div>
          )}

          {/* Tag Filter (for personal snippets) */}
          {!showCategory && (
            <div>
              <label className="block text-sm font-medium text-foreground mb-2">
                Tag
              </label>
              <input
                type="text"
                placeholder="Enter tag name"
                value={filters.tag || ''}
                onChange={(e) => updateFilter('tag', e.target.value)}
                className="w-full px-3 py-2 border border-border rounded-md bg-background text-foreground text-sm placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-foreground/20"
              />
            </div>
          )}
        </div>
      )}
    </div>
  )
}