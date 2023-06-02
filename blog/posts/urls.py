from django.urls import path, include
from . import views

app_name = 'posts'

urlpatterns = [
    path('index', views.index),
    path('image1', views.image1),
]
