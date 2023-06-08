from django.urls import path, include
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.index),
    path('upload', views.upload),
    path('index', views.index),
    path('image1', views.image1),
]
