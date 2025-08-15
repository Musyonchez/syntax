import { NextRequest, NextResponse } from 'next/server';

export function middleware(request: NextRequest) {
  const { nextUrl } = request;

  // Protected routes that require authentication
  const isProtectedRoute = [
    '/dashboard',
    '/practice',
    '/snippets',
    '/analytics'
  ].some(route => nextUrl.pathname.startsWith(route));

  // Auth routes that should redirect to dashboard if already logged in
  const isAuthRoute = [
    '/login',
    '/signup'
  ].some(route => nextUrl.pathname.startsWith(route));

  // For now, allow all routes - authentication will be handled client-side
  // This can be enhanced later with proper session checking
  return NextResponse.next();
}

export const config = {
  matcher: [
    // Skip Next.js internals and all static files, unless found in search params
    '/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)',
    // Always run for API routes
    '/(api|trpc)(.*)',
  ],
};