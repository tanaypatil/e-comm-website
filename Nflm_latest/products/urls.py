from django.conf.urls import include, url
from .views import ProductListView,ProductDetailView,OutofStockNotification,TagListView


urlpatterns = [
    url(r'stock/notification',OutofStockNotification,name="stock_notification"),
    url(r'^tag/page(?P<page>[0-9]+)/$', TagListView.as_view(), name='tag_list'),
    url(r'^page(?P<page>[0-9]+)/$', ProductListView.as_view(), name='product_list'),
    url(r'^(?P<slug>[\w-]+)/$', ProductDetailView.as_view(), name='product_detail'),
]