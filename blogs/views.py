from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import BlogCategory, Blog, BlogComment
from .serializers import BlogCategorySerializer, BlogSerializer, BlogCommentSerializer

class IsOwnerOrReadOnly(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		if request.method in permissions.SAFE_METHODS:
			return True
		owner = getattr(obj, "author", None) or getattr(obj, "user", None)
		return owner == request.user

class BlogCategoryViewSet(viewsets.ModelViewSet):
	queryset = BlogCategory.objects.all().order_by("name")
	serializer_class = BlogCategorySerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]
	filter_backends = [filters.SearchFilter, filters.OrderingFilter]
	search_fields = ["name","description"]
	ordering_fields = ["name","created_at"]

class BlogViewSet(viewsets.ModelViewSet):
	queryset = Blog.objects.select_related("author","category").all().order_by("-created_at")
	serializer_class = BlogSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
	filter_backends = [filters.SearchFilter, filters.OrderingFilter]
	search_fields = ["title","description","content"]
	ordering_fields = ["created_at"]

	@action(detail=True, methods=["post"], permission_classes=[permissions.AllowAny])
	def increment_view(self, request, pk=None):
		blog = self.get_object()
		blog.view_count += 1
		blog.save(update_fields=["view_count"])
		return Response({"view_count": blog.view_count})

class BlogCommentViewSet(viewsets.ModelViewSet):
	serializer_class = BlogCommentSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

	def get_queryset(self):
		qs = BlogComment.objects.select_related("blog","user").all().order_by("created_at")
		blog_id = self.request.query_params.get("blog")
		if blog_id:
			qs = qs.filter(blog_id=blog_id)
		return qs 