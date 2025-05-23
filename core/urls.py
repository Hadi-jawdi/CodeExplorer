from django.urls import path
from .views import home,search_projects, add_to_favorites

app_name = 'core'

urlpatterns = [
    path('', home, name='home'),
    path('search/', search_projects, name='search_projects'),
    path('add-to-favorites/', add_to_favorites, name='add_to_favorites'),
]

