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
      {/* Tab Navigation - Centered */}
      <div className="flex flex-col items-center space-y-4">
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

        {activeTab === 'personal' && (
          <button
            onClick={() => setShowCreateModal(true)}
            className="bg-foreground text-background px-4 py-2 rounded-lg font-medium hover:bg-foreground/90 transition-colors"
          >
            + Create Snippet
          </button>
        )}
      </div>

      {/* Search and Filters */}
      <SearchAndFilters
        filters={filters}
        onFiltersChange={setFilters}
        showCategory={activeTab === 'official'}
      />

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