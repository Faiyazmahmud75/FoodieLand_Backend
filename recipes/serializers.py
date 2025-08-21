from rest_framework import serializers
from .models import RecipeCategory, Recipe, RecipeRating, UserFavoriteRecipe

class RecipeCategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = RecipeCategory
		fields = "__all__"
		read_only_fields = ["id", "recipe_count", "created_at"]

class RecipeSerializer(serializers.ModelSerializer):
	author_name = serializers.CharField(source="author.name", read_only=True)
	class Meta:
		model = Recipe
		fields = ["id","title","description","image","ingredients","preparation_steps","category","author","author_name","average_rating","total_ratings","is_featured","created_at","updated_at"]
		read_only_fields = ["id","author","average_rating","total_ratings","created_at","updated_at"]

	def create(self, validated_data):
		validated_data["author"] = self.context["request"].user
		return super().create(validated_data)

class RecipeRatingSerializer(serializers.ModelSerializer):
	class Meta:
		model = RecipeRating
		fields = "__all__"
		read_only_fields = ["id", "created_at", "updated_at", "user"]

	def validate_rating(self, value):
		if value < 1 or value > 5:
			raise serializers.ValidationError("Rating must be between 1 and 5")
		return value

	def create(self, validated_data):
		validated_data["user"] = self.context["request"].user
		return super().create(validated_data)

class UserFavoriteRecipeSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserFavoriteRecipe
		fields = "__all__"
		read_only_fields = ["id", "created_at", "user"]

	def create(self, validated_data):
		validated_data["user"] = self.context["request"].user
		return super().create(validated_data) 