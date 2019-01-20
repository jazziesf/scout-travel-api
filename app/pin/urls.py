from django.urls import path, include
from rest_framework.routers import DefaultRouter

from pin import views


router = DefaultRouter()
router.register('tags', views.TagViewSet)
router.register('categories', views.CategoriesViewSet)
router.register('pin', views.PinViewSet)
router.register('available', views.AvailablePinViewSet)
router.register('mypins', views.MyPinsViewSet)



app_name = 'pin'

urlpatterns = [
    path('', include(router.urls))
]
