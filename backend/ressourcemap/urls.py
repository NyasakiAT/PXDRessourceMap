from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from ressourcemap import views
from .views import RessourceNodesByMapView

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'maps', views.MapViewSet)
router.register(r'ressource-types', views.RessourceTypeViewSet)
router.register(r'ressources', views.RessourceNodeViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    #path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('auth/', obtain_auth_token, name='api_token_auth'),
    path('maps/<int:map_id>/nodes/', RessourceNodesByMapView.as_view(), name='map-resource-nodes'),
    path('maps/<int:map_id>/nodes/<int:type_id>', RessourceNodesByMapView.as_view(), name='map-resource-nodes'),
]