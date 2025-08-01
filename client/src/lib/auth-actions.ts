// Auth actions for client-side authentication operations
// Simple, Uniform, Consistent

export async function logoutAllDevices(accessToken: string) {
  try {
    const response = await fetch(`${process.env.NEXT_PUBLIC_AUTH_API_URL || 'http://localhost:8081'}/logout-all`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json',
      },
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.message || 'Failed to logout all devices')
    }

    const data = await response.json()
    return data
  } catch (error) {
    console.error('Logout all devices failed:', error)
    throw error
  }
}

export async function logout(refreshToken: string) {
  try {
    const response = await fetch(`${process.env.NEXT_PUBLIC_AUTH_API_URL || 'http://localhost:8081'}/logout`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        refreshToken: refreshToken,
      }),
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.message || 'Failed to logout')
    }

    const data = await response.json()
    return data
  } catch (error) {
    console.error('Logout failed:', error)
    throw error
  }
}