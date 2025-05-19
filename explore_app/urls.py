from django.urls import path
from .views import explore

app_name = 'explore_app'

urlpatterns = [
    path('', explore, name='explore'),
]
