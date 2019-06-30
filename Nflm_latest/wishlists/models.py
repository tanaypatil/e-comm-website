from __future__ import unicode_literals
from managing_users.models import NFLMUser
from products.models import Product
from django.db import models

# Create your models here.


class Wishlist(models.Model):
    user = models.ForeignKey(NFLMUser)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return "Wislist id: %s" %(self.id)


class WishlistItem(models.Model):
    wishlist = models.ForeignKey('Wishlist',related_name="wishlist_items", null=True, blank=True)
    product = models.ForeignKey(Product)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        try:
            return str(self.wishlist.id)
        except:
            return self.product.title
