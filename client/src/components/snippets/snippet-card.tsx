'use client'

import { useState } from 'react'
import { apiClient, type PersonalSnippet, type OfficialSnippet } from '@/lib/api-client'
import { EditSnippetModal } from '../modals/edit-snippet-modal'
import { ViewSnippetModal } from '../modals/view-snippet-modal'
import { ConfirmModal } from '../modals/confirm-modal'

interface SnippetCardProps {
  snippet: PersonalSnippet | OfficialSnippet
  type: 'personal' | 'official'
  accessToken: string
  refreshToken: string
  onUpdated?: (snippet: PersonalSnippet) => void
  onDeleted?: (id: string) => void
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

export function SnippetCard({ snippet, type, accessToken, refreshToken, onUpdated, onDeleted }: SnippetCardProps) {
  const [showEditModal, setShowEditModal] = useState(false)
  const [showViewModal, setShowViewModal] = useState(false)
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false)
  const [isDeleting, setIsDeleting] = useState(false)

  const handleDelete = async () => {
    if (!onDeleted || type !== 'personal') return
    setShowDeleteConfirm(true)
  }

  const confirmDelete = async () => {
    setShowDeleteConfirm(false)
    setIsDeleting(true)
    try {
      await apiClient.deletePersonalSnippet(snippet._id, accessToken, refreshToken)
      onDeleted?.(snippet._id)
    } catch (error) {
      console.error('Failed to delete snippet:', error)
      alert('Failed to delete snippet. Please try again.')
    } finally {
      setIsDeleting(false)
    }
  }

  const cancelDelete = () => {
    setShowDeleteConfirm(false)
  }

  const isOfficial = type === 'official'
  const officialSnippet = isOfficial ? snippet as OfficialSnippet : null
  const personalSnippet = !isOfficial ? snippet as PersonalSnippet : null

  return (
    <div className="bg-background border border-border rounded-xl p-6 flex flex-col hover:shadow-md transition-shadow h-full">
      {/* Card Content - flex-1 to take available space */}
      <div className="flex-1 flex flex-col space-y-4">
        {/* Header */}
        <div className="flex items-start justify-between">
          <div className="flex-1 min-w-0">
            <h3 className="text-lg font-semibold text-foreground truncate">
              {snippet.title}
            </h3>
            {/* Always render description area to maintain uniform spacing */}
            <div className="mt-1 h-[2.5rem] flex items-start">
              {snippet.description ? (
                <p className="text-sm text-muted-foreground line-clamp-2 leading-5">
                  {snippet.description}
                </p>
              ) : (
                // Empty placeholder to maintain uniform spacing (exactly 2 lines)
                <p className="text-sm text-transparent select-none line-clamp-2 leading-5">
                  Placeholder description text that spans exactly two lines to maintain consistent spacing and layout
                </p>
              )}
            </div>
          </div>
          
          {type === 'personal' && (
            <div className="flex items-center space-x-2 ml-2">
              <button
                onClick={() => setShowEditModal(true)}
                className="p-1 text-muted-foreground hover:text-foreground transition-colors"
                title="Edit snippet"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
              </button>
              <button
                onClick={handleDelete}
                disabled={isDeleting}
                className="p-1 text-muted-foreground hover:text-red-600 transition-colors disabled:opacity-50"
                title="Delete snippet"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </button>
            </div>
          )}
        </div>

        {/* Language and Difficulty */}
        <div className="flex items-center space-x-2">
          <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium text-white ${
            LANGUAGE_COLORS[snippet.language] || 'bg-gray-500'
          }`}>
            {snippet.language}
          </span>
          <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
            DIFFICULTY_COLORS[snippet.difficulty] || 'bg-gray-100 text-gray-800'
          }`}>
            {snippet.difficulty}
          </span>
          {isOfficial && officialSnippet?.category && (
            <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
              {officialSnippet.category}
            </span>
          )}
        </div>

        {/* Tags - Use min-height for consistent spacing */}
        <div className="flex flex-wrap gap-1 min-h-[32px] items-start">
          {snippet.tags && snippet.tags.length > 0 && (
            <>
              {snippet.tags.slice(0, 3).map((tag, index) => (
                <span
                  key={index}
                  className="inline-flex items-center px-2 py-1 rounded-md text-xs bg-foreground/10 text-foreground"
                >
                  #{tag}
                </span>
              ))}
              {snippet.tags.length > 3 && (
                <span className="inline-flex items-center px-2 py-1 rounded-md text-xs bg-foreground/10 text-muted-foreground">
                  +{snippet.tags.length - 3} more
                </span>
              )}
            </>
          )}
        </div>

        {/* Code Preview - flex-1 to take remaining space */}
        <div className="bg-muted/50 rounded-lg p-3 flex-1">
          <div
            className="text-xs text-foreground font-mono overflow-hidden line-clamp-4 whitespace-pre"
            style={{ display: '-webkit-box', WebkitBoxOrient: 'vertical', WebkitLineClamp: 4 }}
          >
            {snippet.code}
          </div>
        </div>
      </div>

      {/* Footer - pinned to bottom */}
      <div className="flex items-center justify-between pt-4 mt-4 border-t border-border">
        <div className="text-xs text-muted-foreground">
          {isOfficial && officialSnippet?.estimatedTime ? (
            <span>~{officialSnippet.estimatedTime} min</span>
          ) : (
            <span>
              Created {new Date(snippet.createdAt).toLocaleDateString()}
            </span>
          )}
        </div>
        
        <button
          onClick={() => setShowViewModal(true)}
          className="px-3 py-1 text-xs bg-foreground/10 hover:bg-foreground/20 text-foreground rounded-md transition-colors"
        >
          View Code
        </button>
      </div>

      {/* Modals */}
      {showEditModal && type === 'personal' && personalSnippet && (
        <EditSnippetModal
          snippet={personalSnippet}
          accessToken={accessToken}
          refreshToken={refreshToken}
          onUpdated={(updated) => {
            onUpdated?.(updated)
            setShowEditModal(false)
          }}
          onClose={() => setShowEditModal(false)}
        />
      )}

      {showViewModal && (
        <ViewSnippetModal
          snippet={snippet}
          type={type}
          onClose={() => setShowViewModal(false)}
        />
      )}

      {showDeleteConfirm && (
        <ConfirmModal
          title="Delete Snippet"
          description="Are you sure you want to delete this snippet? This action cannot be undone."
          confirmText="Delete"
          cancelText="Cancel"
          onConfirm={confirmDelete}
          onCancel={cancelDelete}
          loading={isDeleting}
          isDestructive={true}
        />
      )}
    </div>
  )
}