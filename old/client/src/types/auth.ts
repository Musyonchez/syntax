export interface User {
  user_id: string
  email: string
  name: string
  avatar: string
  role: "user" | "admin"
  preferences: UserPreferences
  stats: UserStats
  created_at: string
  last_active?: string
}

export interface UserPreferences {
  theme: "light" | "dark"
  languages: string[]
  difficulty: number
}

export interface UserStats {
  totalScore: number
  practiceTime: number
  streak: number
  level: number
  achievements: string[]
}

export interface AuthResponse {
  token: string
  user: User
  message: string
}