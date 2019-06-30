from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', home, name="home"),
    url(r'^contact$',contact_us, name="contact"),
    url(r'^about$', about, name="about"),
    url(r'^disclaimer$', disclaimer, name="disclaimer"),
    url(r'^delivery$', delivery, name="delivery"),
    url(r'^faq$', faq, name="faq"),
    url(r'^privacy$', privacy, name="privacy"),
    url(r'^refunds$', refunds, name="refunds"),
    url(r'^terms$', terms, name="terms"),
    url(r'^customization$', customization, name="customization"),
    url(r'^how_to_use$', try_before_buy, name="try_before_buy"),
    url(r'^address$',user_addresses, name="user_addresses"),
    url(r'^address/add$',add_address, name="add_address"),
    url(r'^code_generation$', code_generation, name="code_generation"),
    url(r'^code_check$', code_check, name="code_check"),
    url(r'^address/update/(?P<id>\d+)$',update_address, name="update_address"),
    url(r'^address/delete/(?P<id>\d+)$',delete_address, name="delete_address"),
    url(r'^googlef853ae7d9bf10541.html$',google, name="google"),
    url(r'^sitemap.xml$', sitemap, name="sitemap"),
    url(r'^robots.txt$', robots, name="robots"),
]
