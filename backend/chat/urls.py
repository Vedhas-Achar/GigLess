from django.urls import path

from .views import ChatWebSocketTokenView, ConversationListCreateView, MessageListCreateView

urlpatterns = [
    path('conversations/', ConversationListCreateView.as_view(), name='conversation-list-create'),
    path('conversations/<int:conversation_id>/messages/', MessageListCreateView.as_view(), name='message-list-create'),
    path('ws-token/', ChatWebSocketTokenView.as_view(), name='chat-ws-token'),
]
