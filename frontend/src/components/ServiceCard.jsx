import { Link } from 'react-router-dom'
import { resolveMediaUrl } from '../utils/media'

export default function ServiceCard({ service }) {
  return (
    <article className="service-card">
      <div className="service-cover-wrap">
        {service.image ? (
          <img className="service-cover" src={resolveMediaUrl(service.image)} alt={service.title} />
        ) : (
          <div className="service-cover placeholder">No image</div>
        )}
      </div>
      <h3>{service.title}</h3>
      <p>{service.description}</p>
      <div className="service-meta">
        <span className="freelancer-chip">
          {service.freelancer_profile_photo ? (
            <img src={resolveMediaUrl(service.freelancer_profile_photo)} alt={service.freelancer_name} className="avatar tiny" />
          ) : (
            <span className="avatar tiny fallback">{service.freelancer_name?.charAt(0)}</span>
          )}
          {service.freelancer_name}
        </span>
        <span>${service.price}</span>
        <span>{service.rating}★</span>
      </div>
      <Link to={`/services/${service.id}`}>View details</Link>
    </article>
  )
}
