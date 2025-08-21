import uuid
from django.db import models
from django.conf import settings

class RecipeCategory(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=120, unique=True)
	description = models.TextField(blank=True, null=True)
	icon = models.CharField(max_length=255, blank=True, null=True)
	color = models.CharField(max_length=7, blank=True, null=True)
	recipe_count = models.PositiveIntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

class Recipe(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	title = models.CharField(max_length=255)
	description = models.TextField(blank=True, null=True)
	image = models.URLField(blank=True, null=True)
	ingredients = models.JSONField(default=list, blank=True)
	preparation_steps = models.JSONField(default=list, blank=True)
	category = models.ForeignKey(RecipeCategory, on_delete=models.SET_NULL, null=True, related_name="recipes")
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="recipes")
	average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
	total_ratings = models.PositiveIntegerField(default=0)
	is_featured = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.title

class RecipeRating(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="ratings")
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="recipe_ratings")
	rating = models.PositiveSmallIntegerField()
	review = models.TextField(blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		unique_together = ("recipe", "user")

class UserFavoriteRecipe(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="favorite_recipes")
	recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="favorited_by")
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ("user", "recipe") 