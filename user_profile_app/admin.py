from django.contrib import admin

from .models import FavoriteRepo,UserProfile
admin.site.register(FavoriteRepo)
admin.site.register(UserProfile)
# Register your models here.
