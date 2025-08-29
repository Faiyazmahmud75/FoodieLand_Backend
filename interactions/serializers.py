from rest_framework import serializers
from .models import ContactMessage, UserFollow, Newsletter, ContactUsMessage

class ContactMessageSerializer(serializers.ModelSerializer):
	class Meta:
		model = ContactMessage
		fields = "__all__"
		read_only_fields = ["id", "is_read", "created_at"]

class UserFollowSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserFollow
		fields = ["id", "follower", "following", "created_at"]
		read_only_fields = ["id", "created_at", "follower"]

	def create(self, validated_data):
		validated_data["follower"] = self.context["request"].user
		return super().create(validated_data) 

class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = ["id", "email", "created_at"]
        read_only_fields = ["id", "created_at"]


class ContactUsMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUsMessage
        fields = "__all__"
        read_only_fields = ["id", "created_at"]