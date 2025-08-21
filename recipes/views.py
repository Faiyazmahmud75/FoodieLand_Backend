from rest_framework import viewsets, permissions, filters, decorators, response, status
from .models import RecipeCategory, Recipe, RecipeRating, UserFavoriteRecipe
from .serializers import RecipeCategorySerializer, RecipeSerializer, RecipeRatingSerializer, UserFavoriteRecipeSerializer

class IsOwnerOrReadOnly(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		if request.method in permissions.SAFE_METHODS:
			return True
		owner = getattr(obj, "author", None) or getattr(obj, "user", None)
		return owner == request.user

class RecipeCategoryViewSet(viewsets.ModelViewSet):
	queryset = RecipeCategory.objects.all().order_by("name")
	serializer_class = RecipeCategorySerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]
	filter_backends = [filters.SearchFilter, filters.OrderingFilter]
	search_fields = ["name","description"]
	ordering_fields = ["name","created_at"]

class RecipeViewSet(viewsets.ModelViewSet):
	queryset = Recipe.objects.select_related("author","category").all().order_by("-created_at")
	serializer_class = RecipeSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
	filter_backends = [filters.SearchFilter, filters.OrderingFilter]
	search_fields = ["title","description","ingredients"]
	ordering_fields = ["created_at","average_rating","total_ratings"]

class RecipeRatingViewSet(viewsets.ModelViewSet):
	serializer_class = RecipeRatingSerializer
	permission_classes = [permissions.IsAuthenticated]
	def get_queryset(self):
		return RecipeRating.objects.filter(user=self.request.user)

class UserFavoriteRecipeViewSet(viewsets.ModelViewSet):
	serializer_class = UserFavoriteRecipeSerializer
	permission_classes = [permissions.IsAuthenticated]
	def get_queryset(self):
		return UserFavoriteRecipe.objects.filter(user=self.request.user) 