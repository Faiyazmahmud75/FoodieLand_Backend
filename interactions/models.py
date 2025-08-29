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
	parent_message = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

	def __str__(self):
		return f"Message to {self.recipient.email} from {self.sender_email}"
	
	def is_reply(self):
    		return self.parent_message is not None

class UserFollow(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	follower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following")
	following = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="followers")
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ("follower", "following") 

class Newsletter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class ContactUsMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    enquiry_type = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} from {self.email}"