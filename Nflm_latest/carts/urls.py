from django.conf.urls import url
from .views import add_to_cart, cart_details, view_cart, remove_from_cart, update_cart, add_gift_cart, add_custom_product_to_cart

urlpatterns = [
    url(r'^view_cart$', view_cart, name='view_cart'),
    url(r'^cart_details$', cart_details, name='cart_details'),
    url(r'^add_gift_cart', add_gift_cart, name='add_gift_cart'),
    url(r'^update$', update_cart, name='update_cart'),
    url(r'^remove/(?P<id>\d+)/$', remove_from_cart, name='remove_from_cart'),
    url(r'^(?P<slug>[\w-]+)/$', add_to_cart, name='add_to_cart'),
    url(r'^add_custom_product_to_cart/(?P<slug>[\w-]+)/$', add_custom_product_to_cart, name='add_custom_product_to_cart'),
]
