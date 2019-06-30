from django.contrib import admin
from .models import Wishlist,WishlistItem

# Register your models here.

class WhishlistAdmin(admin.ModelAdmin):
    model = Wishlist
    readonly_fields = ['updated', 'timestamp']

admin.site.register(Wishlist, WhishlistAdmin)
admin.site.register(WishlistItem)
