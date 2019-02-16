from django.urls import path
from .views import index, parsing, support, other


urlpatterns = [
    path('', index, name='index_url'),
    path('parsing/', parsing, name='parsing_url'),
    path('support/', support, name='support_url'),
    path('other/', other, name='other_url')]
