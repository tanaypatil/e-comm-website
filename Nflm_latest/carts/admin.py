from django.contrib import admin
from .models import Cart,CartItem

# Register your models here.


class CartAdmin(admin.ModelAdmin):
    list_filter = ['gift_wrap',]
    readonly_fields = ['updated', 'timestamp']

admin.site.register(Cart,CartAdmin)


class CartItemAdmin(admin.ModelAdmin):
    model = CartItem
    list_display = ('cart', 'product', 'quantity', 'line_total')
    search_fields = ['cart', 'product',]

admin.site.register(CartItem, CartItemAdmin)
