from rest_framework import viewsets, permissions, response, decorators, status
from .models import ContactMessage, UserFollow
from .serializers import ContactMessageSerializer, UserFollowSerializer

class ContactMessageViewSet(viewsets.ModelViewSet):
	serializer_class = ContactMessageSerializer
	permission_classes = [permissions.AllowAny]
	queryset = ContactMessage.objects.all()

	def get_queryset(self):
		if self.request.user.is_authenticated:
			return ContactMessage.objects.filter(recipient=self.request.user).order_by("-created_at")
		return ContactMessage.objects.none()

	def create(self, request, *args, **kwargs):
		return super().create(request, *args, **kwargs)

class UserFollowViewSet(viewsets.ModelViewSet):
	serializer_class = UserFollowSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		return UserFollow.objects.filter(follower=self.request.user)

	@decorators.action(detail=False, methods=["post"], url_path="unfollow")
	def unfollow(self, request):
		following_id = request.data.get("following")
		UserFollow.objects.filter(follower=request.user, following_id=following_id).delete()
		return response.Response({"detail": "unfollowed"}, status=status.HTTP_200_OK) 