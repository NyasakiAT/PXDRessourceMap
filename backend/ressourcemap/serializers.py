from django.contrib.auth.models import User, Group
from .models import RessourceNode, Ressource, Map, RessourceCategory, Recipe, RecipeIngredient, CraftingStation
from rest_framework import serializers

class SimplifiedRessourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ressource
        fields = ['id', 'name', 'icon', 'image', 'description', 'obtained_from', 'stack_size']

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

class MapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Map
        fields = ['id', 'name', 'image']

class RessourceCategorySerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        # Remove the 'ressources' field if 'include_ressources' is not in the context or is False
        include_ressources = kwargs.pop('context', {}).get('include_ressources', False)
        super().__init__(*args, **kwargs)
        if not include_ressources:
            self.fields.pop('ressources', None)

    ressources = SimplifiedRessourceSerializer(many=True, read_only=True)

    class Meta:
        model = RessourceCategory
        fields = ['id', 'name', 'ressources']

class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = SimplifiedRessourceSerializer(read_only=True)

    class Meta:
        model = RecipeIngredient
        fields = ['id', 'ingredient', 'amount']

class RecipeSerializer(serializers.ModelSerializer):
    crafting_station = CraftingStationSerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(many=True, source='recipeingredient_set', read_only=True)

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'processing_time', 'amount_crafted', 'crafting_station', 'ingredients']

class RessourceSerializer(serializers.ModelSerializer):
    # Pass context to the RessourceCategorySerializer to control 'ressources' field inclusion
    ressource_category = serializers.SerializerMethodField()
    used_in = RecipeSerializer(many=True, read_only=True)

    class Meta:
        model = Ressource
        fields = ['id', 'name', 'icon', 'image', 'description', 'obtained_from', 'stack_size', 'ressource_category', 'used_in']

    def get_ressource_category(self, obj):
        serializer = RessourceCategorySerializer(obj.ressource_category, context={'include_ressources': False})
        return serializer.data

class RecipeIngredientRessourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ressource
        fields = ['id', 'name', 'icon']
