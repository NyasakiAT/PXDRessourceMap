from django.contrib.auth.models import User, Group
from .models import RessourceNode, Ressource, Map, RessourceCategory, Recipe, RecipeIngredient, CraftingStation
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class RessourceNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RessourceNode
        fields = ['id', 'x', 'y', 'ressource', 'map']

class CraftingStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CraftingStation
        fields = ['id', 'name']  # Add other fields as needed

class RecipeSerializer(serializers.ModelSerializer):
    crafting_station = CraftingStationSerializer()  # Include the crafting station serializer

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'processing_time', 'amount_crafted', 'crafting_station']

    def get_ingredients(self, obj):
        # Retrieve the RecipeIngredients related to this recipe
        ingredients = RecipeIngredient.objects.filter(recipe=obj)

        # Serialize each ingredient with its name and amount
        serialized_ingredients = [
            {
                'name': ingredient.resource.name,
                'amount': ingredient.amount
            }
            for ingredient in ingredients
        ]

        return serialized_ingredients

    def to_representation(self, instance):
        # Override the to_representation method to include ingredients
        representation = super().to_representation(instance)
        representation['ingredients'] = self.get_ingredients(instance)
        return representation

class RessourceSerializer(serializers.ModelSerializer):
    used_in = RecipeSerializer(many=True, read_only=True)

    class Meta:
        model = Ressource
        fields = ['id', 'name', 'icon', 'image', 'description', 'obtained_from', 'ressource_category', 'used_in']

class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = RessourceSerializer()  # Use the correct attribute name 'ingredient'

    class Meta:
        model = RecipeIngredient
        fields = ['id', 'ingredient', 'amount']

class RessourceCategorySerializer(serializers.ModelSerializer):
    ressources = RessourceSerializer(many=True, read_only=True)

    class Meta:
        model = RessourceCategory
        fields = ['id', 'name', 'ressources']

class MapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Map
        fields = ['id', 'name', 'image']

