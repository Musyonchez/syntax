import { Metadata } from "next";
import { SignInForm } from "@/components/auth/signin-form";
import { AnimatedLoader } from "@/components/auth/animated-loader";
import { Suspense } from "react";

export const metadata: Metadata = {
  title: "Sign In",
  description:
    "Sign in to your SyntaxMem account to start practicing and track your progress.",
};

function SessionExpiredMessage() {
  return (
    <div className="mb-6 p-4 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg">
      <div className="flex items-center space-x-2">
        <svg className="w-5 h-5 text-yellow-600 dark:text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
        </svg>
        <div>
          <h3 className="text-sm font-medium text-yellow-800 dark:text-yellow-200">
            Session Expired
          </h3>
          <p className="text-sm text-yellow-700 dark:text-yellow-300">
            Your session has expired. Please sign in again to continue.
          </p>
        </div>
      </div>
    </div>
  )
}

function SignInContent() {
  return (
    <div className="mx-auto flex w-full flex-col justify-center space-y-6 sm:w-[350px]">
      <div className="flex flex-col space-y-2 text-center">
        <h1 className="text-2xl font-semibold tracking-tight">
          Welcome back
        </h1>
        <p className="text-sm text-muted-foreground">
          Sign in to continue your coding journey
        </p>
      </div>
      <Suspense fallback={null}>
        <SessionExpiredCheck />
      </Suspense>
      <SignInForm />
      <p className="px-8 text-center text-sm text-muted-foreground">
        By clicking continue, you agree to our{" "}
        <a
          href="/terms"
          className="underline underline-offset-4 hover:text-primary"
        >
          Terms of Service
        </a>{" "}
        and{" "}
        <a
          href="/privacy"
          className="underline underline-offset-4 hover:text-primary"
        >
          Privacy Policy
        </a>
        .
      </p>
    </div>
  )
}

function SessionExpiredCheck() {
  if (typeof window === 'undefined') return null
  
  const urlParams = new URLSearchParams(window.location.search)
  const error = urlParams.get('error')
  
  if (error === 'SessionExpired') {
    return <SessionExpiredMessage />
  }
  
  return null
}

export default function SignInPage() {
  return (
    <div className="relative min-h-screen flex flex-col items-center justify-center lg:grid lg:max-w-none lg:grid-cols-2 lg:px-0 lg:container">
      <div className="relative hidden h-full flex-col bg-muted p-10 text-muted-foreground lg:flex dark:border-r">
        <AnimatedLoader />
        <div className="relative z-20 flex items-center text-lg font-medium hover:bg-background/80 hover:backdrop-blur-sm transition-all duration-300 rounded-lg px-3 py-2 -mx-3 -my-2">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            className="mr-2 h-6 w-6"
          >
            <path d="m8 3 4 8 5-5v11H5V6l3-3z" />
          </svg>
          SyntaxMem
        </div>
        <div className="relative z-20 mt-auto">
          <blockquote className="space-y-2 hover:bg-background/80 hover:backdrop-blur-sm transition-all duration-300 rounded-lg px-4 py-3 -mx-4 -my-3">
            <p className="text-lg">
              &quot;SyntaxMem has completely transformed how I practice coding.
              The interactive challenges keep me engaged and the progress
              tracking motivates me to code every day.&quot;
            </p>
            <footer className="text-sm opacity-80">
              Sofia Davis - Software Engineer
            </footer>
          </blockquote>
        </div>
      </div>
      <div className="lg:p-8 p-4">
        <SignInContent />
      </div>
    </div>
  );
}
