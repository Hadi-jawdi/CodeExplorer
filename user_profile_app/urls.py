from django.urls import path
from . import views

app_name = 'user_profile_app'
urlpatterns =[
    path("add_favorite/", views.add_to_favorites, name = 'add_favorite'),
    path("profile/", views.profile_view, name='profile'),

]