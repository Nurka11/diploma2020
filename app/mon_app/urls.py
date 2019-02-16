from django.urls import path
from .views import index, parsing


urlpatterns = [
    path('', index, name='index_url'),
    path('success/', parsing, name='parsing_url'),
    path('404/', parsing, name='exception_url')]
