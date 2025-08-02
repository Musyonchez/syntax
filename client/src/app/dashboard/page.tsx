import { auth } from "@/lib/auth"
import { redirect } from "next/navigation"
import { LogoutAllButton } from "@/components/logout-all-button"
import { DashboardStats } from "@/components/dashboard-stats"
import { RecentSnippets } from "@/components/recent-snippets"
import Image from "next/image"
import Link from "next/link"

export default async function Dashboard() {
  const session = await auth()
  
  if (!session?.user) {
    redirect("/login")
  }


  return (
    <div className="min-h-[calc(100vh-8rem)] p-4 md:p-8">
      <div className="max-w-7xl mx-auto space-y-8">
        {/* Header Section */}
        <div className="flex flex-col md:flex-row md:items-center md:justify-between space-y-4 md:space-y-0">
          <div className="space-y-2">
            <h1 className="text-3xl md:text-4xl font-bold text-foreground">
              Welcome back, {session.user.name?.split(' ')[0]}! 👋
            </h1>
            <p className="text-muted-foreground text-lg">
              Ready to master coding through simplicity?
            </p>
          </div>
          
          {/* Quick Actions */}
          <div className="flex items-center space-x-3">
            <Link 
              href="/practice"
              className="bg-foreground text-background px-4 py-2 rounded-lg font-medium hover:bg-foreground/90 transition-colors"
            >
              Start Practice
            </Link>
            <Link 
              href="/snippets"
              className="border border-border px-4 py-2 rounded-lg font-medium hover:bg-foreground/5 transition-colors"
            >
              Browse Snippets
            </Link>
          </div>
        </div>

        {/* Main Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column - Profile & Stats */}
          <div className="lg:col-span-1 space-y-6">
            {/* Profile Card */}
            <div className="bg-gradient-to-br from-background to-foreground/5 border border-border rounded-xl p-6 space-y-6">
              <div className="flex items-center space-x-4">
                <div className="relative">
                  <Image
                    src={session.user.image || '/logo.png'}
                    alt={session.user.name || 'User'}
                    width={64}
                    height={64}
                    className="rounded-full border-2 border-border"
                  />
                  <div className="absolute -bottom-1 -right-1 w-5 h-5 bg-green-500 border-2 border-background rounded-full"></div>
                </div>
                <div className="flex-1 min-w-0">
                  <h3 className="text-lg font-semibold text-foreground truncate">
                    {session.user.name}
                  </h3>
                  <p className="text-sm text-muted-foreground truncate">
                    {session.user.email}
                  </p>
                  <div className="flex items-center space-x-2 mt-1">
                    <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-foreground/10 text-foreground">
                      {session.user.role === 'admin' ? '👑 Admin' : '🚀 Developer'}
                    </span>
                  </div>
                </div>
              </div>

              {/* Edit Profile Button */}
              <button className="w-full bg-foreground/10 hover:bg-foreground/20 text-foreground px-4 py-2 rounded-lg font-medium transition-colors">
                ✏️ Edit Profile
              </button>
            </div>

            {/* Stats Card */}
            <DashboardStats 
              accessToken={session.user.backendToken} 
              refreshToken={session.user.refreshToken}
            />

            {/* Security Card */}
            <div className="bg-background border border-border rounded-xl p-6 space-y-4">
              <h3 className="font-semibold text-foreground">Security</h3>
              <div className="space-y-3">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-muted-foreground">Last login</span>
                  <span className="text-foreground">Today</span>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-muted-foreground">Active sessions</span>
                  <span className="text-foreground">2 devices</span>
                </div>
                <div className="pt-2 border-t border-border">
                  <LogoutAllButton accessToken={session.user.backendToken} />
                </div>
              </div>
            </div>
          </div>

          {/* Right Column - Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Quick Actions Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Link 
                href="/practice"
                className="group bg-gradient-to-br from-foreground/5 to-foreground/10 border border-border rounded-xl p-6 hover:shadow-md hover:bg-foreground/10 transition-all duration-200"
              >
                <div className="flex items-center space-x-4">
                  <div className="w-12 h-12 bg-blue-500 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform duration-200">
                    <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                  </div>
                  <div>
                    <h3 className="font-semibold text-foreground">Practice Sessions</h3>
                    <p className="text-sm text-muted-foreground">Interactive masked code completion</p>
                  </div>
                </div>
              </Link>

              <Link 
                href="/snippets"
                className="group bg-gradient-to-br from-foreground/5 to-foreground/10 border border-border rounded-xl p-6 hover:shadow-md hover:bg-foreground/10 transition-all duration-200"
              >
                <div className="flex items-center space-x-4">
                  <div className="w-12 h-12 bg-purple-500 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform duration-200">
                    <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </div>
                  <div>
                    <h3 className="font-semibold text-foreground">Code Snippets</h3>
                    <p className="text-sm text-muted-foreground">Browse and manage your snippets</p>
                  </div>
                </div>
              </Link>

              <Link 
                href="/leaderboard"
                className="group bg-gradient-to-br from-foreground/5 to-foreground/10 border border-border rounded-xl p-6 hover:shadow-md hover:bg-foreground/10 transition-all duration-200"
              >
                <div className="flex items-center space-x-4">
                  <div className="w-12 h-12 bg-green-500 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform duration-200">
                    <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v4a2 2 0 01-2 2h-2a2 2 0 00-2 2z" />
                    </svg>
                  </div>
                  <div>
                    <h3 className="font-semibold text-foreground">Leaderboard</h3>
                    <p className="text-sm text-muted-foreground">See how you rank against others</p>
                  </div>
                </div>
              </Link>

              <Link 
                href="/forum"
                className="group bg-gradient-to-br from-foreground/5 to-foreground/10 border border-border rounded-xl p-6 hover:shadow-md hover:bg-foreground/10 transition-all duration-200"
              >
                <div className="flex items-center space-x-4">
                  <div className="w-12 h-12 bg-orange-500 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform duration-200">
                    <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8h2a2 2 0 012 2v6a2 2 0 01-2 2h-2v4l-4-4H9a1.994 1.994 0 01-1.414-.586m0 0L11 14h4a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2v4l.586-.586z" />
                    </svg>
                  </div>
                  <div>
                    <h3 className="font-semibold text-foreground">Community Forum</h3>
                    <p className="text-sm text-muted-foreground">Connect with other developers</p>
                  </div>
                </div>
              </Link>
            </div>

            {/* Recent Snippets */}
            <RecentSnippets 
              accessToken={session.user.backendToken}
              refreshToken={session.user.refreshToken}
            />
            
          </div>
        </div>
      </div>
    </div>
  )
}