from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^coupon_check$',coupon_check, name="coupon_check"),
    url(r'^referral/login', referral_login, name="referral_login"),
    url(r'^affiliate/login', affiliate_login, name="affiliate_login"),
    url(r'^customization/login', customization_login, name="customization_login"),
    url(r'^referral/share',referral_share, name="referral_share"),
    url(r'^affiliate/add$', add_affiliate, name='add_affiliate'),
    url(r'^affiliate/coupon/status/$', affiliate_coupon_status, name='affiliate_coupon_status'),
    url(r'^affiliate/banking/$', affiliate_banking_details, name='affiliate_bank_details'),
    url(r'^affiliate/users/$', affiliate_users, name='affiliate_users'),
    url(r'^referral/users/$', referral_users, name='referral_users'),
]
