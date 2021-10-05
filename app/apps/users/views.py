from rest_framework import viewsets, permissions, mixins

from .models import User
from .serializers import UserSerializer


class MustBeCreatorViewSet(viewsets.GenericViewSet,
                           mixins.CreateModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    # owner for post and put `and del
    # consider option of creating multiple users at once

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(creator=user)


class FreePermissionViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.RetrieveModelMixin):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.all()
