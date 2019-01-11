from django.urls import path, include
from rest_framework.routers import DefaultRouter

from board import views

router = DefaultRouter()
router.register('board', views.BoardViewSet)

app_name = 'board'

urlpatterns = [
    path('', include(router.urls)),
]
