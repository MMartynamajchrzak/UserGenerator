from django.urls import path

from .views import UserViewSet

urlpatterns = [
    path("", UserViewSet.as_view({"post": "create"}), kwargs={'quantity': 1}),
    path("<int:quantity>/", UserViewSet.as_view({"post": "create"})),
    path("", UserViewSet.as_view({"get": "list"})),
    path("<int:pk>/", UserViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy"})),
]
