from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import ApiUser
from apps.users.serializers import UserSerializer


class ApiUserSerializer(serializers.ModelSerializer):
    generated_users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = ApiUser
        fields = ['username', 'password', 'is_staff', 'is_superuser', 'generated_users']
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ['is_staff', 'is_superuser']

    def validate(self, attrs):
        attrs['password'] = make_password(attrs['password'])
        return attrs


class TokenSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
