from django.contrib.auth.models import User, Group
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import RessourceNode, Map, Ressource, RessourceCategory
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import permissions
from ressourcemap.serializers import UserSerializer, GroupSerializer, RessourceNodeSerializer, MapSerializer, RessourceCategorySerializer, RessourceSerializer

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

    def create(self, request, *args, **kwargs):
        try:
            # Handle the resource creation as usual
            return super().create(request, *args, **kwargs)
        except Exception as e:
            # Log any exceptions
            print("Error during resource creation: %s", str(e))
            return Response({"error": "Failed to create resource"}, status=status.HTTP_400_BAD_REQUEST)

class RessourceViewSet(viewsets.ModelViewSet):
    queryset = Ressource.objects.all()
    serializer_class = RessourceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class RessourceCategoryViewSet(viewsets.ModelViewSet):
    queryset = RessourceCategory.objects.all()
    serializer_class = RessourceCategorySerializer
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
        ressource_id =  self.kwargs['ressource_id'] if 'ressource_id' in self.kwargs else None

        # Filter resource nodes by the specified map ID.
        if ressource_id is not None or 0:
            return RessourceNode.objects.filter(map_id=map_id, ressource_id=ressource_id)
        else:
            return RessourceNode.objects.filter(map_id=map_id)
        
class AuthorizedCheckView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        response_data = {'authenticated': 'true'}
        return Response(response_data)