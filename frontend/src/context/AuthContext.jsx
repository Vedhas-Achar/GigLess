import { createContext, useContext, useEffect, useState } from 'react'

import { login, logout, me, signup } from '../api/auth'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  const refreshMe = async () => {
    try {
      const { data } = await me()
      setUser(data)
    } catch {
      setUser(null)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    refreshMe()
  }, [])

  const handleLogin = async (payload) => {
    const { data } = await login(payload)
    setUser(data.user)
  }

  const handleSignup = async (payload) => {
    const { data } = await signup(payload)
    setUser(data.user)
  }

  const handleLogout = async () => {
    await logout()
    setUser(null)
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        isAuthenticated: Boolean(user),
        login: handleLogin,
        signup: handleSignup,
        logout: handleLogout,
        refreshMe,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  return useContext(AuthContext)
}
