from django.urls import path

from .views import MustBeCreatorViewSet, FreePermissionViewSet


urlpatterns = [
    path('', MustBeCreatorViewSet.as_view({'post': 'create'})),
    path('<int:pk>/', MustBeCreatorViewSet.as_view({'put': 'update', 'delete': 'destroy'})),
    path('', FreePermissionViewSet.as_view({'get': 'list'})),
    path('<int:pk>/', FreePermissionViewSet.as_view({'get': 'retrieve'})),
]
