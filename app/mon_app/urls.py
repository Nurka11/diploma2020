from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='index_url'),
    path('parsing/', parsing, name='parsing_url'),
    path('support/', support, name='support_url'),
    path('other/', other, name='other_url'),
    path('api/productcompetitor', api_get_or_post_productcompetitor, name='api_get_or_post_productcompetitor_url'),
    path('api/productcompetitor/<id>', api_get_productcompetitor_by_id, name='api_get_productcompetitor_by_id_url'),
    # path('api/prodcutmy', api_productmy, name='api_productmy_url'),
    # path('api/match', api_match, name='api_match_url')
]
