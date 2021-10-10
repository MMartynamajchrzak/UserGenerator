import json

import requests
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

    def create(self, request, *args, quantity, **kwargs):
        r = requests.get(f"https://randomuser.me/api/?results={quantity}")
        generated_data = []
        if r.status_code == 200:
            d = json.dumps(r.json())
            data = json.loads(d)
            n = 0
            for i in range(0, int(len(data))):

                credentials = User(creator=self.request.user,
                                   gender=data['results'][n]['gender'],
                                   first_name=data['results'][n]['name']['first'],
                                   last_name=data['results'][n]['name']['last'],
                                   country=data['results'][n]['location']['country'],
                                   city=data['results'][n]['location']['city'],
                                   email=data['results'][n]['email'],
                                   username=data['results'][n]['login']['username'],
                                   phone=data['results'][n]['phone'],
                                   picture=data['results'][n]['picture']['medium'],
                                   )

                n += 1
                credentials.save()
                serializer = UserSerializer(credentials)
                generated_data.append(serializer.data)

            return Response(data=generated_data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
