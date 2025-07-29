"use client"

import { signOut } from "next-auth/react"

export function SignOutButton() {
  return (
    <button
      onClick={() => signOut()}
      className="text-sm text-muted-foreground hover:text-foreground transition-colors"
    >
      Sign Out
    </button>
  )
}