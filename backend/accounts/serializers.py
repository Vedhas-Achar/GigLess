from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = [
            'id',
            'name',
            'username',
            'email',
            'password',
            'role',
            'bio',
            'skills',
            'profile_photo',
            'rating',
        ]
        read_only_fields = ['id', 'rating']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(email=attrs['email'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'name',
            'username',
            'email',
            'role',
            'bio',
            'skills',
            'profile_photo',
            'rating',
            'rating_count',
        ]
        read_only_fields = ['id', 'email', 'role', 'rating', 'rating_count']
