"use client"

import { QueryClient, QueryClientProvider } from "@tanstack/react-query"
import { ReactQueryDevtools } from "@tanstack/react-query-devtools"
import { useState } from "react"

export function QueryProvider({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            staleTime: 60 * 1000, // 1 minute
            retry: (failureCount, error: Error) => {
              // Don't retry on 4xx errors
              const statusError = error as Error & { status?: number }
              if (statusError?.status && statusError.status >= 400 && statusError.status < 500) {
                return false
              }
              return failureCount < 3
            },
          },
          mutations: {
            retry: (failureCount, error: Error) => {
              // Don't retry on 4xx errors
              const statusError = error as Error & { status?: number }
              if (statusError?.status && statusError.status >= 400 && statusError.status < 500) {
                return false
              }
              return failureCount < 1
            },
          },
        },
      })
  )

  return (
    <QueryClientProvider client={queryClient}>
      {children}
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  )
}