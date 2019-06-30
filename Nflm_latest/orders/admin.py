from django.contrib import admin
from .models import Order,OrderItem,PaymentDetails

# Register your models here.


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline, ]
    model = Order
    list_display = ('user', 'date', 'order_id', 'status', 'guest_customer', 'gift_wrap')
    list_filter = ['status', 'guest_customer', 'gift_wrap', 'date']
    search_fields = ['user', 'order_id', 'notes']
    ordering = ['date']

    class Meta:
        model = Order

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(PaymentDetails)
