from django.conf.urls import include, url
from .views import add_review,view_reviews,remove_from_reviews


urlpatterns = [
    url(r'^view_review/$', view_reviews, name='view_review'),
    url(r'^product_id(?P<product_id>[0-9]+)/$', add_review, name='add_review'),
    url(r'^remove/(?P<id>\d+)/$', remove_from_reviews, name='remove_from_reviews'),
]