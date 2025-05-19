from django.urls import path
from . import views

app_name = 'explore_app'

urlpatterns = [
    path('', views.explore, name='explore'),
    path('add_favorite/', views.add_favorite, name='add_favorite'),
]
