import uuid
from django.db import models
from django.conf import settings

class ContactMessage(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	sender_name = models.CharField(max_length=255)
	sender_email = models.EmailField()
	message = models.TextField()
	recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="received_messages")
	is_read = models.BooleanField(default=False)
	message_type = models.CharField(max_length=64, default="general")
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Message to {self.recipient.email} from {self.sender_email}"

class UserFollow(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	follower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following")
	following = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="followers")
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ("follower", "following") 