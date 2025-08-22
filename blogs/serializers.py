from rest_framework import serializers
from .models import BlogCategory, Blog, BlogComment

class BlogCategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = BlogCategory
		fields = "__all__"
		read_only_fields = ["id","blog_count","created_at"]

class BlogSerializer(serializers.ModelSerializer):
	author_name = serializers.CharField(source="author.name", read_only=True)
	class Meta:
		model = Blog
		fields = ["id","title","description","content","featured_image","author","author_name","category","view_count","is_published","created_at","updated_at"]
		read_only_fields = ["id","author","view_count","created_at","updated_at"]

	def create(self, validated_data):
		validated_data["author"] = self.context["request"].user
		return super().create(validated_data)

class BlogCommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = BlogComment
		fields = "__all__"
		read_only_fields = ["id","created_at","updated_at","user"]

	def create(self, validated_data):
		validated_data["user"] = self.context["request"].user
		return super().create(validated_data) 