import { auth } from "@/lib/auth"
import { redirect } from "next/navigation"

export default async function AdminDashboard() {
  const session = await auth()
  
  if (!session?.user) {
    redirect("/login")
  }

  // Check if user is admin
  if (session.user.role !== 'admin') {
    redirect("/dashboard")
  }

  return (
    <div className="flex items-center justify-center min-h-[calc(100vh-8rem)] p-8">
      <div className="text-center space-y-8 max-w-2xl">
        <div className="space-y-4">
          <h1 className="text-3xl font-bold text-foreground">
            Admin Dashboard
          </h1>
          <p className="text-muted-foreground">
            Administrative controls and system management
          </p>
        </div>
        
        <div className="bg-muted/50 rounded-lg p-6 space-y-4">
          <h2 className="text-xl font-semibold">Admin Controls</h2>
          <div className="space-y-2 text-sm">
            <p><strong>User:</strong> {session.user.name}</p>
            <p><strong>Role:</strong> {session.user.role}</p>
            <p><strong>Admin Access:</strong> ✅ Granted</p>
          </div>
          
          <div className="pt-4 border-t border-border">
            <h3 className="text-lg font-medium mb-2">Coming Soon</h3>
            <p className="text-muted-foreground">
              Admin functionality is currently under development. 
              Soon you&apos;ll be able to manage users, content, and system settings.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}