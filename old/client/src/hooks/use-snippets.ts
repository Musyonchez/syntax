import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { snippetsApi } from '@/lib/api/snippets'
import { toast } from 'sonner'

// Official snippets hooks
export function useOfficialSnippets(params?: {
  language?: string
  difficulty?: number
  page?: number
  per_page?: number
}) {
  return useQuery({
    queryKey: ['snippets', 'official', params],
    queryFn: () => snippetsApi.getOfficial(params),
    staleTime: 5 * 60 * 1000, // 5 minutes
  })
}

// Personal snippets hooks
export function usePersonalSnippets(params?: {
  page?: number
  per_page?: number
}) {
  return useQuery({
    queryKey: ['snippets', 'personal', params],
    queryFn: () => snippetsApi.getPersonal(params),
    staleTime: 2 * 60 * 1000, // 2 minutes
  })
}

// Individual snippet hooks
export function useSnippet(snippetId: string | null) {
  return useQuery({
    queryKey: ['snippet', snippetId],
    queryFn: () => snippetId ? snippetsApi.getById(snippetId) : null,
    enabled: !!snippetId,
    staleTime: 10 * 60 * 1000, // 10 minutes
  })
}

export function useMaskedSnippet(snippetId: string | null, difficulty?: number) {
  return useQuery({
    queryKey: ['snippet', 'masked', snippetId, difficulty],
    queryFn: () => snippetId ? snippetsApi.getMasked(snippetId, difficulty) : null,
    enabled: !!snippetId,
    staleTime: 30 * 60 * 1000, // 30 minutes (masked versions don't change often)
  })
}

// Snippet mutations
export function useCreateSnippet() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: snippetsApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['snippets', 'personal'] })
      toast.success('Personal snippet created successfully!')
    },
    onError: (error: unknown) => {
      const message = (error as { response?: { data?: { detail?: string } } })?.response?.data?.detail || 'Failed to create snippet'
      toast.error(message)
    }
  })
}

export function useSubmitSnippet() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: snippetsApi.submit,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['snippet-submissions'] })
      toast.success('Snippet submitted for review!')
    },
    onError: (error: unknown) => {
      const message = (error as { response?: { data?: { detail?: string } } })?.response?.data?.detail || 'Failed to submit snippet'
      toast.error(message)
    }
  })
}

// Snippet submissions
export function useSnippetSubmissions() {
  return useQuery({
    queryKey: ['snippet-submissions'],
    queryFn: snippetsApi.getSubmissions,
    staleTime: 2 * 60 * 1000, // 2 minutes
  })
}

// Utility hooks
export function useSnippetFilters() {
  const languages = ['python', 'javascript'] as const
  const difficulties = Array.from({ length: 10 }, (_, i) => i + 1)
  
  return {
    languages,
    difficulties
  }
}