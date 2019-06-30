from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^$', vote, name='vote'),
    url(r'^vote$', rateart, name='rateart'),
    url(r'^addup$', addup, name='addup')
]
