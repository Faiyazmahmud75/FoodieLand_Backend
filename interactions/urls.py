from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContactMessageViewSet, UserFollowViewSet, UserListViewSet, NewsletterViewSet, ContactUsMessageViewSet

router = DefaultRouter()
router.register(r'contact-messages', ContactMessageViewSet)
router.register(r"follows", UserFollowViewSet, basename="follows")
router.register(r'users', UserListViewSet, basename='user')
router.register(r'newsletter', NewsletterViewSet, basename='newsletter')
router.register(r'contact-us', ContactUsMessageViewSet, basename='contact-us')

urlpatterns = [
	path("", include(router.urls)),
]