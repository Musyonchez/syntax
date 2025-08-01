import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { practiceApi } from '@/lib/api/practice'
import { toast } from 'sonner'

// Practice session hooks
export function useStartPractice() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: practiceApi.startSession,
    onSuccess: (data) => {
      // Cache the session data
      queryClient.setQueryData(['practice-session', data.session_id], data)
      toast.success('Practice session started!')
    },
    onError: (error: unknown) => {
      const message = (error as { response?: { data?: { detail?: string } } })?.response?.data?.detail || 'Failed to start practice session'
      toast.error(message)
    }
  })
}

export function useSubmitPractice() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: practiceApi.submitSession,
    onSuccess: (data, variables) => {
      // Invalidate related queries
      queryClient.invalidateQueries({ queryKey: ['practice-history'] })
      queryClient.invalidateQueries({ queryKey: ['practice-stats'] })
      queryClient.invalidateQueries({ queryKey: ['practice-session', variables.session_id] })
      toast.success('Practice session completed!')
    },
    onError: (error: unknown) => {
      const message = (error as { response?: { data?: { detail?: string } } })?.response?.data?.detail || 'Failed to submit practice session'
      toast.error(message)
    }
  })
}

export function usePracticeSession(sessionId: string | null) {
  return useQuery({
    queryKey: ['practice-session', sessionId],
    queryFn: () => sessionId ? practiceApi.getSession(sessionId) : null,
    enabled: !!sessionId,
    staleTime: 5 * 60 * 1000, // 5 minutes
  })
}

// Practice history hooks
export function usePracticeHistory(params?: {
  page?: number
  per_page?: number
  language?: string
  completed_only?: boolean
}) {
  return useQuery({
    queryKey: ['practice-history', params],
    queryFn: () => practiceApi.getHistory(params),
    staleTime: 2 * 60 * 1000, // 2 minutes
  })
}

// Practice statistics hooks
export function usePracticeStats() {
  return useQuery({
    queryKey: ['practice-stats'],
    queryFn: practiceApi.getStats,
    staleTime: 5 * 60 * 1000, // 5 minutes
  })
}

// Custom hook for practice workflow
export function usePracticeWorkflow() {
  const startPractice = useStartPractice()
  const submitPractice = useSubmitPractice()
  
  const startSession = async (snippetId: string, difficulty?: number) => {
    try {
      const session = await startPractice.mutateAsync({
        snippet_id: snippetId,
        difficulty
      })
      return session
    } catch (error) {
      throw error
    }
  }
  
  const submitSession = async (sessionId: string, answers: string[], timeSpent: number) => {
    try {
      const result = await submitPractice.mutateAsync({
        session_id: sessionId,
        user_answers: answers,
        time_taken: timeSpent
      })
      return result
    } catch (error) {
      throw error
    }
  }
  
  return {
    startSession,
    submitSession,
    isStarting: startPractice.isPending,
    isSubmitting: submitPractice.isPending,
    startError: startPractice.error,
    submitError: submitPractice.error
  }
}