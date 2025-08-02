import { NextRequest, NextResponse } from 'next/server'
import { auth } from '@/lib/auth'
import { getToken, encode } from 'next-auth/jwt'

export async function POST(request: NextRequest) {
  try {
    const session = await auth()
    
    if (!session?.user) {
      return NextResponse.json({ error: 'Not authenticated' }, { status: 401 })
    }

    const { backendToken } = await request.json()
    
    if (!backendToken) {
      return NextResponse.json({ error: 'Backend token required' }, { status: 400 })
    }

    // Get the current JWT token
    const token = await getToken({ 
      req: request, 
      secret: process.env.NEXTAUTH_SECRET 
    })
    
    if (!token) {
      return NextResponse.json({ error: 'No session token found' }, { status: 401 })
    }

    // Update the token with new backend token
    const updatedToken = {
      ...token,
      backendToken: backendToken,
    }

    // Encode the updated token
    const encodedToken = await encode({
      token: updatedToken,
      secret: process.env.NEXTAUTH_SECRET!,
      salt: '',
    })

    // Create response with updated session cookie
    const response = NextResponse.json({ success: true })
    
    // Set the updated session token cookie
    response.cookies.set('next-auth.session-token', encodedToken, {
      httpOnly: true,
      sameSite: 'lax',
      path: '/',
      secure: process.env.NODE_ENV === 'production',
    })

    return response
    
  } catch (error) {
    console.error('Failed to update session:', error)
    return NextResponse.json({ error: 'Failed to update session' }, { status: 500 })
  }
}