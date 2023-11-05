from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from ressourcemap import views
from .views import RessourceNodesByMapView, AuthorizedCheckView

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'maps', views.MapViewSet)
router.register(r'ressource-categories', views.RessourceCategoryViewSet)
router.register(r'ressources', views.RessourceViewSet)
router.register(r'ressource-nodes', views.RessourceNodeViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    #path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('auth/', obtain_auth_token, name='api_token_auth'),
    path('auth/isauthenticated', AuthorizedCheckView.as_view(), name='is_authenticated'),
    path('maps/<int:map_id>/nodes/', RessourceNodesByMapView.as_view(), name='map-resource-nodes'),
    path('maps/<int:map_id>/nodes/<int:ressource_id>', RessourceNodesByMapView.as_view(), name='map-resource-nodes-detailed'),
]