import json
from urllib.parse import parse_qs

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db.models import Q
from rest_framework_simplejwt.tokens import AccessToken

from accounts.models import User
from chat.models import Conversation, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        token = self._token_from_query_string() or self._token_from_cookie_header()
        self.user = await self._get_user_from_token(token)

        if not self.user:
            await self.close()
            return

        allowed = await self._is_conversation_member(self.user.id, self.conversation_id)
        if not allowed:
            await self.close(code=4403)
            return

        self.room_group_name = f'chat_{self.conversation_id}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        payload = json.loads(text_data)
        content = payload.get('content', '').strip()
        if not content:
            return

        message = await self._save_message(self.conversation_id, self.user.id, content)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': {
                    'id': message.id,
                    'conversation': int(self.conversation_id),
                    'order_id': message.conversation.order_id,
                    'sender': self.user.id,
                    'sender_name': self.user.name,
                    'sender_username': self.user.username,
                    'content': message.content,
                    'created_at': message.created_at.isoformat(),
                },
            },
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event['message']))

    @sync_to_async
    def _get_user_from_token(self, token):
        try:
            payload = AccessToken(token)
            return User.objects.get(id=payload['user_id'])
        except Exception:
            return None

    @sync_to_async
    def _is_conversation_member(self, user_id, conversation_id):
        return Conversation.objects.filter(
            id=conversation_id,
        ).filter(
            Q(user_one_id=user_id) | Q(user_two_id=user_id)
        ).exists()

    @sync_to_async
    def _save_message(self, conversation_id, sender_id, content):
        conversation = Conversation.objects.select_related('order', 'order__service').get(id=conversation_id)
        if sender_id not in [conversation.user_one_id, conversation.user_two_id]:
            raise PermissionError('Not allowed in this conversation')
        if conversation.order and sender_id not in [conversation.order.customer_id, conversation.order.service.freelancer_id]:
            raise PermissionError('Not allowed in this order conversation')
        conversation.save(update_fields=['updated_at'])
        return Message.objects.create(conversation=conversation, sender_id=sender_id, content=content)

    def _token_from_query_string(self):
        try:
            query_string = self.scope.get('query_string', b'').decode('utf-8')
            params = parse_qs(query_string)
            token_values = params.get('token', [])
            return token_values[0] if token_values else None
        except Exception:
            return None

    def _token_from_cookie_header(self):
        try:
            header_map = dict(self.scope.get('headers', []))
            cookies = header_map.get(b'cookie', b'').decode('utf-8')
            for part in cookies.split(';'):
                key, _, value = part.strip().partition('=')
                if key == 'access_token':
                    return value
        except Exception:
            return None
        return None
