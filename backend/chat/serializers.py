from rest_framework import serializers

from orders.models import Order
from .models import Conversation, Message


class ConversationSerializer(serializers.ModelSerializer):
    other_user_id = serializers.SerializerMethodField()
    other_user_name = serializers.SerializerMethodField()
    other_user_username = serializers.SerializerMethodField()
    other_user_profile_photo = serializers.SerializerMethodField()
    order_service_title = serializers.CharField(source='order.service.title', read_only=True)

    class Meta:
        model = Conversation
        fields = [
            'id',
            'user_one',
            'user_two',
            'order',
            'order_service_title',
            'other_user_id',
            'other_user_name',
            'other_user_username',
            'other_user_profile_photo',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'user_one', 'user_two', 'created_at', 'updated_at']

    def validate_order(self, value: Order):
        request = self.context.get('request')
        if not request or request.user.id not in [value.customer_id, value.service.freelancer_id]:
            raise serializers.ValidationError('You are not allowed to chat for this order.')
        return value

    def get_other_user_id(self, obj):
        request = self.context.get('request')
        if not request:
            return None
        other = obj.user_two if obj.user_one_id == request.user.id else obj.user_one
        return other.id

    def get_other_user_name(self, obj):
        request = self.context.get('request')
        if not request:
            return None
        other = obj.user_two if obj.user_one_id == request.user.id else obj.user_one
        return other.name

    def get_other_user_username(self, obj):
        request = self.context.get('request')
        if not request:
            return None
        other = obj.user_two if obj.user_one_id == request.user.id else obj.user_one
        return other.username

    def get_other_user_profile_photo(self, obj):
        request = self.context.get('request')
        if not request:
            return None
        other = obj.user_two if obj.user_one_id == request.user.id else obj.user_one
        return other.profile_photo.url if other.profile_photo else None


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.name', read_only=True)
    sender_username = serializers.CharField(source='sender.username', read_only=True)
    order_id = serializers.IntegerField(source='conversation.order_id', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'conversation', 'order_id', 'sender', 'sender_name', 'sender_username', 'content', 'is_read', 'created_at']
        read_only_fields = ['id', 'order_id', 'sender', 'sender_name', 'sender_username', 'is_read', 'created_at']

    def create(self, validated_data):
        validated_data['sender'] = self.context['request'].user
        return super().create(validated_data)
