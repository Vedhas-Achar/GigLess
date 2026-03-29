import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'

import { freelancerProfile } from '../api/auth'
import { fetchFreelancerReviews } from '../api/orders'
import { resolveMediaUrl } from '../utils/media'

export default function FreelancerProfilePage() {
  const { id } = useParams()
  const [freelancer, setFreelancer] = useState(null)
  const [reviews, setReviews] = useState([])

  useEffect(() => {
    Promise.all([freelancerProfile(id), fetchFreelancerReviews(id)]).then(([profileRes, reviewsRes]) => {
      setFreelancer(profileRes.data)
      setReviews(reviewsRes.data)
    })
  }, [id])

  if (!freelancer) return <p className="state">Loading freelancer...</p>

  return (
    <section className="panel">
      <h2>{freelancer.name}</h2>
      {freelancer.profile_photo ? (
        <img src={resolveMediaUrl(freelancer.profile_photo)} alt={freelancer.name} className="avatar large" />
      ) : (
        <span className="avatar large fallback">{freelancer.name?.charAt(0)}</span>
      )}
      <p><strong>Username:</strong> @{freelancer.username}</p>
      <p><strong>Skills:</strong> {freelancer.skills || 'Not provided yet'}</p>
      <p><strong>Bio:</strong> {freelancer.bio || 'No bio yet'}</p>
      <p><strong>Rating:</strong> {freelancer.rating} ({freelancer.rating_count} reviews)</p>
      <h3>Reviews</h3>
      <div className="stack">
        {reviews.map((review) => (
          <article key={review.id} className="order-card">
            <p>{review.rating}★</p>
            <p>{review.comment}</p>
          </article>
        ))}
      </div>
    </section>
  )
}
