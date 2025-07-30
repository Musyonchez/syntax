import { auth } from "@/lib/auth"
import { redirect } from "next/navigation"

export default async function Practice() {
  const session = await auth()
  
  if (!session?.user) {
    redirect("/login")
  }

  return (
    <div className="flex items-center justify-center min-h-[calc(100vh-8rem)] p-8">
      <div className="text-center space-y-8 max-w-2xl">
        <div className="space-y-4">
          <h1 className="text-3xl font-bold text-foreground">
            Practice Sessions
          </h1>
          <p className="text-muted-foreground">
            Interactive masked code completion challenges
          </p>
        </div>
        
        <div className="bg-muted/50 rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Coming Soon</h2>
          <p className="text-muted-foreground">
            The practice system is currently under development. 
            Soon you&apos;ll be able to practice coding with interactive masked completion exercises.
          </p>
        </div>
      </div>
    </div>
  )
}