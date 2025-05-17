from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'account_app'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(
        template_name='account_app/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='account_app/password_reset_confirm.html',
        success_url='/account/password_reset_complete/'
    ), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='account_app/password_reset_complete.html'
    ), name='password_reset_complete'),
]
