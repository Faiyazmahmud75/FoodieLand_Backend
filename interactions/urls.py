from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContactMessageViewSet, UserFollowViewSet, UserListViewSet

router = DefaultRouter()
router.register(r'contact-messages', ContactMessageViewSet)
router.register(r"follows", UserFollowViewSet, basename="follows")
router.register(r'users', UserListViewSet, basename='user')

urlpatterns = [
	path("", include(router.urls)),
]