import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { useParams } from 'react-router-dom'

import { createOrder } from '../api/orders'
import { fetchService } from '../api/services'
import { resolveMediaUrl } from '../utils/media'

export default function ServiceDetailPage() {
  const { id } = useParams()
  const [service, setService] = useState(null)
  const [message, setMessage] = useState('')

  useEffect(() => {
    fetchService(id).then((res) => setService(res.data))
  }, [id])

  const onHire = async () => {
    await createOrder({ service: Number(id), dummy_payment_status: 'paid' })
    setMessage('Order placed with dummy payment success.')
  }

  if (!service) return <p className="state">Loading service...</p>

  return (
    <section className="panel service-detail-layout">
      <article className="service-detail-main">
        <h2>{service.title}</h2>
        <p>{service.description}</p>
        <p><strong>Category:</strong> {service.category_name}</p>
        <p><strong>Price:</strong> ${service.price}</p>
        <p><strong>Delivery:</strong> {service.delivery_time} days</p>
        <div className="freelancer-preview">
          {service.freelancer_profile_photo ? (
            <img src={resolveMediaUrl(service.freelancer_profile_photo)} alt={service.freelancer_name} className="avatar" />
          ) : (
            <span className="avatar fallback">{service.freelancer_name?.charAt(0)}</span>
          )}
          <div>
            <p>
              <strong>Freelancer:</strong>{' '}
              <Link to={`/freelancers/${service.freelancer}`}>{service.freelancer_name}</Link>
            </p>
            <p>@{service.freelancer_username}</p>
            <p>{service.rating}★ average rating</p>
          </div>
        </div>
        <button className="cta" onClick={onHire}>Hire with dummy payment</button>
        {message && <p className="success">{message}</p>}
      </article>
      <aside className="service-detail-media">
        {service.image ? (
          <img src={resolveMediaUrl(service.image)} alt={service.title} className="service-detail-image" />
        ) : (
          <div className="service-detail-image placeholder">No service image uploaded</div>
        )}
      </aside>
    </section>
  )
}
