from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Blog, BlogCategory

@receiver(post_save, sender=Blog)
@receiver(post_delete, sender=Blog)
def update_blog_category_count(sender, instance, **kwargs):
	if instance.category_id:
		cat = instance.category
		cat.blog_count = cat.blogs.count()
		cat.save(update_fields=["blog_count"]) 