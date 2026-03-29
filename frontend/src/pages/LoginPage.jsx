import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import { useAuth } from '../context/AuthContext'

export default function LoginPage() {
  const [form, setForm] = useState({ email: '', password: '' })
  const [error, setError] = useState('')
  const { login } = useAuth()
  const navigate = useNavigate()

  const onSubmit = async (event) => {
    event.preventDefault()
    setError('')
    try {
      await login(form)
      navigate('/dashboard')
    } catch {
      setError('Login failed. Check credentials.')
    }
  }

  return (
    <form className="panel form" onSubmit={onSubmit}>
      <h2>Welcome Back</h2>
      {error && <p className="error">{error}</p>}
      <label>Email<input type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} required /></label>
      <label>Password<input type="password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} required /></label>
      <button className="cta" type="submit">Login</button>
      <p>Need an account? <Link to="/signup">Sign up</Link></p>
    </form>
  )
}
