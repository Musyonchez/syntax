import NextAuth, { type DefaultSession } from "next-auth"
import GoogleProvider from "next-auth/providers/google"
import { MongoDBAdapter } from "@auth/mongodb-adapter"
import { MongoClient } from "mongodb"

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

// MongoDB client for NextAuth adapter
const client = process.env.MONGODB_URI ? new MongoClient(process.env.MONGODB_URI) : null

const authConfig = NextAuth({
  adapter: client ? MongoDBAdapter(client) : undefined,
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
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
              google_token: account.access_token,
              google_id: account.providerAccountId,
              email: profile.email,
              name: profile.name,
              avatar: profile.image,
            }),
          })

          if (response.ok) {
            const data = await response.json()
            // Store additional user data
            user.role = data.user?.role || "user"
            return true
          } else {
            console.error("Backend auth failed:", response.statusText)
            return false
          }
        } catch (error) {
          console.error("Sign-in error:", error)
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
    strategy: client ? "database" : "jwt",
  },
  debug: process.env.NODE_ENV === "development",
})

export const { handlers, auth, signIn, signOut } = authConfig
export const { GET, POST } = handlers