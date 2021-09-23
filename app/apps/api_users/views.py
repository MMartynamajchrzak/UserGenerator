from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import ApiUser
from .serializers import ApiUserSerializer, TokenSerializer


@extend_schema(request=ApiUserSerializer, responses=TokenSerializer)
class ApiUserViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = ApiUserSerializer
    permission_classes = [permissions.AllowAny]
    queryset = ApiUser.objects.all()

    def create(self, request, *args, **kwargs):
        api_user_serializer = self.get_serializer(data=request.data)
        api_user_serializer.is_valid(raise_exception=True)
        api_user = api_user_serializer.save()

        refresh = RefreshToken.for_user(api_user)

        token_serializer = TokenSerializer(
            data={
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }
        )

        token_serializer.is_valid(raise_exception=True)

        headers = self.get_success_headers(token_serializer.data)

        return Response(token_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

