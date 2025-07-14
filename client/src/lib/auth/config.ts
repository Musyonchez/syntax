import NextAuth, { type DefaultSession } from "next-auth"
import GoogleProvider from "next-auth/providers/google"

// Extend the default session type
declare module "next-auth" {
  interface Session {
    user: {
      id: string
      role: string
    } & DefaultSession["user"]
  }

  interface User {
    role: string
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
    async session({ session, token, user }) {
      // Send properties to the client
      if (session.user) {
        session.user.id = user?.id || token?.sub || ""
        session.user.role = (user as { role?: string })?.role || "user"
      }
      return session
    },
    async jwt({ token, user }) {
      if (user) {
        token.role = (user as { role?: string })?.role || "user"
      }
      return token
    },
    async signIn({ user, account, profile }) {
      // Custom sign-in logic - integrate with our backend
      if (account?.provider === "google" && profile) {
        try {
          // Call our backend auth service to sync user data
          const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/google-auth`, {
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
            // Store additional user data
            user.role = data.user?.role || "user"
            return true
          } else {
            // Backend auth failed
            return false
          }
        } catch (error) {
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