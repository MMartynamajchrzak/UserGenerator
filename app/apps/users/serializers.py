from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import User, ApiUser


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['gender', 'first_name', 'last_name', 'country', 'city',
                  'email', 'username', 'phone', 'picture', 'creator']


class ApiUserSerializer(serializers.ModelSerializer):
    generated_users = UsersSerializer(many=True, read_only=True)

    class Meta:
        model = ApiUser
        fields = ['username', 'password', 'is_staff', 'is_superuser']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        password = make_password(attrs['password'])
        return password
