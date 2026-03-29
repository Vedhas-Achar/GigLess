import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import { useAuth } from '../context/AuthContext'

export default function SignupPage() {
  const [form, setForm] = useState({ name: '', username: '', email: '', password: '', role: 'customer' })
  const [error, setError] = useState('')
  const { signup } = useAuth()
  const navigate = useNavigate()

  const onSubmit = async (event) => {
    event.preventDefault()
    setError('')
    try {
      await signup(form)
      navigate('/dashboard')
    } catch {
      setError('Sign up failed. Ensure email is unique and password is strong.')
    }
  }

  return (
    <form className="panel form" onSubmit={onSubmit}>
      <h2>Create account</h2>
      {error && <p className="error">{error}</p>}
      <label>Name<input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required /></label>
      <label>Username<input value={form.username} onChange={(e) => setForm({ ...form, username: e.target.value })} required /></label>
      <label>Email<input type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} required /></label>
      <label>Password<input type="password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} required minLength={8} /></label>
      <label>
        Role
        <select value={form.role} onChange={(e) => setForm({ ...form, role: e.target.value })}>
          <option value="customer">Customer</option>
          <option value="freelancer">Freelancer</option>
        </select>
      </label>
      <button className="cta" type="submit">Sign up</button>
      <p>Already registered? <Link to="/login">Login</Link></p>
    </form>
  )
}
