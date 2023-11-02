from django.contrib.auth.models import User, Group
from .models import RessourceNode, RessourceType, Map
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
        fields = ['id', 'x', 'y', 'ressource_type', 'map']

class RessourceTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RessourceType
        fields = ['id', 'name', 'icon']

class MapSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Map
        fields = ['id', 'name', 'image']