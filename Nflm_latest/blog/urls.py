from django.conf.urls import include, url
from .views import BlogListView,BlogDetailView


urlpatterns = [
    url(r'^page(?P<page>[0-9]+)/$', BlogListView.as_view(), name='blog_list'),
    url(r'^(?P<slug>[\w-]+)/$', BlogDetailView.as_view(), name='blog_detail'),
]