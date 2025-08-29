from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet
# Create a router and register our ViewSet with it.
router = DefaultRouter()
router.register(r'users', UserViewSet) # will create /api/users/ and /api/users/{id}/

urlpatterns = [
	path("", SpectacularSwaggerView.as_view(url_name="schema"), name="root"),
	path("admin/", admin.site.urls),
	path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
	path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
	path("api/auth/", include("users.urls")),
	path("api/recipes/", include("recipes.urls")),
	path("api/blogs/", include("blogs.urls")),
	path("api/interactions/", include("interactions.urls")),
    path("api/", include(router.urls)),
    path("api/auth/", include("users.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)