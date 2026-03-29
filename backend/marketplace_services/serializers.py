from rest_framework import serializers

from accounts.models import User
from .models import Category, Service


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ServiceSerializer(serializers.ModelSerializer):
    freelancer_name = serializers.CharField(source='freelancer.name', read_only=True)
    freelancer_username = serializers.CharField(source='freelancer.username', read_only=True)
    freelancer_profile_photo = serializers.ImageField(source='freelancer.profile_photo', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    rating = serializers.DecimalField(source='freelancer.rating', max_digits=3, decimal_places=2, read_only=True)

    class Meta:
        model = Service
        fields = [
            'id',
            'freelancer',
            'freelancer_name',
            'freelancer_username',
            'freelancer_profile_photo',
            'title',
            'description',
            'image',
            'category',
            'category_name',
            'price',
            'delivery_time',
            'rating',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'freelancer', 'created_at', 'updated_at', 'freelancer_name', 'rating']

    def validate(self, attrs):
        request = self.context.get('request')
        if request and request.method == 'POST' and request.user.role != User.Role.FREELANCER:
            raise serializers.ValidationError('Only freelancers can create services.')
        return attrs

    def create(self, validated_data):
        validated_data['freelancer'] = self.context['request'].user
        return super().create(validated_data)
