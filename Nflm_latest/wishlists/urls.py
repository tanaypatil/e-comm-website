from django.conf.urls import url
from .views import add_to_wishlist,view_wishlist,remove_from_wishlist

urlpatterns = [
    url(r'^view_wishlist$', view_wishlist, name='view_wishlist'),
    url(r'^remove/(?P<id>\d+)/$', remove_from_wishlist, name='remove_from_wishlist'),
    url(r'^(?P<slug>[\w-]+)/$', add_to_wishlist , name='add_to_wishlist'),
]
