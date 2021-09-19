from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path("docs/schema/", SpectacularAPIView.as_view(), name="docs"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="docs"), name="swagger-ui"),
]
