from django.contrib import admin
from django.urls import path, include
# Add these two new imports at the top
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('courses.urls'))
]
# Add this to the very bottom:
# This tells Django to serve media files ONLY when in development (DEBUG = True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)