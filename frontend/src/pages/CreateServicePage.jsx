import { useEffect, useState } from 'react'

import { fetchCategories, createService } from '../api/services'

export default function CreateServicePage() {
  const [categories, setCategories] = useState([])
  const [form, setForm] = useState({ title: '', description: '', category: '', price: '', delivery_time: 3 })
  const [imageFile, setImageFile] = useState(null)
  const [message, setMessage] = useState('')

  useEffect(() => {
    fetchCategories().then((res) => setCategories(res.data))
  }, [])

  const onSubmit = async (event) => {
    event.preventDefault()
    const payload = new FormData()
    payload.append('title', form.title)
    payload.append('description', form.description)
    payload.append('category', Number(form.category))
    payload.append('price', Number(form.price))
    payload.append('delivery_time', Number(form.delivery_time))
    if (imageFile) {
      payload.append('image', imageFile)
    }

    await createService(payload, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    setMessage('Service created successfully.')
  }

  return (
    <form className="panel form" onSubmit={onSubmit}>
      <h2>Create a Service</h2>
      <label>Title<input value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} required /></label>
      <label>Description<textarea value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} required /></label>
      <label>
        Category
        <select value={form.category} onChange={(e) => setForm({ ...form, category: e.target.value })} required>
          <option value="">Select Category</option>
          {categories.map((category) => <option key={category.id} value={category.id}>{category.name}</option>)}
        </select>
      </label>
      <label>Price<input type="number" value={form.price} onChange={(e) => setForm({ ...form, price: e.target.value })} required /></label>
      <label>Delivery Time (days)<input type="number" value={form.delivery_time} onChange={(e) => setForm({ ...form, delivery_time: e.target.value })} required /></label>
      <label>
        Service Image
        <input type="file" accept="image/*" onChange={(e) => setImageFile(e.target.files?.[0] || null)} />
      </label>
      <button className="cta" type="submit">Publish Service</button>
      {message && <p className="success">{message}</p>}
    </form>
  )
}
