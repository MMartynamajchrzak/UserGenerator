from rest_framework import viewsets, mixins, permissions

from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.UpdateModelMixin):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    # owner for post and put
    # consider option of creating multiple users at once

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(creator=user)


class GetUsers(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
