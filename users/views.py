from rest_framework import generics, viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import User
from .serializers import UserSerializer, RegisterSerializer, RequestPasswordResetSerializer, ResetPasswordSerializer, VerifyEmailSerializer
from rest_framework.views import APIView

class RegisterView(generics.CreateAPIView):
	serializer_class = RegisterSerializer
	permission_classes = [permissions.AllowAny]

class MeView(generics.RetrieveUpdateAPIView):
	serializer_class = UserSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_object(self):
		return self.request.user

class VerifyEmailView(generics.GenericAPIView):
    serializer_class = VerifyEmailSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data["token"]

        try:
            user = User.objects.get(email_verification_token=token)
        except User.DoesNotExist:
            return Response({"detail": "invalid token"}, status=status.HTTP_400_BAD_REQUEST)

        user.is_email_verified = True
        user.email_verification_token = None
        user.save(update_fields=["is_email_verified", "email_verification_token"])
        return Response({"detail": "email verified"}, status=status.HTTP_200_OK)


class RequestPasswordResetView(generics.GenericAPIView):
	serializer_class = RequestPasswordResetSerializer
	permission_classes = [permissions.AllowAny]
	def post(self, request):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		return Response({"detail": "reset email sent"})

class ResetPasswordView(generics.GenericAPIView):
	serializer_class = ResetPasswordSerializer
	permission_classes = [permissions.AllowAny]
	def post(self, request):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		return Response({"detail": "password reset successful"}) 