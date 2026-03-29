import { useEffect, useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'

import { createConversation } from '../api/chat'
import { createReview, fetchOrders, updateOrderStatus } from '../api/orders'
import { useAuth } from '../context/AuthContext'
import { resolveMediaUrl } from '../utils/media'

function formatDate(value) {
  return new Date(value).toLocaleString()
}

function UserPill({ photo, label }) {
  return (
    <div className="user-pill">
      {photo ? (
        <img src={resolveMediaUrl(photo)} alt={label} className="avatar" />
      ) : (
        <span className="avatar fallback">{label?.charAt(0)}</span>
      )}
      <span>{label}</span>
    </div>
  )
}

function OrderCard({ order, user, onMarkInProgress, onMarkCompleted, onQuickReview, onStartChat }) {
  const isFreelancerOwner = order.freelancer_id === user?.id

  return (
    <article className="order-card">
      <div className="order-head">
        {order.service_image ? (
          <img className="order-service-thumb" src={resolveMediaUrl(order.service_image)} alt={order.service_title} />
        ) : (
          <div className="order-service-thumb placeholder">No image</div>
        )}
        <div>
          <h4>{order.service_title}</h4>
          <p><strong>Price:</strong> ${order.service_price}</p>
          <p><strong>Status:</strong> {order.status}</p>
          <p><strong>Order Date:</strong> {formatDate(order.order_date)}</p>
        </div>
      </div>

      <UserPill photo={order.customer_profile_photo} label={`Customer: @${order.customer_username}`} />

      <div className="row">
        {isFreelancerOwner && order.status === 'pending' && (
          <button onClick={() => onMarkInProgress(order.id)}>Start Work</button>
        )}
        {order.customer === user?.id && order.status === 'in_progress' && (
          <button onClick={() => onMarkCompleted(order.id)}>Mark Complete</button>
        )}
        {order.customer === user?.id && order.status === 'completed' && (
          <button onClick={() => onQuickReview(order.id)}>Leave 5★ Review</button>
        )}
        <button onClick={() => onStartChat(order.id)}>Open Chat</button>
      </div>
    </article>
  )
}

export default function DashboardPage() {
  const { user } = useAuth()
  const navigate = useNavigate()
  const [orders, setOrders] = useState([])

  const loadOrders = async () => {
    const { data } = await fetchOrders()
    setOrders(data)
  }

  useEffect(() => {
    loadOrders()
  }, [])

  const ordersReceived = useMemo(
    () => orders.filter((order) => order.freelancer_id === user?.id),
    [orders, user?.id],
  )

  const ordersPlaced = useMemo(
    () => orders.filter((order) => order.customer === user?.id),
    [orders, user?.id],
  )

  const markInProgress = async (orderId) => {
    await updateOrderStatus(orderId, 'in_progress')
    await loadOrders()
  }

  const markCompleted = async (orderId) => {
    await updateOrderStatus(orderId, 'completed')
    await loadOrders()
  }

  const submitQuickReview = async (orderId) => {
    await createReview(orderId, { rating: 5, comment: 'Great work and timely delivery.' })
    await loadOrders()
  }

  const startChatForOrder = async (orderId) => {
    await createConversation({ order: orderId })
    navigate(`/chat?order=${orderId}`)
  }

  return (
    <section className="dashboard-grid">
      <section className="panel">
        <h2>Orders Received</h2>
        <p className="muted">Freelancer work requests from customers.</p>
        <div className="stack">
          {ordersReceived.map((order) => (
            <OrderCard
              key={order.id}
              order={order}
              user={user}
              onMarkInProgress={markInProgress}
              onMarkCompleted={markCompleted}
              onQuickReview={submitQuickReview}
              onStartChat={startChatForOrder}
            />
          ))}
          {ordersReceived.length === 0 && <p className="state">No received orders yet.</p>}
        </div>
      </section>

      <section className="panel">
        <h2>Orders Placed</h2>
        <p className="muted">Services you purchased from other freelancers.</p>
        <div className="stack">
          {ordersPlaced.map((order) => (
            <OrderCard
              key={order.id}
              order={order}
              user={user}
              onMarkInProgress={markInProgress}
              onMarkCompleted={markCompleted}
              onQuickReview={submitQuickReview}
              onStartChat={startChatForOrder}
            />
          ))}
          {ordersPlaced.length === 0 && <p className="state">No placed orders yet.</p>}
        </div>
      </section>
    </section>
  )
}
