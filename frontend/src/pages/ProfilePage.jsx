import { useEffect, useState } from 'react'

import api from '../api/client'
import { useAuth } from '../context/AuthContext'
import { resolveMediaUrl } from '../utils/media'

export default function ProfilePage() {
  const { user, refreshMe } = useAuth()
  const [form, setForm] = useState({ bio: user?.bio || '', skills: user?.skills || '' })
  const [profilePhoto, setProfilePhoto] = useState(null)
  const [message, setMessage] = useState('')

  useEffect(() => {
    setForm({ bio: user?.bio || '', skills: user?.skills || '' })
  }, [user?.bio, user?.skills])

  const onSave = async (event) => {
    event.preventDefault()
    const payload = new FormData()
    payload.append('bio', form.bio)
    payload.append('skills', form.skills)
    if (profilePhoto) {
      payload.append('profile_photo', profilePhoto)
    }

    await api.patch('/auth/me/', payload, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    await refreshMe()
    setMessage('Profile updated.')
  }

  if (!user) return <p className="state">Loading profile...</p>

  return (
    <form className="panel form" onSubmit={onSave}>
      <h2>{user.name}</h2>
      {user.profile_photo ? (
        <img src={resolveMediaUrl(user.profile_photo)} alt={user.name} className="avatar large" />
      ) : (
        <span className="avatar large fallback">{user.name?.charAt(0)}</span>
      )}
      <p>{user.email}</p>
      <p>Role: {user.role}</p>
      <p>Rating: {user.rating} ({user.rating_count} reviews)</p>
      <label>Bio<textarea value={form.bio} onChange={(e) => setForm({ ...form, bio: e.target.value })} /></label>
      <label>Skills (comma separated)<input value={form.skills} onChange={(e) => setForm({ ...form, skills: e.target.value })} /></label>
      <label>
        Profile Photo
        <input type="file" accept="image/*" onChange={(e) => setProfilePhoto(e.target.files?.[0] || null)} />
      </label>
      <button className="cta" type="submit">Save Profile</button>
      {message && <p className="success">{message}</p>}
    </form>
  )
}
