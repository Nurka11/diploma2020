import django.urls
from .views import index, parsing, support, other


urlpatterns = [
    django.urls.path('', index, name='index_url'),
    django.urls.path('parsing/', parsing, name='parsing_url'),
    django.urls.path('support/', support, name='support_url'),
    django.urls.path('other/', other, name='other_url')]
