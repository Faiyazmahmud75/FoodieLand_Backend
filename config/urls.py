from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
	path("", SpectacularSwaggerView.as_view(url_name="schema"), name="root"),
	path("admin/", admin.site.urls),
	path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
	path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
	path("api/auth/", include("users.urls")),
	path("api/recipes/", include("recipes.urls")),
	path("api/blogs/", include("blogs.urls")),
	path("api/interactions/", include("interactions.urls")),
] 