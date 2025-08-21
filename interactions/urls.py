from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContactMessageViewSet, UserFollowViewSet

router = DefaultRouter()
router.register(r"messages", ContactMessageViewSet, basename="messages")
router.register(r"follows", UserFollowViewSet, basename="follows")

urlpatterns = [
	path("", include(router.urls)),
] 