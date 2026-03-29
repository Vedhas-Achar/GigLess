import api from './client'

export const fetchServices = (params) => api.get('/services/', { params })
export const fetchCategories = () => api.get('/services/categories/')
export const fetchService = (id) => api.get(`/services/${id}/`)
export const createService = (payload, config = {}) => api.post('/services/', payload, config)
