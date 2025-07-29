import NextAuth, { type DefaultSession } from "next-auth"
import GoogleProvider from "next-auth/providers/google"

// Extend the default session type
declare module "next-auth" {
  interface Session {
    user: {
      id: string
      role: string
    } & DefaultSession["user"]
    accessToken?: string
  }

  interface User {
    role: string
    accessToken?: string
  }
  
  interface JWT {
    accessToken?: string
    refreshToken?: string
    role?: string
  }
}

const authConfig = NextAuth({
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    }),
  ],
  callbacks: {
    async jwt({ token, account, profile }) {
      // Sync with backend on first sign in
      if (account?.provider === "google" && profile) {
        try {
          const response = await fetch(`${process.env.NEXT_PUBLIC_AUTH_API_URL || 'http://localhost:8081'}/google-auth`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              account: { id_token: account.id_token },
              profile: {
                sub: profile.sub,
                name: profile.name,
                picture: profile.picture,
                email: profile.email,
              },
            }),
          })

          if (response.ok) {
            const data = await response.json()
            if (data.success && data.data) {
              token.sub = data.data.user?.user_id
              token.role = data.data.user?.role || "user"
              token.accessToken = data.data.access_token
              token.refreshToken = data.data.refresh_token
              
              // Update user data from server
              if (data.data.user) {
                token.name = data.data.user.name
                token.email = data.data.user.email
                token.picture = data.data.user.avatar
              }
            }
          }
        } catch (error) {
          console.error("Backend sync failed:", error)
          // Continue with client-only auth if backend fails
          token.role = "user"
        }
      }

      // Check if access token needs refresh
      if (token.accessToken && token.refreshToken) {
        try {
          const payload = JSON.parse(atob(token.accessToken.split('.')[1]))
          const currentTime = Date.now() / 1000
          
          // If token expires in less than 5 seconds, refresh it
          if (payload.exp && payload.exp - currentTime < 5) {
            const refreshResponse = await fetch(`${process.env.NEXT_PUBLIC_AUTH_API_URL || 'http://localhost:8081'}/refresh`, {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({
                refresh_token: token.refreshToken
              }),
            })

            if (refreshResponse.ok) {
              const refreshData = await refreshResponse.json()
              if (refreshData.success && refreshData.data) {
                token.accessToken = refreshData.data.access_token
                // Keep the same refresh token unless a new one is provided
                if (refreshData.data.refresh_token) {
                  token.refreshToken = refreshData.data.refresh_token
                }
              }
            }
          }
        } catch {
          // If refresh fails, continue with existing tokens
        }
      }
      
      return token
    },
    
    async session({ session, token }) {
      if (token) {
        session.user.id = token.sub as string
        session.user.role = token.role as string
        session.accessToken = token.accessToken as string
      }
      return session
    },
  },
  pages: {
    signIn: "/auth/signin",
    error: "/auth/error",
  },
  session: {
    strategy: "jwt",
  },
})

export const { handlers, auth, signIn, signOut } = authConfig
export const { GET, POST } = handlers