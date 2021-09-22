from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import User, ApiUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['gender', 'first_name', 'last_name', 'country', 'city',
                  'email', 'username', 'phone', 'picture', 'creator']
        read_only_fields = ['creator']

    """def create(self, validated_data):
        # use API
        """


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
