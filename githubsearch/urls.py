from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account_app.urls', namespace='account_app')),
    path('', include('core.urls', namespace='core')),
    path('user_profile/', include('user_profile_app.urls', namespace='user_profile_app')),
    path('explore/', include('explore_app.urls', namespace='explore_app')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
