import { Link, NavLink, Outlet, useNavigate } from 'react-router-dom'

import { useAuth } from '../context/AuthContext'

export default function Layout() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const onLogout = async () => {
    await logout()
    navigate('/login')
  }

  return (
    <div className="app-shell">
      <header className="topbar">
        <Link to="/" className="brand">GigLess Campus</Link>
        <nav className="nav-links">
          <NavLink to="/">Home</NavLink>
          <NavLink to="/services">Browse Services</NavLink>
          {user && <NavLink to="/dashboard">Dashboard</NavLink>}
          {user && <NavLink to="/profile">My Profile</NavLink>}
          {user?.role === 'freelancer' && <NavLink to="/services/create">Create Service</NavLink>}
        </nav>
        <div className="auth-actions">
          {!user && <Link to="/login">Login</Link>}
          {!user && <Link to="/signup" className="cta">Sign Up</Link>}
          {user && <button onClick={onLogout}>Logout</button>}
        </div>
      </header>
      <main className="content-wrap">
        <Outlet />
      </main>
    </div>
  )
}
