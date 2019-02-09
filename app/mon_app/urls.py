from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='index_url'),
    path('success/', parsing, name='parsing_url'),
    ]
