export interface User {
  id: string
  email: string
  first_name: string
  last_name: string
  company_name?: string
  industry?: string
  role: 'user' | 'admin' | 'premium'
  subscription: 'free' | 'basic' | 'premium' | 'enterprise'
  created_at: string
  updated_at: string
}

export interface UserProfile {
  id: string
  email: string
  first_name: string
  last_name: string
  company_name?: string
  industry?: string
  avatar_url?: string
  bio?: string
  website?: string
  social_links?: {
    twitter?: string
    linkedin?: string
    github?: string
  }
  preferences?: {
    email_notifications: boolean
    marketing_emails: boolean
    theme: 'light' | 'dark' | 'system'
    timezone: string
  }
  created_at: string
  updated_at: string
}

export interface AuthTokens {
  access_token: string
  refresh_token: string
  expires_in: number
}

export interface LoginCredentials {
  email: string
  password: string
}

export interface RegisterData {
  email: string
  password: string
  first_name: string
  last_name: string
  company_name?: string
  industry?: string
}

export interface PasswordResetRequest {
  email: string
}

export interface PasswordReset {
  token: string
  new_password: string
}

export interface PasswordChange {
  current_password: string
  new_password: string
}
