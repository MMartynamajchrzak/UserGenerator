import requests
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions, status, mixins
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.GenericViewSet,
                  mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    # owner for post and put `and del
    # consider option of creating multiple users at once

    def get_queryset(self):
        if self.request.method == 'GET':
            return User.objects.all()
        else:
            user = self.request.user
            return User.objects.filter(creator=user)

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
                "creator": self.request.user.id,
            }

        response = requests.get(f"https://randomuser.me/api/?results={quantity}")
        response.raise_for_status()

        results = response.json()['results']

        # case we have data for more than one person as input
        if type(self.request.data) == list:
            user_data = [
                (
                    _parse_user(self.request.data[i], results[i])
                    if i < len(self.request.data)
                    else _parse_user({}, results[i])
                ) for i in range(quantity)
            ]

        # case it's dict and we iterate just once
        else:
            user_data = [_parse_user(self.request.data, results[0])]

        users = UserSerializer(data=user_data, many=True)
        users.is_valid(raise_exception=True)
        users.save()

        return Response(data=users.data, status=status.HTTP_201_CREATED)
