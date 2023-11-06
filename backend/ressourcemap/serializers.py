from django.contrib.auth.models import User, Group
from .models import RessourceNode, Ressource, Map, RessourceCategory, Recipe, RecipeIngredient
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

class RessourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ressource
        fields = ['id', 'name', 'icon', 'image', 'description', 'obtained_from', 'ressource_category', 'used_in']

class RessourceCategorySerializer(serializers.ModelSerializer):
    ressources = RessourceSerializer(many=True, read_only=True)

    class Meta:
        model = RessourceCategory
        fields = ['id', 'name', 'ressources']

class MapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Map
        fields = ['id', 'name', 'image']

class RecipeSerializer(serializers.ModelSerializer):
    ingredients = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'processing_time', 'ingredients', 'amount_crafted']

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

class RecipeIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeIngredient
        fields = ['id', 'resource', 'amount']