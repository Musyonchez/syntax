"use client"

import { useState, useRef, useEffect } from 'react'
import { useSession, signOut } from 'next-auth/react'
import Link from 'next/link'
import Image from 'next/image'

export function UserDropdown() {
  const { data: session } = useSession()
  const [isOpen, setIsOpen] = useState(false)
  const dropdownRef = useRef<HTMLDivElement>(null)

  // Close dropdown when clicking outside
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  if (!session?.user) {
    return null
  }

  const isAdmin = session.user.role === 'admin'

  return (
    <div className="relative" ref={dropdownRef}>
      {/* Profile Image Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center space-x-2 p-1 rounded-full hover:bg-foreground/10 transition-colors"
        aria-label="User menu"
      >
        <Image
          src={session.user.image || '/logo.png'}
          alt={session.user.name || 'User'}
          width={32}
          height={32}
          className="rounded-full border-2 border-border"
        />
        {/* Dropdown arrow */}
        <svg
          className={`w-4 h-4 text-muted-foreground transition-transform ${
            isOpen ? 'rotate-180' : ''
          }`}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M19 9l-7 7-7-7"
          />
        </svg>
      </button>

      {/* Dropdown Menu */}
      {isOpen && (
        <div className="absolute right-0 mt-2 w-48 bg-background border border-border rounded-lg shadow-lg z-50">
          <div className="py-2">
            {/* User Info */}
            <div className="px-4 py-2 border-b border-border">
              <p className="text-sm font-medium text-foreground">
                {session.user.name}
              </p>
              <p className="text-xs text-muted-foreground truncate">
                {session.user.email}
              </p>
            </div>

            {/* Menu Items */}
            <div className="py-1">
              <Link
                href="/dashboard"
                className="block px-4 py-2 text-sm text-foreground hover:bg-foreground/10 transition-colors"
                onClick={() => setIsOpen(false)}
              >
                Dashboard
              </Link>
              
              {isAdmin && (
                <Link
                  href="/admin"
                  className="block px-4 py-2 text-sm text-foreground hover:bg-foreground/10 transition-colors"
                  onClick={() => setIsOpen(false)}
                >
                  Admin Dashboard
                </Link>
              )}
              
              <button
                onClick={() => {
                  setIsOpen(false)
                  signOut()
                }}
                className="block w-full text-left px-4 py-2 text-sm text-foreground hover:bg-foreground/10 transition-colors"
              >
                Sign Out
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}