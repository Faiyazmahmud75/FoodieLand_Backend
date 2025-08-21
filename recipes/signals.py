from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg, Count
from .models import Recipe, RecipeRating, RecipeCategory

@receiver(post_save, sender=RecipeRating)
@receiver(post_delete, sender=RecipeRating)
def update_recipe_rating(sender, instance, **kwargs):
	recipe = instance.recipe
	agg = recipe.ratings.aggregate(avg=Avg("rating"), count=Count("id"))
	recipe.average_rating = round(agg["avg"] or 0, 2)
	recipe.total_ratings = agg["count"] or 0
	recipe.save(update_fields=["average_rating", "total_ratings"])

@receiver(post_save, sender=Recipe)
@receiver(post_delete, sender=Recipe)
def update_category_count(sender, instance, **kwargs):
	if instance.category_id:
		cat = instance.category
		cat.recipe_count = cat.recipes.count()
		cat.save(update_fields=["recipe_count"]) 