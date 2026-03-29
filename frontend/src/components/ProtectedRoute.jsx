import { Navigate } from 'react-router-dom'

import { useAuth } from '../context/AuthContext'

export default function ProtectedRoute({ children }) {
  const { loading, isAuthenticated } = useAuth()

  if (loading) return <p className="state">Checking session...</p>
  if (!isAuthenticated) return <Navigate to="/login" replace />

  return children
}
