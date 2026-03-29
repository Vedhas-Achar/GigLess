import api from './client'

export const login = (payload) => api.post('/auth/login/', payload)
export const signup = (payload) => api.post('/auth/signup/', payload)
export const logout = () => api.post('/auth/logout/')
export const me = () => api.get('/auth/me/')
export const freelancerProfile = (id) => api.get(`/auth/freelancers/${id}/`)
