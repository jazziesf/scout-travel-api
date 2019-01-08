from django.urls import path

from . import views

app_name = 'user'
# which app you are using the create user
# function from is defined here

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
]
