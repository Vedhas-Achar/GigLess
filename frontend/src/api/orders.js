import api from './client'

export const fetchOrders = () => api.get('/orders/')
export const createOrder = (payload) => api.post('/orders/', payload)
export const updateOrderStatus = (id, status) => api.patch(`/orders/${id}/status/`, { status })
export const createReview = (orderId, payload) => api.post(`/orders/${orderId}/review/`, payload)
export const fetchFreelancerReviews = (freelancerId) => api.get(`/orders/freelancer/${freelancerId}/reviews/`)
