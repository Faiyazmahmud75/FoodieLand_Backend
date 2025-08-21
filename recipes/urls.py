from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RecipeCategoryViewSet, RecipeViewSet, RecipeRatingViewSet, UserFavoriteRecipeViewSet

router = DefaultRouter()
router.register(r"categories", RecipeCategoryViewSet, basename="recipe-categories")
router.register(r"", RecipeViewSet, basename="recipes")
router.register(r"my/ratings", RecipeRatingViewSet, basename="my-ratings")
router.register(r"my/favorites", UserFavoriteRecipeViewSet, basename="my-favorites")

urlpatterns = [
	path("", include(router.urls)),
] 