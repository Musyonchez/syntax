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
      console.log("JWT callback triggered", { hasAccount: !!account, provider: account?.provider, backendSynced: token.backendSynced })
      
      // Integrate with backend on first sign in - pass ALL Google data to server
      if (account?.provider === "google" && !token.backendSynced) {
        console.log("Starting backend sync - passing all Google data to server")
        try {
          const response = await Promise.race([
            fetch(`${process.env.NEXT_PUBLIC_AUTH_API_URL || 'http://127.0.0.1:8080'}/google-auth`, {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify({
                // Pass ALL account data to server
                account: {
                  provider: account.provider,
                  providerAccountId: account.providerAccountId,
                  type: account.type,
                  id_token: account.id_token,
                  access_token: account.access_token,
                  expires_at: account.expires_at,
                  refresh_token: account.refresh_token,
                  scope: account.scope,
                  token_type: account.token_type,
                },
                // Pass ALL profile data to server
                profile: {
                  sub: profile?.sub,
                  name: profile?.name,
                  given_name: profile?.given_name,
                  family_name: profile?.family_name,
                  picture: profile?.picture,
                  email: profile?.email,
                  email_verified: profile?.email_verified,
                  locale: profile?.locale,
                },
                // Pass user data if available
                user: user ? {
                  id: user.id,
                  name: user.name,
                  email: user.email,
                  image: user.image,
                } : null
              }),
            }),
            new Promise((_, reject) => 
              setTimeout(() => reject(new Error('Backend sync timeout after 10 seconds')), 10000)
            )
          ])

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
          // Use fallback data only if server sync fails
          token.sub = profile?.sub || user?.id
          token.role = "user"
          token.name = profile?.name || user?.name
          token.email = profile?.email || user?.email
          token.picture = profile?.picture || user?.image
          token.backendSynced = false
          console.log("Using fallback client data due to backend sync failure")
        }
      }
      
      console.log("JWT callback completed")
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