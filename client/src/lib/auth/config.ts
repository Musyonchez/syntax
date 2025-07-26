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
    backendSynced?: boolean
  }
}

const authConfig = NextAuth({
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
      authorization: {
        params: {
          scope: "openid email profile",
        },
      },
    }),
  ],
  callbacks: {
    async jwt({ token, user, account, profile }) {
      console.log("JWT callback triggered", { hasAccount: !!account, provider: account?.provider, backendSynced: token.backendSynced })
      
      // Integrate with backend on first sign in - pass ALL Google data to server
      if (account?.provider === "google" && !token.backendSynced) {
        console.log("Starting backend sync - passing all Google data to server")
        try {
          const response = await fetch(`${process.env.NEXT_PUBLIC_AUTH_API_URL || 'http://localhost:8081'}/google-auth`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              // Only send essential account data
              account: {
                id_token: account.id_token,
              },
              // Only send essential profile data
              profile: {
                sub: profile?.sub,
                name: profile?.name,
                picture: profile?.picture,
                email: profile?.email,
              },
            }),
          })

          if (response.ok) {
            const serverData = await response.json()
            console.log("Backend sync successful - using server response")
            
            // Use ONLY server response data - don't mix with client data
            if (serverData.success && serverData.data) {
              token.sub = serverData.data.user?.user_id
              token.role = serverData.data.user?.role
              token.accessToken = serverData.data.token
              token.backendSynced = true
              
              // Store user data from server response
              if (serverData.data.user) {
                token.name = serverData.data.user.name
                token.email = serverData.data.user.email
                token.picture = serverData.data.user.avatar
              }
              
              console.log("Token updated with server data")
            } else {
              throw new Error("Invalid server response format")
            }
          } else {
            throw new Error(`Server responded with status ${response.status}`)
          }
        } catch (error) {
          console.error("Backend sync failed:", error)
          // Don't fallback - authentication should fail if backend sync fails
          throw error
        }
      }
      
      console.log("JWT callback completed")
      return token
    },
    async session({ session: sessionData, token }) {
      // Pass JWT data to session
      if (token) {
        sessionData.user.id = token.sub as string
        sessionData.user.role = token.role as string
        sessionData.accessToken = token.accessToken as string
      }
      return sessionData
    },
    async signIn({ account, profile }) {
      // Allow Google sign-in - backend sync happens in jwt callback
      if (account?.provider === "google" && profile) {
        return true
      }
      return true
    },
  },
  pages: {
    signIn: "/auth/signin",
    error: "/auth/error",
  },
  session: {
    strategy: "jwt",
  },
  debug: false, // Disable debug logs to prevent token exposure
})

export const { handlers, auth, signIn, signOut } = authConfig
export const { GET, POST } = handlers