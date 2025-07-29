import { auth } from "@/lib/auth"
import { redirect } from "next/navigation"
import { LogoutAllButton } from "@/components/logout-all-button"

export default async function Dashboard() {
  const session = await auth()
  
  if (!session?.user) {
    redirect("/login")
  }

  return (
    <div className="flex items-center justify-center min-h-[calc(100vh-8rem)] p-8">
      <div className="text-center space-y-8 max-w-2xl">
        <div className="space-y-4">
          <h1 className="text-3xl font-bold text-foreground">
            Welcome back, {session.user.name}!
          </h1>
          <p className="text-muted-foreground">
            Ready to master coding through simplicity?
          </p>
        </div>
        
        <div className="bg-muted/50 rounded-lg p-6 space-y-4">
          <h2 className="text-xl font-semibold">Your Profile</h2>
          <div className="space-y-2 text-sm">
            <p><strong>Name:</strong> {session.user.name}</p>
            <p><strong>Email:</strong> {session.user.email}</p>
            <p><strong>Role:</strong> {session.user.role}</p>
            <p><strong>User ID:</strong> {session.user.id}</p>
          </div>
          
          <div className="pt-4 border-t border-border">
            <h3 className="text-sm font-medium mb-2 text-muted-foreground">Security</h3>
            <LogoutAllButton accessToken={session.user.backendToken} />
          </div>
        </div>
        
        <div className="space-y-4">
          <h2 className="text-lg font-medium text-muted-foreground">
            Coming Soon
          </h2>
          <div className="grid gap-4 sm:grid-cols-2">
            <div className="border rounded-lg p-4">
              <h3 className="font-medium">Practice Sessions</h3>
              <p className="text-sm text-muted-foreground">Interactive masked code completion</p>
            </div>
            <div className="border rounded-lg p-4">
              <h3 className="font-medium">Code Snippets</h3>
              <p className="text-sm text-muted-foreground">Browse and manage snippets</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}