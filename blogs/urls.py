from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BlogCategoryViewSet, BlogViewSet, BlogCommentViewSet

router = DefaultRouter()
router.register(r"categories", BlogCategoryViewSet, basename="blog-categories")
router.register(r"", BlogViewSet, basename="blogs")
router.register(r"comments", BlogCommentViewSet, basename="blog-comments")

urlpatterns = [
	path("", include(router.urls)),
] 