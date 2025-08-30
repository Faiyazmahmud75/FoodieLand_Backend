from rest_framework import serializers
from .models import ContactMessage, UserFollow, Newsletter, ContactUsMessage
from django.contrib.auth import get_user_model

User = get_user_model()

class ContactMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField()
    sender_email = serializers.EmailField()
    recipient_name = serializers.SerializerMethodField()
    is_reply = serializers.SerializerMethodField()
    is_sent_by_me = serializers.SerializerMethodField()
    reply_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ContactMessage
        fields = "__all__"
        read_only_fields = ["id", "is_read", "created_at"]
    
    def get_is_sent_by_me(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.sender_email == request.user.email
        return False

    def get_recipient_name(self, obj):
        return obj.recipient.name or obj.recipient.email
    
    def get_is_reply(self, obj):
        return obj.parent_message is not None
    
    def get_reply_count(self, obj):
        return obj.replies.count() if hasattr(obj, 'replies') else 0

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