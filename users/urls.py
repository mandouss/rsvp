#users/urls.py

from  django.urls import path, include
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name = 'register'),
    path('password/', views.change_password, name = 'change_password'),
    path('password/reset', views.reset_password, name = 'reset_password'),
]
