import uuid
from django.db import models
from django.conf import settings

class BlogCategory(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=120, unique=True)
	description = models.TextField(blank=True, null=True)
	color = models.CharField(max_length=7, blank=True, null=True)
	blog_count = models.PositiveIntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

class Blog(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	title = models.CharField(max_length=255)
	description = models.TextField(blank=True, null=True)
	content = models.TextField()
	featured_image = models.URLField(blank=True, null=True)
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="blogs")
	category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, related_name="blogs")
	view_count = models.PositiveIntegerField(default=0)
	is_published = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.title

class BlogComment(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="comments")
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="blog_comments")
	content = models.TextField()
	parent_comment = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies")
	is_approved = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True) 