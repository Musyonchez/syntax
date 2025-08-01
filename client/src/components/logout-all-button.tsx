'use client'

import { useState } from 'react'
import { signOut } from 'next-auth/react'
import { logoutAllDevices } from '@/lib/auth-actions'

interface LogoutAllButtonProps {
  accessToken: string
}

export function LogoutAllButton({ accessToken }: LogoutAllButtonProps) {
  const [isLoading, setIsLoading] = useState(false)

  const handleLogoutAll = async () => {
    if (!confirm('This will sign you out of ALL devices. Continue?')) {
      return
    }

    setIsLoading(true)
    
    try {
      // Call backend to revoke all refresh tokens
      const result = await logoutAllDevices(accessToken)
      
      console.log(`Revoked ${result.data.revokedTokens} sessions`)
      
      // Sign out of current session
      await signOut({ 
        callbackUrl: '/login',
        redirect: true 
      })
      
    } catch (error) {
      console.error('Failed to logout all devices:', error)
      alert('Failed to logout all devices. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <button
      onClick={handleLogoutAll}
      disabled={isLoading}
      className="px-4 py-2 text-sm bg-red-500 hover:bg-red-600 disabled:bg-red-300 text-white rounded-lg transition-colors"
    >
      {isLoading ? 'Signing out...' : 'Sign out all devices'}
    </button>
  )
}