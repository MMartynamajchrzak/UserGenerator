from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import ApiUserViewSet, UserViewSet, GetUsers

urlpatterns = [
    path("docs/schema/", SpectacularAPIView.as_view(), name="docs"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="docs"), name="swagger-ui"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", ApiUserViewSet.as_view({'post': 'create'}), name='register_user'),
    path("", UserViewSet.as_view({"post": "create"}), name='generate_user'),
    path("edit/<int:pk>/", UserViewSet.as_view({"put": "update"}), name='edit_user'),
    path("show/", GetUsers.as_view({"get": "list"}), name="list_users"),
    path("<int:pk>/", GetUsers.as_view({"get": "retrieve"}), name='get_user')
]
