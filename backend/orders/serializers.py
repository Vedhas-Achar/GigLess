from rest_framework import serializers

from marketplace_services.models import Service
from .models import Order, Review


class OrderSerializer(serializers.ModelSerializer):
    service_title = serializers.CharField(source='service.title', read_only=True)
    service_price = serializers.DecimalField(source='service.price', max_digits=10, decimal_places=2, read_only=True)
    service_image = serializers.ImageField(source='service.image', read_only=True)
    service_freelancer_name = serializers.CharField(source='service.freelancer.name', read_only=True)
    service_freelancer_username = serializers.CharField(source='service.freelancer.username', read_only=True)
    service_freelancer_profile_photo = serializers.ImageField(source='service.freelancer.profile_photo', read_only=True)
    freelancer_id = serializers.IntegerField(source='service.freelancer_id', read_only=True)
    customer_username = serializers.CharField(source='customer.username', read_only=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    customer_profile_photo = serializers.ImageField(source='customer.profile_photo', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'customer',
            'customer_username',
            'customer_name',
            'customer_profile_photo',
            'service',
            'service_title',
            'service_price',
            'service_image',
            'service_freelancer_name',
            'service_freelancer_username',
            'service_freelancer_profile_photo',
            'freelancer_id',
            'order_date',
            'status',
            'dummy_payment_status',
        ]
        read_only_fields = ['id', 'customer', 'order_date', 'status']

    def validate_service(self, value: Service):
        if value.freelancer_id == self.context['request'].user.id:
            raise serializers.ValidationError('You cannot order your own service.')
        return value

    def create(self, validated_data):
        validated_data['customer'] = self.context['request'].user
        return super().create(validated_data)


class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']

    def validate_status(self, value):
        if value not in [Order.Status.PENDING, Order.Status.IN_PROGRESS, Order.Status.COMPLETED]:
            raise serializers.ValidationError('Invalid status.')
        return value


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'order', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate(self, attrs):
        order = attrs['order']
        user = self.context['request'].user
        if order.customer_id != user.id:
            raise serializers.ValidationError('Only the order customer can submit review.')
        if order.status != Order.Status.COMPLETED:
            raise serializers.ValidationError('Review is allowed only after completion.')
        if hasattr(order, 'review'):
            raise serializers.ValidationError('Review already exists for this order.')
        rating = attrs['rating']
        if rating < 1 or rating > 5:
            raise serializers.ValidationError('Rating must be between 1 and 5.')
        return attrs
