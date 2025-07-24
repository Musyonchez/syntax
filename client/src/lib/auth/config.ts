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
    async session({ session, token }) {
      // Send properties to the client
      if (session.user) {
        session.user.id = token?.sub || ""
        session.user.role = token?.role as string || "user"
        session.accessToken = token?.accessToken as string
      }
      return session
    },
    async jwt({ token, user, account, profile }) {
      console.log("JWT callback triggered", { hasAccount: !!account, provider: account?.provider, backendSynced: token.backendSynced, isClient: typeof window !== "undefined" })
      
      // Integrate with backend on first sign in
      if (account?.provider === "google" && !token.backendSynced) {
        console.log("Starting backend sync for Google auth")
        try {
          
          console.log("Making backend request to:", `${process.env.NEXT_PUBLIC_AUTH_API_URL || 'http://127.0.0.1:8080'}/google-auth`)
          const response = await Promise.race([
            fetch(`${process.env.NEXT_PUBLIC_AUTH_API_URL || 'http://127.0.0.1:8080'}/google-auth`, {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify({
                google_token: account.id_token || account.access_token || "",
                google_id: account.providerAccountId || profile?.sub,
                email: profile?.email,
                name: profile?.name || "",
                avatar: profile?.picture || profile?.image || "",
              }),
            }),
            new Promise((_, reject) => 
              setTimeout(() => reject(new Error('Backend sync timeout after 10 seconds')), 10000)
            )
          ])
          console.log("Backend response status:", response.status)

          
          if (response.ok) {
            console.log("Backend sync successful")
            const data = await response.json()
            console.log("Backend response data:", data)
            
            // Store backend data in token
            token.role = data.data?.user?.role || "user"
            token.accessToken = data.data?.token
            token.backendSynced = true
            console.log("Token updated successfully")
          } else {
            console.error("Backend sync failed with status:", response.status)
            const errorText = await response.text()
            console.error("Error response:", errorText)
            token.role = "user"
            token.backendSynced = false
          }
        } catch (error) {
          console.error("Backend sync error:", error)
          // Continue with OAuth flow even if backend sync fails
          token.role = "user"
          token.backendSynced = false
          console.log("Continuing OAuth flow despite backend sync failure")
        }
      }
      
      // Store user data from previous sync
      if (user && account) {
        token.role = token.role || "user"
      }
      
      console.log("JWT callback completed, returning token")
      return token
    },
    async signIn({ user, account, profile }) {
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