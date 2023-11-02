from django.contrib.auth.models import User, Group
from .models import RessourceNode, Map, RessourceType
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import permissions
from ressourcemap.serializers import UserSerializer, GroupSerializer, RessourceNodeSerializer, MapSerializer, RessourceTypeSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class RessourceNodeViewSet(viewsets.ModelViewSet):
    queryset = RessourceNode.objects.all()
    serializer_class = RessourceNodeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class RessourceTypeViewSet(viewsets.ModelViewSet):
    queryset = RessourceType.objects.all()
    serializer_class = RessourceTypeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class MapViewSet(viewsets.ModelViewSet):
    queryset = Map.objects.all()
    serializer_class = MapSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class RessourceNodesByMapView(generics.ListAPIView):
    serializer_class = RessourceNodeSerializer

    def get_queryset(self):
        # Retrieve the map_id from the URL parameter.
        map_id = self.kwargs['map_id']
        type_id =  self.kwargs['type_id'] if 'type_id' in self.kwargs else None

        # Filter resource nodes by the specified map ID.
        if type_id is not None or 0:
            return RessourceNode.objects.filter(map_id=map_id, ressource_type_id=type_id)
        else:
            return RessourceNode.objects.filter(map_id=map_id)