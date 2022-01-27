from io import BytesIO
from typing import List

import requests
from django.core.files import File
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(creator=user)

    @staticmethod
    def get_users_from_api(quantity: int) -> list:
        response = requests.get(f"https://randomuser.me/api/?results={quantity}")
        response.raise_for_status()

        return response.json()['results']

    @staticmethod
    def get_pictures(results) -> List[BytesIO]:
        pictures = []

        for i in range(len(results)):
            response = requests.get(results[i]['picture']['large'])
            response.raise_for_status()
            picture = BytesIO(response.content)
            pictures.append(picture)

        return pictures

    @extend_schema(responses=UserSerializer)
    def create(self, request, *args, quantity: int, **kwargs):

        def _parse_user(_user, _api):
            return {
                "gender": _user.get("gender") or _api["gender"],
                "first_name": _user.get("first_name") or _api['name']['first'],
                "last_name": _user.get("last_name") or _api['name']['last'],
                "country": _user.get("country") or _api['location']['country'],
                "city": _user.get("city") or _api['location']['city'],
                "email": _user.get("email") or _api["email"],
                "username": _user.get("username") or _api['login']['username'],
                "phone": _user.get("phone") or _api['cell'],
                "creator": self.request.user
            }

        user_api_results = self.get_users_from_api(quantity)

        # case we have data for more than one person as input
        if type(self.request.data) == list:
            if len(self.request.data) >= quantity:
                user_data = [_parse_user(self.request.data[i], user_api_results[i])
                             for i in range(quantity)]

            else:
                # consider using only api data when quantity > len(request.data)
                user_data = []
                for i in range(quantity):
                    if i >= len(self.request.data):
                        user_data.append(_parse_user({}, user_api_results[i]))
                    else:
                        user_data.append(_parse_user(self.request.data[i], user_api_results[i]))

            # case it's dict and we iterate just once
        else:
            user_data = [_parse_user(self.request.data, user_api_results[0])]


        users = UserSerializer(data=user_data, many=True, context={'request': request})
        users.is_valid(raise_exception=True)
        users.save()

        if quantity == 0:
            quantity = 1

        # convert image url to image
        pictures = self.get_pictures(user_api_results)

        for i in range(quantity):
            user = User.objects.get(email=user_data[i]['email'])
            user.picture.save(f"Profile-{user.pk}.jpg", File(pictures[i]))

        return Response(data=users.data, status=status.HTTP_201_CREATED)
