from rest_framework import viewsets, permissions

from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
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
