from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from .models import User
import secrets
from core.utils import send_email
from django.conf import settings

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ["id", "name", "email", "profile_picture", "bio", "is_email_verified", "created_at", "updated_at"]
		read_only_fields = ["id", "is_email_verified", "created_at", "updated_at"]

class RegisterSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True, min_length=8)
	class Meta:
		model = User
		fields = ["name", "email", "password"]

	def create(self, validated_data):
		user = User.objects.create_user(**validated_data)
		token = secrets.token_urlsafe(32)
		user.email_verification_token = token
		user.save(update_fields=["email_verification_token"])
		verify_link = f"{settings.FRONTEND_URL}/verify-email?token={token}"
		send_email(
			"Verify your FoodieLand account",
			f"Click to verify: {verify_link}",
			[user.email]
		)
		return user

class RequestPasswordResetSerializer(serializers.Serializer):
	email = serializers.EmailField()
	def validate(self, attrs):
		email = attrs["email"]
		try:
			user = User.objects.get(email=email)
		except User.DoesNotExist:
			raise serializers.ValidationError("User not found")
		token = secrets.token_urlsafe(32)
		user.password_reset_token = token
		user.password_reset_expires = timezone.now() + timedelta(hours=1)
		user.save(update_fields=["password_reset_token", "password_reset_expires"])
		reset_link = f"{settings.FRONTEND_URL}/reset-password?token={token}"
		send_email("Reset your FoodieLand password", f"Reset link: {reset_link}", [user.email])
		return attrs

class ResetPasswordSerializer(serializers.Serializer):
	token = serializers.CharField()
	new_password = serializers.CharField(min_length=8)

	def validate(self, attrs):
		token = attrs["token"]
		new_password = attrs["new_password"]
		try:
			user = User.objects.get(password_reset_token=token)
		except User.DoesNotExist:
			raise serializers.ValidationError("Invalid token")
		if not user.password_reset_expires or user.password_reset_expires < timezone.now():
			raise serializers.ValidationError("Token expired")
		user.set_password(new_password)
		user.password_reset_token = None
		user.password_reset_expires = None
		user.save()
		return attrs 

class VerifyEmailSerializer(serializers.Serializer):
    token = serializers.CharField()
