from django.db.models import Q
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationListCreateView(generics.ListCreateAPIView):
	serializer_class = ConversationSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		user = self.request.user
		return (
			Conversation.objects.select_related('user_one', 'user_two', 'order', 'order__service')
			.filter(Q(user_one=user) | Q(user_two=user))
			.order_by('-updated_at')
		)

	def list(self, request, *args, **kwargs):
		# Keep only the most recent conversation per counterpart user.
		conversations = []
		seen_other_user_ids = set()
		for conversation in self.get_queryset():
			other_user_id = conversation.user_two_id if conversation.user_one_id == request.user.id else conversation.user_one_id
			if other_user_id in seen_other_user_ids:
				continue
			seen_other_user_ids.add(other_user_id)
			conversations.append(conversation)

		serializer = self.get_serializer(conversations, many=True)
		return Response(serializer.data)

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		order = serializer.validated_data['order']
		if request.user.id == order.customer_id:
			current_user = order.customer
			other_user = order.service.freelancer
		else:
			current_user = order.service.freelancer
			other_user = order.customer

		user_one, user_two = (current_user, other_user)
		if user_two.id < user_one.id:
			user_one, user_two = user_two, user_one

		conversation, _ = Conversation.objects.get_or_create(
			user_one=user_one,
			user_two=user_two,
			order=order,
		)
		output = self.get_serializer(conversation)
		return Response(output.data)


class MessageListCreateView(generics.ListCreateAPIView):
	serializer_class = MessageSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		conversation = Conversation.objects.select_related('order', 'order__service').get(pk=self.kwargs['conversation_id'])
		if self.request.user.id not in [conversation.user_one_id, conversation.user_two_id]:
			return Message.objects.none()
		if conversation.order and self.request.user.id not in [conversation.order.customer_id, conversation.order.service.freelancer_id]:
			return Message.objects.none()
		return Message.objects.filter(conversation=conversation).select_related('sender')

	def perform_create(self, serializer):
		conversation = Conversation.objects.select_related('order', 'order__service').get(pk=self.kwargs['conversation_id'])
		if self.request.user.id not in [conversation.user_one_id, conversation.user_two_id]:
			raise PermissionDenied('Not allowed in this conversation')
		if conversation.order and self.request.user.id not in [conversation.order.customer_id, conversation.order.service.freelancer_id]:
			raise PermissionDenied('Not allowed in this order conversation')
		message = serializer.save(conversation=conversation)
		conversation.save(update_fields=['updated_at'])

		channel_layer = get_channel_layer()
		async_to_sync(channel_layer.group_send)(
			f'chat_{conversation.id}',
			{
				'type': 'chat_message',
				'message': {
					'id': message.id,
					'conversation': conversation.id,
					'order_id': conversation.order_id,
					'sender': self.request.user.id,
					'sender_name': self.request.user.name,
					'sender_username': self.request.user.username,
					'content': message.content,
					'created_at': message.created_at.isoformat(),
				},
			},
		)


class ChatWebSocketTokenView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def get(self, request):
		token = AccessToken.for_user(request.user)
		return Response({'token': str(token)})
