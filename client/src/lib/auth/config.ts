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
    async jwt({ token, user, account }) {
      // Store the JWT token from our backend in the NextAuth token
      if (user && account) {
        token.role = (user as { role?: string })?.role || "user"
        token.accessToken = (user as { accessToken?: string })?.accessToken
      }
      return token
    },
    async signIn({ user, account, profile }) {
      // Custom sign-in logic - integrate with our backend
      if (account?.provider === "google" && profile) {
        try {
          // Call our backend auth service to sync user data
          const response = await fetch(`${process.env.NEXT_PUBLIC_AUTH_API_URL || 'http://localhost:8080'}/google-auth`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              google_token: account.id_token || account.access_token || "",
              google_id: account.providerAccountId || profile.sub,
              email: profile.email,
              name: profile.name || "",
              avatar: profile.picture || profile.image || "",
            }),
          })

          if (response.ok) {
            const data = await response.json()
            // Store the JWT token and user data in the user object
            user.role = data.user?.role || "user"
            user.accessToken = data.token // Store the JWT token
            return true
          } else {
            // Backend auth failed
            return false
          }
        } catch {
          // Sign-in error occurred
          return false
        }
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