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
      // Custom sign-in logic - temporarily bypassing backend for testing
      if (account?.provider === "google" && profile) {
        // TODO: Fix auth service and re-enable backend integration
        // For now, just allow sign-in with Google data
        user.role = "user"
        user.accessToken = "temp-token" // Temporary token
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