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