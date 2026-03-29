import { useEffect, useState } from 'react'

import { fetchCategories, fetchServices } from '../api/services'
import ServiceCard from '../components/ServiceCard'

export default function ServicesPage() {
  const [services, setServices] = useState([])
  const [categories, setCategories] = useState([])
  const [filters, setFilters] = useState({ keyword: '', category: '', price_min: '', price_max: '', rating_min: '' })

  const loadData = async () => {
    const [servicesRes, categoriesRes] = await Promise.all([
      fetchServices(filters),
      fetchCategories(),
    ])
    setServices(servicesRes.data)
    setCategories(categoriesRes.data)
  }

  useEffect(() => {
    loadData()
  }, [])

  const onSearch = async (event) => {
    event.preventDefault()
    await loadData()
  }

  return (
    <section>
      <form className="panel filters" onSubmit={onSearch}>
        <input placeholder="Search keyword" value={filters.keyword} onChange={(e) => setFilters({ ...filters, keyword: e.target.value })} />
        <select value={filters.category} onChange={(e) => setFilters({ ...filters, category: e.target.value })}>
          <option value="">All Categories</option>
          {categories.map((category) => <option key={category.id} value={category.id}>{category.name}</option>)}
        </select>
        <input placeholder="Min price" type="number" value={filters.price_min} onChange={(e) => setFilters({ ...filters, price_min: e.target.value })} />
        <input placeholder="Max price" type="number" value={filters.price_max} onChange={(e) => setFilters({ ...filters, price_max: e.target.value })} />
        <input placeholder="Min rating" type="number" step="0.1" value={filters.rating_min} onChange={(e) => setFilters({ ...filters, rating_min: e.target.value })} />
        <button className="cta" type="submit">Apply</button>
      </form>
      <div className="grid">
        {services.map((service) => <ServiceCard key={service.id} service={service} />)}
      </div>
    </section>
  )
}
