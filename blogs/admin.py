from django.contrib import admin
from .models import BlogCategory, Blog, BlogComment
admin.site.register(BlogCategory)
admin.site.register(Blog)
admin.site.register(BlogComment) 