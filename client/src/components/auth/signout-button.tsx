"use client"

import { useState } from "react"
import { signOut, useSession } from "next-auth/react"
import { logout } from "@/lib/auth-actions"

export function SignOutButton() {
  const { data: session } = useSession()
  const [isLoading, setIsLoading] = useState(false)

  const handleSignOut = async () => {
    setIsLoading(true)
    
    try {
      // First, revoke refresh token from backend if we have one
      if (session?.user?.refreshToken) {
        await logout(session.user.refreshToken)
        console.log('Refresh token revoked from backend')
      }
      
      // Then sign out from NextAuth
      await signOut({ 
        callbackUrl: '/',
        redirect: true 
      })
      
    } catch (error) {
      console.error('Error during logout:', error)
      // Still sign out from NextAuth even if backend fails
      await signOut({ 
        callbackUrl: '/',
        redirect: true 
      })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <button
      onClick={handleSignOut}
      disabled={isLoading}
      className="text-sm text-muted-foreground hover:text-foreground disabled:opacity-50 transition-colors"
    >
      {isLoading ? 'Signing out...' : 'Sign Out'}
    </button>
  )
}