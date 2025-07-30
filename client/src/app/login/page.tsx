import { signIn, auth } from "@/lib/auth"
import { redirect } from "next/navigation"
import Image from "next/image"

export default async function Login() {
  const session = await auth()
  
  if (session?.user) {
    redirect("/dashboard")
  }
  
  return (
    <div className="min-h-[calc(100vh-8rem)] flex">
      {/* Left Side - Branding */}
      <div className="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-foreground/5 to-foreground/10 p-8 items-center justify-center">
        <div className="max-w-md space-y-8 text-center">
          <div className="space-y-4">
            <Image
              src="/logo.png"
              alt="SyntaxMem"
              width={200}
              height={67}
              className="mx-auto dark:invert"
            />
            <h2 className="text-2xl font-bold text-foreground">
              Master Coding Through Simplicity
            </h2>
            <p className="text-muted-foreground">
              Interactive practice sessions, curated snippets, and community-driven learning.
            </p>
          </div>
          
          <div className="space-y-3 text-sm text-muted-foreground">
            <div className="flex items-center justify-center space-x-2">
              <div className="w-2 h-2 bg-green-500 rounded-full"></div>
              <span>Simple. Uniform. Consistent.</span>
            </div>
            <div className="flex items-center justify-center space-x-2">
              <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
              <span>Interactive Practice Sessions</span>
            </div>
            <div className="flex items-center justify-center space-x-2">
              <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
              <span>Community-Driven Learning</span>
            </div>
          </div>
        </div>
      </div>

      {/* Right Side - Login Form */}
      <div className="w-full lg:w-1/2 flex items-center justify-center p-8">
        <div className="w-full max-w-md space-y-8">
          {/* Mobile Logo */}
          <div className="lg:hidden text-center">
            <Image
              src="/logo.png"
              alt="SyntaxMem"
              width={150}
              height={50}
              className="mx-auto dark:invert"
            />
          </div>

          {/* Header */}
          <div className="text-center space-y-4">
            <h1 className="text-3xl font-bold text-foreground">
              Welcome Back
            </h1>
            <p className="text-muted-foreground">
              Choose your preferred sign-in method to continue your coding journey
            </p>
          </div>

          {/* Login Options */}
          <div className="space-y-4">
            {/* Google Sign In */}
            <form action={async () => {
              "use server"
              await signIn("google", { redirectTo: "/dashboard" })
            }}>
              <button 
                type="submit" 
                className="w-full flex items-center justify-center gap-3 bg-white dark:bg-gray-900 text-gray-700 dark:text-gray-300 border border-gray-300 dark:border-gray-600 px-6 py-4 rounded-xl font-medium hover:bg-gray-50 dark:hover:bg-gray-800 transition-all duration-200 shadow-sm hover:shadow-md"
              >
                <svg className="w-5 h-5" viewBox="0 0 24 24">
                  <path fill="currentColor" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                  <path fill="currentColor" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                  <path fill="currentColor" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                  <path fill="currentColor" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                </svg>
                Continue with Google
              </button>
            </form>

            {/* Divider */}
            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-border"></div>
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="px-4 bg-background text-muted-foreground">or</span>
              </div>
            </div>

            {/* GitHub Sign In - Coming Soon */}
            <div className="relative">
              <button 
                disabled
                className="w-full flex items-center justify-center gap-3 bg-gray-900 dark:bg-gray-800 text-white border border-gray-700 px-6 py-4 rounded-xl font-medium opacity-60 cursor-not-allowed transition-all duration-200"
              >
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                </svg>
                Continue with GitHub
              </button>
              
              {/* Coming Soon Badge */}
              <div className="absolute -top-2 -right-2 bg-gradient-to-r from-purple-500 to-blue-500 text-white text-xs px-2 py-1 rounded-full font-medium">
                Coming Soon
              </div>
            </div>
          </div>


          {/* Terms */}
          <div className="text-center text-sm text-muted-foreground">
            By signing in, you agree to our{" "}
            <a href="/terms" className="text-foreground hover:underline">Terms of Service</a>
            {" "}and{" "}
            <a href="/privacy" className="text-foreground hover:underline">Privacy Policy</a>
          </div>
        </div>
      </div>
    </div>
  )
}