import api from './client'

export const fetchConversations = () => api.get('/chat/conversations/')
export const createConversation = (payload) => api.post('/chat/conversations/', payload)
export const fetchMessages = (conversationId) => api.get(`/chat/conversations/${conversationId}/messages/`)
export const sendMessage = (conversationId, payload) => api.post(`/chat/conversations/${conversationId}/messages/`, payload)
export const fetchWebSocketToken = () => api.get('/chat/ws-token/')

export const buildChatWebSocketUrl = (conversationId, token) => {
	const apiBase = api.defaults.baseURL || ''
	const wsBase = apiBase.replace(/^http/, 'ws').replace(/\/api\/?$/, '')
	return `${wsBase}/ws/chat/${conversationId}/?token=${encodeURIComponent(token)}`
}
