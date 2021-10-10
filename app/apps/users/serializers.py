from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['gender', 'first_name', 'last_name', 'country', 'city',
                  'email', 'username', 'phone', 'picture', 'creator']
        read_only_fields = ['creator']
