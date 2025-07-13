"use client"

import { SessionProvider } from "next-auth/react"
import { useEffect } from "react"
import { useSession } from "next-auth/react"
import { useAuthStore } from "@/stores/auth-store"
import type { User } from "@/types/auth"

function AuthSync() {
  const { data: session, status } = useSession()
  const { setUser, logout, setLoading } = useAuthStore()

  useEffect(() => {
    setLoading(status === "loading")

    if (status === "authenticated" && session?.user) {
      const user: User = {
        user_id: session.user.id,
        email: session.user.email!,
        name: session.user.name!,
        avatar: session.user.image!,
        role: session.user.role as "user" | "admin",
        preferences: {
          theme: "dark",
          languages: ["python"],
          difficulty: 5,
        },
        stats: {
          totalScore: 0,
          practiceTime: 0,
          streak: 0,
          level: 1,
          achievements: [],
        },
        created_at: new Date().toISOString(),
      }
      setUser(user)
    } else if (status === "unauthenticated") {
      logout()
    }
  }, [session, status, setUser, logout, setLoading])

  return null
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
  return (
    <SessionProvider>
      <AuthSync />
      {children}
    </SessionProvider>
  )
}