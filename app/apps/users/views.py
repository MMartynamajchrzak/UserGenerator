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
            
            for i in range(0, int(len(data))):
                credentials = User(creator=self.request.user,
                                   gender=data['results'][0]['gender'],
                                   first_name=data['results'][0]['name']['first'],
                                   last_name=data['results'][0]['name']['last'],
                                   country=data['results'][0]['location']['country'],
                                   city=data['results'][0]['location']['city'],
                                   email=data['results'][0]['email'],
                                   username=data['results'][0]['login']['username'],
                                   phone=data['results'][0]['phone'],
                                   picture=data['results'][0]['picture']['medium'],
                                   )

                credentials.save()
                serializer = UserSerializer(credentials)
                generated_data.append(serializer.data)

            return Response(data=generated_data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
