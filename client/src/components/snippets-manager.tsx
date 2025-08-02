'use client'

import { useState, useEffect, useCallback } from 'react'
import { apiClient, type PersonalSnippet, type OfficialSnippet, type SnippetFilters } from '@/lib/api-client'
import { SnippetCard } from './snippet-card'
import { CreateSnippetModal } from './create-snippet-modal'
import { SearchAndFilters } from './search-and-filters'

interface SnippetsManagerProps {
  accessToken: string
  refreshToken: string
  userRole?: string
}

type ActiveTab = 'personal' | 'official'

export function SnippetsManager({ accessToken, refreshToken }: SnippetsManagerProps) {
  const [activeTab, setActiveTab] = useState<ActiveTab>('personal')
  const [personalSnippets, setPersonalSnippets] = useState<PersonalSnippet[]>([])
  const [officialSnippets, setOfficialSnippets] = useState<OfficialSnippet[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [filters, setFilters] = useState<SnippetFilters>({})
  const [filtersExpanded, setFiltersExpanded] = useState(false)

  const loadSnippets = useCallback(async () => {
    try {
      setLoading(true)
      setError(null)

      if (activeTab === 'personal') {
        const response = await apiClient.getPersonalSnippets(accessToken, refreshToken)
        setPersonalSnippets(response.snippets)
      } else {
        const response = await apiClient.getOfficialSnippets(filters)
        setOfficialSnippets(response.snippets)
      }
    } catch (err) {
      if (err instanceof Error && err.message.includes('Session expired')) {
        return
      }
      console.error('Failed to load snippets:', err)
      setError(err instanceof Error ? err.message : 'Failed to load snippets')
    } finally {
      setLoading(false)
    }
  }, [activeTab, filters, accessToken, refreshToken])

  // Load snippets based on active tab
  useEffect(() => {
    loadSnippets()
  }, [loadSnippets])

  const handleSnippetCreated = (snippet: PersonalSnippet) => {
    setPersonalSnippets(prev => [snippet, ...prev])
    setShowCreateModal(false)
  }

  const handleSnippetUpdated = (updatedSnippet: PersonalSnippet) => {
    setPersonalSnippets(prev => 
      prev.map(snippet => 
        snippet._id === updatedSnippet._id ? updatedSnippet : snippet
      )
    )
  }

  const handleSnippetDeleted = (deletedId: string) => {
    setPersonalSnippets(prev => prev.filter(snippet => snippet._id !== deletedId))
  }

  const currentSnippets = activeTab === 'personal' ? personalSnippets : officialSnippets

  return (
    <div className="space-y-6">
      {/* Tab Navigation - Centered with Filters */}
      <div className="flex flex-col items-center space-y-4">
        <div className="flex items-center space-x-4">
          <div className="flex space-x-1 bg-muted p-1 rounded-lg">
            <button
              onClick={() => setActiveTab('personal')}
              className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                activeTab === 'personal'
                  ? 'bg-background text-foreground shadow-sm'
                  : 'text-muted-foreground hover:text-foreground'
              }`}
            >
              My Snippets
            </button>
            <button
              onClick={() => setActiveTab('official')}
              className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                activeTab === 'official'
                  ? 'bg-background text-foreground shadow-sm'
                  : 'text-muted-foreground hover:text-foreground'
              }`}
            >
              Official Library
            </button>
          </div>

          {/* Filters Toggle moved here */}
          <button
            onClick={() => setFiltersExpanded(!filtersExpanded)}
            className="flex items-center space-x-2 text-sm text-muted-foreground hover:text-foreground transition-colors"
          >
            <svg 
              className={`w-4 h-4 transition-transform ${filtersExpanded ? 'rotate-180' : ''}`} 
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
            <span>Filters</span>
            {Object.keys(filters).length > 0 && (
              <span className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-foreground text-background">
                {Object.keys(filters).length}
              </span>
            )}
          </button>
        </div>

        {activeTab === 'personal' && (
          <button
            onClick={() => setShowCreateModal(true)}
            className="bg-foreground text-background px-4 py-2 rounded-lg font-medium hover:bg-foreground/90 transition-colors"
          >
            + Create Snippet
          </button>
        )}
      </div>

      {/* Filter Controls */}
      {filtersExpanded && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 p-4 bg-muted/30 rounded-lg">
          {/* Language Filter */}
          <div>
            <label className="block text-sm font-medium text-foreground mb-2">
              Language
            </label>
            <select
              value={filters.language || ''}
              onChange={(e) => {
                const newFilters = { ...filters }
                if (e.target.value === '') {
                  delete newFilters.language
                } else {
                  newFilters.language = e.target.value
                }
                setFilters(newFilters)
              }}
              className="w-full px-3 py-2 border border-border rounded-md bg-background text-foreground text-sm focus:outline-none focus:ring-2 focus:ring-foreground/20"
            >
              <option value="">All languages</option>
              {['javascript', 'typescript', 'python', 'java', 'c', 'cpp', 'csharp', 'php', 'ruby', 'go', 'rust', 'swift', 'kotlin', 'html', 'css', 'scss', 'sql', 'bash', 'json', 'markdown'].map((lang) => (
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
              onChange={(e) => {
                const newFilters = { ...filters }
                if (e.target.value === '') {
                  delete newFilters.difficulty
                } else {
                  newFilters.difficulty = e.target.value
                }
                setFilters(newFilters)
              }}
              className="w-full px-3 py-2 border border-border rounded-md bg-background text-foreground text-sm focus:outline-none focus:ring-2 focus:ring-foreground/20"
            >
              <option value="">All difficulties</option>
              {['easy', 'medium', 'hard'].map((diff) => (
                <option key={diff} value={diff}>
                  {diff}
                </option>
              ))}
            </select>
          </div>

          {/* Category/Tag Filter */}
          <div>
            <label className="block text-sm font-medium text-foreground mb-2">
              {activeTab === 'official' ? 'Category' : 'Tag'}
            </label>
            {activeTab === 'official' ? (
              <select
                value={filters.tag || ''}
                onChange={(e) => {
                  const newFilters = { ...filters }
                  if (e.target.value === '') {
                    delete newFilters.tag
                  } else {
                    newFilters.tag = e.target.value
                  }
                  setFilters(newFilters)
                }}
                className="w-full px-3 py-2 border border-border rounded-md bg-background text-foreground text-sm focus:outline-none focus:ring-2 focus:ring-foreground/20"
              >
                <option value="">All categories</option>
                {['algorithms', 'data-structures', 'frontend', 'backend', 'database', 'api', 'testing', 'deployment', 'security', 'utilities'].map((cat) => (
                  <option key={cat} value={cat}>
                    {cat}
                  </option>
                ))}
              </select>
            ) : (
              <input
                type="text"
                placeholder="Enter tag name"
                value={filters.tag || ''}
                onChange={(e) => {
                  const newFilters = { ...filters }
                  if (e.target.value === '') {
                    delete newFilters.tag
                  } else {
                    newFilters.tag = e.target.value
                  }
                  setFilters(newFilters)
                }}
                className="w-full px-3 py-2 border border-border rounded-md bg-background text-foreground text-sm placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-foreground/20"
              />
            )}
          </div>

          {/* Clear Filters */}
          {Object.keys(filters).length > 0 && (
            <div className="flex items-end">
              <button
                onClick={() => setFilters({})}
                className="px-3 py-2 text-sm text-muted-foreground hover:text-foreground transition-colors border border-border rounded-md hover:bg-foreground/5"
              >
                Clear all
              </button>
            </div>
          )}
        </div>
      )}

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
          onChange={(e) => {
            const newFilters = { ...filters }
            if (e.target.value === '') {
              delete newFilters.search
            } else {
              newFilters.search = e.target.value
            }
            setFilters(newFilters)
          }}
          className="block w-full pl-10 pr-12 py-3 border border-border rounded-lg bg-background text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-foreground/20 focus:border-foreground/20"
        />
        {filters.search && (
          <button
            onClick={() => {
              const newFilters = { ...filters }
              delete newFilters.search
              setFilters(newFilters)
            }}
            className="absolute inset-y-0 right-0 pr-3 flex items-center text-muted-foreground hover:text-foreground"
          >
            <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        )}
      </div>

      {/* Loading State */}
      {loading && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <div key={i} className="bg-background border border-border rounded-xl p-6 space-y-4">
              <div className="flex items-center justify-between">
                <div className="w-32 h-5 bg-foreground/10 rounded animate-pulse"></div>
                <div className="w-16 h-4 bg-foreground/10 rounded animate-pulse"></div>
              </div>
              <div className="w-full h-4 bg-foreground/10 rounded animate-pulse"></div>
              <div className="w-24 h-6 bg-foreground/10 rounded animate-pulse"></div>
              <div className="w-full h-32 bg-foreground/10 rounded animate-pulse"></div>
            </div>
          ))}
        </div>
      )}

      {/* Error State */}
      {error && !loading && (
        <div className="text-center py-12">
          <div className="max-w-md mx-auto space-y-4">
            <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto">
              <svg className="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-foreground">Unable to load snippets</h3>
              <p className="text-sm text-muted-foreground mt-1">{error}</p>
              <button
                onClick={loadSnippets}
                className="mt-3 px-4 py-2 bg-foreground text-background rounded-lg hover:bg-foreground/90 transition-colors"
              >
                Try Again
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Empty State */}
      {!loading && !error && currentSnippets.length === 0 && (
        <div className="text-center py-12">
          <div className="max-w-md mx-auto space-y-4">
            <div className="w-16 h-16 bg-foreground/10 rounded-full flex items-center justify-center mx-auto">
              <svg className="w-8 h-8 text-muted-foreground" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-foreground">
                {activeTab === 'personal' ? 'No personal snippets yet' : 'No snippets found'}
              </h3>
              <p className="text-sm text-muted-foreground mt-1">
                {activeTab === 'personal' 
                  ? 'Create your first code snippet to get started'
                  : 'Try adjusting your search filters'
                }
              </p>
              {activeTab === 'personal' && (
                <button
                  onClick={() => setShowCreateModal(true)}
                  className="mt-3 px-4 py-2 bg-foreground text-background rounded-lg hover:bg-foreground/90 transition-colors"
                >
                  Create Your First Snippet
                </button>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Snippets Grid */}
      {!loading && !error && currentSnippets.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {currentSnippets.map((snippet) => (
            <SnippetCard
              key={snippet._id}
              snippet={snippet}
              type={activeTab}
              accessToken={accessToken}
              refreshToken={refreshToken}
              onUpdated={activeTab === 'personal' ? handleSnippetUpdated : undefined}
              onDeleted={activeTab === 'personal' ? handleSnippetDeleted : undefined}
            />
          ))}
        </div>
      )}

      {/* Create Snippet Modal */}
      {showCreateModal && (
        <CreateSnippetModal
          accessToken={accessToken}
          refreshToken={refreshToken}
          onCreated={handleSnippetCreated}
          onClose={() => setShowCreateModal(false)}
        />
      )}
    </div>
  )
}