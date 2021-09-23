from django.urls import path

from .views import UserViewSet, GetUsers

urlpatterns = [
    path("", UserViewSet.as_view({"post": "create"}), name='generate_user'),
    path("<int:pk>/", UserViewSet.as_view({"put": "update"}), name='edit_user'),
    path("", GetUsers.as_view({"get": "list"}), name="list_users"),
    path("<int:pk>/", GetUsers.as_view({"get": "retrieve"}), name='get_user')
]
