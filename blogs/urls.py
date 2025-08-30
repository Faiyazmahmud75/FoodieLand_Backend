from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BlogCategoryViewSet, BlogViewSet, BlogCommentViewSet

router = DefaultRouter()
router.register(r"blogs/categories", BlogCategoryViewSet, basename="blog-categories")
router.register(r"blogs/comments", BlogCommentViewSet, basename="blog-comments") 
router.register(r"blogs", BlogViewSet, basename="blogs")

urlpatterns = [
    path("", include(router.urls)),
]