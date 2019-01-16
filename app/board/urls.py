from django.urls import path, include
from rest_framework_nested import routers
# from rest_framework import routers


from board import views

router = routers.DefaultRouter()
router.register('board', views.BoardViewSet)

domains_router = routers.NestedSimpleRouter(router, r'board', lookup='board')
domains_router.register(r'pins', views.BoardPinViewSet, base_name='board-pins')

app_name = 'board'

urlpatterns = [
    path('', include(router.urls)),
    path('', include(domains_router.urls)),
]
