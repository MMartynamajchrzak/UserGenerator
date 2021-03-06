from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):

    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = User
        fields = [
            'gender',
            'first_name',
            'last_name',
            'country',
            'city',
            'email',
            'username',
            'phone',
            'creator',
        ]
