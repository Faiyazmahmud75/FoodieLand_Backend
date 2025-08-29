from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from .models import User
import secrets
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
		return user

class RequestPasswordResetSerializer(serializers.Serializer):
	email = serializers.EmailField()
	def validate(self, attrs):
		email = attrs["email"]
		try:
			user = User.objects.get(email=email)
		except User.DoesNotExist:
			raise serializers.ValidationError("User not found")
		return attrs

class ResetPasswordSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=8)

class VerifyEmailSerializer(serializers.Serializer):
    token = serializers.CharField()
