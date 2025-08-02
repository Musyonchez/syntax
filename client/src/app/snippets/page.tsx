import { auth } from "@/lib/auth"
import { redirect } from "next/navigation"
import { SnippetsManager } from "@/components/snippets/snippets-manager"

export default async function Snippets() {
  const session = await auth()
  
  if (!session?.user) {
    redirect("/login")
  }

  return (
    <div className="min-h-[calc(100vh-8rem)] p-4 md:p-8">
      <div className="max-w-7xl mx-auto space-y-8">
        <SnippetsManager 
          accessToken={session.user.backendToken}
          refreshToken={session.user.refreshToken}
          userRole={session.user.role}
        />
      </div>
    </div>
  )
}