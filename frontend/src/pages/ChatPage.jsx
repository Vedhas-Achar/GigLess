import { useEffect, useMemo, useRef, useState } from 'react'
import { useSearchParams } from 'react-router-dom'

import { buildChatWebSocketUrl, createConversation, fetchConversations, fetchMessages, fetchWebSocketToken, sendMessage } from '../api/chat'
import { useAuth } from '../context/AuthContext'
import { resolveMediaUrl } from '../utils/media'

function formatTime(value) {
  return new Date(value).toLocaleString()
}

export default function ChatPage() {
  const { user } = useAuth()
  const [searchParams, setSearchParams] = useSearchParams()
  const [conversations, setConversations] = useState([])
  const [activeId, setActiveId] = useState(null)
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [error, setError] = useState('')
  const [isLiveConnected, setIsLiveConnected] = useState(false)
  const wsRef = useRef(null)
  const wsConversationIdRef = useRef(null)

  const orderId = searchParams.get('order')
  const conversationIdParam = searchParams.get('conversation')

  const activeConversation = useMemo(
    () => conversations.find((conversation) => conversation.id === activeId),
    [conversations, activeId],
  )

  const refreshConversations = async (preferredConversationId = null) => {
    const res = await fetchConversations()
    const uniqueByUser = []
    const seenUsers = new Set()

    for (const conversation of res.data) {
      if (seenUsers.has(conversation.other_user_id)) {
        continue
      }
      seenUsers.add(conversation.other_user_id)
      uniqueByUser.push(conversation)
    }

    setConversations(uniqueByUser)

    if (preferredConversationId) {
      const exists = uniqueByUser.some((conversation) => conversation.id === preferredConversationId)
      if (exists) {
        setActiveId(preferredConversationId)
      }
      return
    }

    if (conversationIdParam) {
      const parsed = Number(conversationIdParam)
      if (Number.isInteger(parsed) && uniqueByUser.some((conversation) => conversation.id === parsed)) {
        setActiveId(parsed)
        return
      }
    }

    if (!activeId && uniqueByUser.length) {
      setActiveId(uniqueByUser[0].id)
    }
  }

  useEffect(() => {
    const bootstrap = async () => {
      try {
        if (orderId) {
          const result = await createConversation({ order: Number(orderId) })
          await refreshConversations(result.data.id)
          return
        }
        await refreshConversations()
      } catch {
        setError('Could not load conversations for this order.')
      }
    }

    bootstrap()
  }, [orderId])

  useEffect(() => {
    if (!activeId) return

    const nextParams = new URLSearchParams()
    if (orderId) {
      nextParams.set('order', String(orderId))
    }
    nextParams.set('conversation', String(activeId))
    setSearchParams(nextParams, { replace: true })
  }, [activeId, orderId, setSearchParams])

  useEffect(() => {
    if (!activeId) return

    const targetConversationId = activeId
    let isCancelled = false
    let reconnectTimer = null
    let reconnectAttempt = 0
    let socket = null

    fetchMessages(targetConversationId).then((res) => {
      if (!isCancelled) {
        setMessages(res.data)
      }
    })

    const connect = async () => {
      try {
        const { data } = await fetchWebSocketToken()
        if (isCancelled) return

        socket = new WebSocket(buildChatWebSocketUrl(targetConversationId, data.token))
        wsRef.current = socket
        wsConversationIdRef.current = targetConversationId

        socket.onopen = () => {
          if (isCancelled) return
          setIsLiveConnected(true)
          setError('')
          reconnectAttempt = 0
        }

        socket.onmessage = (event) => {
          if (isCancelled) return
          const message = JSON.parse(event.data)
          if (Number(message.conversation) !== Number(targetConversationId)) {
            return
          }

          setMessages((prev) => {
            if (prev.some((existing) => existing.id === message.id)) {
              return prev
            }
            return [...prev, message]
          })
        }

        socket.onclose = () => {
          if (isCancelled) return
          setIsLiveConnected(false)

          reconnectAttempt += 1
          const waitMs = Math.min(1000 * 2 ** reconnectAttempt, 10000)
          reconnectTimer = setTimeout(() => {
            connect()
          }, waitMs)
        }

        socket.onerror = () => {
          if (isCancelled) return
          setError('Live connection interrupted. Reconnecting...')
        }
      } catch {
        if (isCancelled) return
        setIsLiveConnected(false)
        setError('Unable to initialize chat connection. Retrying...')
        reconnectTimer = setTimeout(() => {
          connect()
        }, 2000)
      }
    }

    connect()

    return () => {
      isCancelled = true
      setIsLiveConnected(false)
      if (reconnectTimer) {
        clearTimeout(reconnectTimer)
      }
      if (socket) {
        socket.close()
      }
      if (wsRef.current === socket) {
        wsRef.current = null
        wsConversationIdRef.current = null
      }
    }
  }, [activeId])

  const onSend = async (event) => {
    event.preventDefault()
    if (!activeId || !input.trim()) return

    const outgoing = input.trim()
    const targetConversationId = activeId
    setInput('')

    try {
      if (
        wsRef.current
        && wsRef.current.readyState === WebSocket.OPEN
        && Number(wsConversationIdRef.current) === Number(targetConversationId)
      ) {
        wsRef.current.send(JSON.stringify({ content: outgoing }))
      } else {
        await sendMessage(targetConversationId, { content: outgoing })
        const refreshed = await fetchMessages(targetConversationId)
        if (Number(targetConversationId) === Number(activeId)) {
          setMessages(refreshed.data)
        }
      }
    } catch {
      setError('Message failed to send.')
    }
  }

  return (
    <section className="chat-layout">
      <aside className="panel">
        <h3>Conversations</h3>
        <div className="stack">
          {conversations.map((conversation) => (
            <button
              key={conversation.id}
              className={conversation.id === activeId ? 'chat-conversation active' : 'chat-conversation'}
              onClick={() => setActiveId(conversation.id)}
            >
              <div className="user-pill">
                {conversation.other_user_profile_photo ? (
                  <img src={resolveMediaUrl(conversation.other_user_profile_photo)} alt={conversation.other_user_name} className="avatar" />
                ) : (
                  <span className="avatar fallback">{conversation.other_user_name?.charAt(0)}</span>
                )}
                <div>
                  <strong>{conversation.other_user_name}</strong>
                  <p>@{conversation.other_user_username}</p>
                  <p>{conversation.order_service_title}</p>
                </div>
              </div>
            </button>
          ))}
          {conversations.length === 0 && <p className="state">No conversations yet.</p>}
        </div>
      </aside>

      <article className="panel">
        <h3>{activeConversation ? `Chat about ${activeConversation.order_service_title}` : 'Messages'}</h3>
        <p className="muted">{isLiveConnected ? 'Live connected' : 'Reconnecting...'}</p>
        {error && <p className="error">{error}</p>}

        <div className="messages">
          {messages.map((message) => {
            const mine = message.sender === user?.id
            return (
              <div key={message.id} className={mine ? 'message-bubble mine' : 'message-bubble'}>
                <p className="message-meta">
                  <strong>{message.sender_name}</strong>
                  <span>{formatTime(message.created_at)}</span>
                </p>
                <p>{message.content}</p>
              </div>
            )
          })}
          {messages.length === 0 && <p className="state">No messages yet.</p>}
        </div>

        <form className="row" onSubmit={onSend}>
          <input value={input} onChange={(e) => setInput(e.target.value)} placeholder="Type message" />
          <button className="cta" type="submit">Send</button>
        </form>
      </article>
    </section>
  )
}
