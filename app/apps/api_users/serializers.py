from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import ApiUser


class ApiUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApiUser
        fields = ['username', 'password', 'is_staff', 'is_superuser']
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ['is_staff', 'is_superuser']

    def validate(self, attrs):
        attrs['password'] = make_password(attrs['password'])
        return attrs


class TokenSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
