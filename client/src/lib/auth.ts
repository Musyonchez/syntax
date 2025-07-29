import NextAuth from "next-auth"
import Google from "next-auth/providers/google"

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
    async signIn({ user, account, profile }) {
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
          console.error('Backend auth failed:', response.status)
          return false // Deny NextAuth session creation
        }
        
        const backendData = await response.json()
        console.log("DEBUG: Backend response:", backendData)
        
        // Check if response has success structure
        const userData = backendData.success ? backendData.data : backendData
        console.log("DEBUG: User data:", userData)
        
        // Replace user data with backend response
        user.id = userData.user.id
        user.name = userData.user.name
        user.email = userData.user.email
        user.image = userData.user.avatar
        user.backendToken = userData.token
        user.role = userData.user.role
        
        return true // Allow NextAuth to create session with backend data
        
      } catch (error) {
        console.error('Auth verification failed:', error)
        return false // Deny session creation if backend fails
      }
    },
    async jwt({ token, user }) {
      // Store backend data in JWT
      if (user) {
        token.backendToken = user.backendToken
        token.role = user.role
        token.sub = user.id
      }
      return token
    },
    async session({ session, token }) {
      // Populate session with backend data
      if (token && session.user) {
        session.user.id = token.sub as string
        session.user.backendToken = token.backendToken as string
        session.user.role = token.role as string
      }
      return session
    },
  },
})