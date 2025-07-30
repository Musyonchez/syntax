"use client"

import Link from "next/link"
import Image from "next/image"
import { useSession } from "next-auth/react"
import { ThemeToggle } from "./theme-toggle"
import { UserDropdown } from "./user-dropdown"
import { MobileMenu } from "./mobile-menu"

export function Navbar() {
  const { data: session } = useSession()
  
  return (
    <nav className="border-b border-border bg-background/80 backdrop-blur-sm sticky top-0 z-50">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center space-x-2">
            <Image
              src="/logo.png"
              alt="SyntaxMem"
              width={32}
              height={32}
              className="rounded"
            />
            <span className="font-bold text-xl text-foreground">
              SyntaxMem
            </span>
          </Link>
          
          {/* Navigation Links */}
          <div className="flex items-center space-x-6">
            {/* Main Navigation */}
            <div className="hidden md:flex items-center space-x-6">
              <Link 
                href="/snippets" 
                className="text-muted-foreground hover:text-foreground transition-colors"
              >
                Snippets
              </Link>
              <Link 
                href="/practice" 
                className="text-muted-foreground hover:text-foreground transition-colors"
              >
                Practice
              </Link>
              <Link 
                href="/leaderboard" 
                className="text-muted-foreground hover:text-foreground transition-colors"
              >
                Leaderboard
              </Link>
              <Link 
                href="/forum" 
                className="text-muted-foreground hover:text-foreground transition-colors"
              >
                Forum
              </Link>
            </div>
            
            {/* Theme Toggle */}
            <ThemeToggle />
            
            {/* Mobile Menu */}
            <MobileMenu />
            
            {/* User Section */}
            {session?.user ? (
              <UserDropdown />
            ) : (
              <Link 
                href="/login" 
                className="bg-foreground text-background px-4 py-2 rounded-lg font-medium hover:bg-foreground/90 transition-colors"
              >
                Sign In
              </Link>
            )}
          </div>
        </div>
      </div>
    </nav>
  )
}