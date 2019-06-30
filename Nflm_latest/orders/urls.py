from django.conf.urls import url
from .views import order_login,user_orders, order_details, InvoiceGeneration, payment_initiated, payment_redirect_url, \
    payment_details_webhook, InvoicePDFView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    url(r'^user_orders/$', user_orders, name='user_orders'),
    url(r'^payment_initiated$', payment_initiated, name='payment_initiated'),
    url(r'^payment_details$', csrf_exempt(payment_details_webhook), name='payment_details'),
    url(r'^payment_completed$', payment_redirect_url, name='payment_completed'),
    url(r'^view_order/(?P<id>\d+)/$$', order_details, name='view_order'),
    url(r'^order_login/(?P<id>\d+)/$', order_login, name='order_login'),
    url(r'^invoice_generation$', InvoiceGeneration, name='invoice_generation'),
    url(r'^invoice.pdf$', InvoicePDFView.as_view(), name='invoice_pdf')
]
