from django.urls import path, include
from rest_framework.routers import DefaultRouter

from pin import views


router = DefaultRouter()
router.register('tags', views.TagViewSet)

app_name = 'pin'

urlpatterns = [
    path('', include(router.urls))
]
