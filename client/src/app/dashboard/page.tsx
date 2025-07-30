import { auth } from "@/lib/auth"
import { redirect } from "next/navigation"
import { LogoutAllButton } from "@/components/logout-all-button"
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
                    <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                      session.user.role === 'admin' 
                        ? 'bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-300' 
                        : 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300'
                    }`}>
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
            <div className="bg-background border border-border rounded-xl p-6 space-y-4">
              <h3 className="font-semibold text-foreground">Your Progress</h3>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <div className="w-8 h-8 bg-green-500/20 rounded-lg flex items-center justify-center">
                      🎯
                    </div>
                    <span className="text-sm font-medium">Practice Sessions</span>
                  </div>
                  <span className="text-lg font-bold text-foreground">12</span>
                </div>
                
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <div className="w-8 h-8 bg-blue-500/20 rounded-lg flex items-center justify-center">
                      📝
                    </div>
                    <span className="text-sm font-medium">Snippets Created</span>
                  </div>
                  <span className="text-lg font-bold text-foreground">8</span>
                </div>
                
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <div className="w-8 h-8 bg-purple-500/20 rounded-lg flex items-center justify-center">
                      🏆
                    </div>
                    <span className="text-sm font-medium">Ranking</span>
                  </div>
                  <span className="text-lg font-bold text-foreground">#24</span>
                </div>
              </div>
            </div>

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
                className="group bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-950/20 dark:to-blue-900/20 border border-blue-200/50 dark:border-blue-800/50 rounded-xl p-6 hover:shadow-md transition-all duration-200"
              >
                <div className="flex items-center space-x-4">
                  <div className="w-12 h-12 bg-blue-500 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform duration-200">
                    <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                  </div>
                  <div>
                    <h3 className="font-semibold text-blue-900 dark:text-blue-100">Practice Sessions</h3>
                    <p className="text-sm text-blue-700 dark:text-blue-300">Interactive masked code completion</p>
                  </div>
                </div>
              </Link>

              <Link 
                href="/snippets"
                className="group bg-gradient-to-br from-purple-50 to-purple-100 dark:from-purple-950/20 dark:to-purple-900/20 border border-purple-200/50 dark:border-purple-800/50 rounded-xl p-6 hover:shadow-md transition-all duration-200"
              >
                <div className="flex items-center space-x-4">
                  <div className="w-12 h-12 bg-purple-500 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform duration-200">
                    <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </div>
                  <div>
                    <h3 className="font-semibold text-purple-900 dark:text-purple-100">Code Snippets</h3>
                    <p className="text-sm text-purple-700 dark:text-purple-300">Browse and manage your snippets</p>
                  </div>
                </div>
              </Link>

              <Link 
                href="/leaderboard"
                className="group bg-gradient-to-br from-green-50 to-green-100 dark:from-green-950/20 dark:to-green-900/20 border border-green-200/50 dark:border-green-800/50 rounded-xl p-6 hover:shadow-md transition-all duration-200"
              >
                <div className="flex items-center space-x-4">
                  <div className="w-12 h-12 bg-green-500 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform duration-200">
                    <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v4a2 2 0 01-2 2h-2a2 2 0 00-2 2z" />
                    </svg>
                  </div>
                  <div>
                    <h3 className="font-semibold text-green-900 dark:text-green-100">Leaderboard</h3>
                    <p className="text-sm text-green-700 dark:text-green-300">See how you rank against others</p>
                  </div>
                </div>
              </Link>

              <Link 
                href="/forum"
                className="group bg-gradient-to-br from-orange-50 to-orange-100 dark:from-orange-950/20 dark:to-orange-900/20 border border-orange-200/50 dark:border-orange-800/50 rounded-xl p-6 hover:shadow-md transition-all duration-200"
              >
                <div className="flex items-center space-x-4">
                  <div className="w-12 h-12 bg-orange-500 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform duration-200">
                    <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8h2a2 2 0 012 2v6a2 2 0 01-2 2h-2v4l-4-4H9a1.994 1.994 0 01-1.414-.586m0 0L11 14h4a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2v4l.586-.586z" />
                    </svg>
                  </div>
                  <div>
                    <h3 className="font-semibold text-orange-900 dark:text-orange-100">Community Forum</h3>
                    <p className="text-sm text-orange-700 dark:text-orange-300">Connect with other developers</p>
                  </div>
                </div>
              </Link>
            </div>

            {/* Recent Activity */}
            <div className="bg-background border border-border rounded-xl p-6 space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="font-semibold text-foreground">Recent Activity</h3>
                <button className="text-sm text-muted-foreground hover:text-foreground transition-colors">
                  View all
                </button>
              </div>
              
              <div className="space-y-3">
                <div className="flex items-center space-x-3 p-3 bg-foreground/5 rounded-lg">
                  <div className="w-8 h-8 bg-blue-500/20 rounded-lg flex items-center justify-center">
                    🎯
                  </div>
                  <div className="flex-1">
                    <p className="text-sm font-medium">Completed JavaScript Basics practice session</p>
                    <p className="text-xs text-muted-foreground">2 hours ago</p>
                  </div>
                  <span className="text-xs bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300 px-2 py-1 rounded-full">
                    +15 XP
                  </span>
                </div>
                
                <div className="flex items-center space-x-3 p-3 bg-foreground/5 rounded-lg">
                  <div className="w-8 h-8 bg-purple-500/20 rounded-lg flex items-center justify-center">
                    📝
                  </div>
                  <div className="flex-1">
                    <p className="text-sm font-medium">Created new React Hook snippet</p>
                    <p className="text-xs text-muted-foreground">1 day ago</p>
                  </div>
                  <span className="text-xs bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300 px-2 py-1 rounded-full">
                    +5 XP
                  </span>
                </div>
                
                <div className="flex items-center space-x-3 p-3 bg-foreground/5 rounded-lg">
                  <div className="w-8 h-8 bg-green-500/20 rounded-lg flex items-center justify-center">
                    🏆
                  </div>
                  <div className="flex-1">
                    <p className="text-sm font-medium">Reached top 30 on leaderboard</p>
                    <p className="text-xs text-muted-foreground">3 days ago</p>
                  </div>
                  <span className="text-xs bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300 px-2 py-1 rounded-full">
                    Achievement
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}