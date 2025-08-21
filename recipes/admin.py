from django.contrib import admin
from .models import RecipeCategory, Recipe, RecipeRating, UserFavoriteRecipe
admin.site.register(RecipeCategory)
admin.site.register(Recipe)
admin.site.register(RecipeRating)
admin.site.register(UserFavoriteRecipe) 