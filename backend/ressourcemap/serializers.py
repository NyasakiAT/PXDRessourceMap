from django.contrib.auth.models import User, Group
from .models import RessourceNode, Ressource, Map, RessourceCategory
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class RessourceNodeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RessourceNode
        fields = ['id', 'x', 'y', 'ressource', 'map']

class RessourceCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RessourceCategory
        fields = ['id', 'name']

class RessourceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ressource
        fields = ['id', 'name', 'icon', 'description', 'ressource_category']

class MapSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Map
        fields = ['id', 'name', 'image']