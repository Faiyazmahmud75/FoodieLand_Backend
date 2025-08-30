from rest_framework import viewsets, permissions, response, decorators, status
from .models import ContactMessage, UserFollow, Newsletter, ContactUsMessage
from .serializers import ContactMessageSerializer, UserFollowSerializer, NewsletterSerializer, ContactUsMessageSerializer
from django.contrib.auth import get_user_model
from rest_framework.decorators import action

User = get_user_model()

class ContactMessageViewSet(viewsets.ModelViewSet):
    serializer_class = ContactMessageSerializer
    permission_classes = [permissions.AllowAny]
    queryset = ContactMessage.objects.all()

    def get_queryset(self):
        if self.request.user.is_authenticated:
            from django.db.models import Q
            return ContactMessage.objects.filter(Q(recipient=self.request.user) | Q(sender_email=self.request.user.email)).order_by("-created_at")
        return ContactMessage.objects.none()

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @decorators.action(detail=True, methods=["post"])
    def reply(self, request, pk=None):
        """
        Fixed reply system - now properly sends reply to original sender as a user
        """
        original_message = self.get_object()
        
        # Find the original sender by email to get their user ID
        try:
            original_sender = User.objects.get(email=original_message.sender_email)
        except User.DoesNotExist:
            return response.Response(
                {"error": "Original sender is not a registered user"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        reply_data = {
            'sender_name': request.user.name or request.user.email,
            'sender_email': request.user.email,
            'message': request.data.get('message'),
            'recipient': original_sender.id,  # Now correctly using user ID
            'parent_message': original_message.id
        }
        
        serializer = self.get_serializer(data=reply_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return response.Response({"detail": "Reply sent successfully"}, status=status.HTTP_201_CREATED)

    
class UserFollowViewSet(viewsets.ModelViewSet):
    serializer_class = UserFollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return UserFollow.objects.none()
        if not self.request.user.is_authenticated:
            return UserFollow.objects.none()
        return UserFollow.objects.filter(follower=self.request.user)

    @decorators.action(detail=False, methods=["post"], url_path="unfollow")
    def unfollow(self, request):
        following_id = request.data.get("following")
        UserFollow.objects.filter(follower=request.user, following_id=following_id).delete()
        return response.Response({"detail": "unfollowed"}, status=status.HTTP_200_OK)

User = get_user_model()

class UserListViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return User.objects.all().exclude(id=self.request.user.id)
    
    def list(self, request):
        users = self.get_queryset()
        data = [{"id": user.id, "name": user.name or user.email, "email": user.email} for user in users]
        return response.Response(data)

class NewsletterViewSet(viewsets.ModelViewSet):
    serializer_class = NewsletterSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Newsletter.objects.all()

    def get_queryset(self):
        return Newsletter.objects.all().order_by("-created_at")


class ContactUsMessageViewSet(viewsets.ModelViewSet):
    serializer_class = ContactUsMessageSerializer
    permission_classes = [permissions.AllowAny]
    queryset = ContactUsMessage.objects.all()

    def get_queryset(self):
        return ContactUsMessage.objects.all().order_by("-created_at")