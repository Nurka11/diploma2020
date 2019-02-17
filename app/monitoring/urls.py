from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mon_app.urls'))]

admin.site.site_header = settings.ADMIN_SITE_HEADER
