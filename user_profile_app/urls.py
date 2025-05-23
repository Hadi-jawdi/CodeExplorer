from django.urls import path
from . import views

app_name = 'user_profile_app'

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('favorites/add/', views.add_to_favorites, name='add_to_favorites'),
    path('favorites/delete/<int:repo_id>/', views.delete_favorite, name='delete_favorite'),
]
