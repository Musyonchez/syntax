import NextAuth from "next-auth"
import Google from "next-auth/providers/google"
import { storeBackendTokens } from "./server-auth"

export const { handlers, signIn, signOut, auth } = NextAuth({
  providers: [
    Google({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    }),
  ],
  pages: {
    signIn: "/login",
  },
  callbacks: {
    async signIn({ user, account }) {
      try {
        // Send all data to backend for validation and user creation
        const response = await fetch(`${process.env.NEXT_PUBLIC_AUTH_API_URL || 'http://localhost:8081'}/google-auth`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            email: user.email,
            name: user.name,
            avatar: user.image,
            googleAccessToken: account?.access_token,
            googleRefreshToken: account?.refresh_token,
          }),
        })
        
        if (!response.ok) {
          return false // Deny NextAuth session creation
        }
        
        const backendData = await response.json()
        
        // Check if response has success structure
        const userData = backendData.success ? backendData.data : backendData
        
        // Replace user data with backend response (NO SENSITIVE TOKENS)
        user.id = userData.user.id
        user.name = userData.user.name
        user.email = userData.user.email
        user.image = userData.user.avatar
        user.role = userData.user.role
        
        // Store tokens securely in HTTP-only cookies (server-side only)
        if (userData.token && userData.refreshToken) {
          await storeBackendTokens(userData.user.id, userData.token, userData.refreshToken)
        }
        
        return true // Allow NextAuth to create session with backend data
        
      } catch (error) {
        return false // Deny session creation if backend fails
      }
    },
    async jwt({ token, user }) {
      // Store only non-sensitive data in JWT
      if (user) {
        token.role = user.role
        token.sub = user.id
      }
      return token
    },
    async session({ session, token }) {
      // Populate session with non-sensitive data only
      if (token && session.user) {
        session.user.id = token.sub as string
        session.user.role = token.role as string
      }
      return session
    },
  },
})