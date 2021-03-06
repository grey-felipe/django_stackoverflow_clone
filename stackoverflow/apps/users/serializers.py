from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        extra_kwargs = {'email': {'write_only': True},
                        'password': {'write_only': True}, }
        fields = ('id', 'username', 'email', 'bio', 'image', 'isAdmin', 'password', 'badge',)
        read_only_fields = ('id', 'badge',)

    def validate_password(self, value):
        if len(value) < 8 or not value:
            raise serializers.ValidationError(
                'please provide a password of not less than 8 characters')
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(read_only=True)
    token = serializers.CharField(read_only=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'no such user with this email or password')

        return {'username': user.username, 'token': user.token}


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'bio', 'image', 'badge')
        read_only_fields = ('id', 'username', 'email', 'bio', 'image', 'badge')
