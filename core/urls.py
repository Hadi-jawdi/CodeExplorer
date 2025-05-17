from django.urls import path
from .views import home,search_projects

app_name = 'core'

urlpatterns = [
    path('', home, name='home'),
    path('search/', search_projects, name='search_projects'),
]

