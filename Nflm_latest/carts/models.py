from __future__ import unicode_literals
from products.models import Product
from managing_users.models import NFLMUser
from marketing.models import Coupon
from django.db import models
from django.db.models.signals import pre_save,post_save,post_delete
from decimal import Decimal
from django.conf import settings

# Create your models here.
try:
    gift_rate = settings.DEFAULT_GIFT_WRAP_RATE
except Exception as e:
    print(str(e))
    raise NotImplementedError(str(e))


class Cart(models.Model):
    user = models.ForeignKey(NFLMUser, null=True)
    coupon = models.ForeignKey(Coupon, null=True, blank=True)
    coupon_discount = models.IntegerField(null=True,blank=True)
    subtotal = models.DecimalField(max_digits=30, decimal_places=2, default=0.00)
    final_total = models.DecimalField(max_digits=30, decimal_places=2, default=0.00)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)
    gift_wrap = models.BooleanField(default=False)
    notes = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return "Cart id: %s" %(self.id)

    def get_final_total(self):
        return self.final_total

    def update_subtotal(self):
        subtotal = 0
        items = self.cart_items.all()
        for item in items:
            subtotal += item.line_total
        if self.gift_wrap:
            self.final_total = subtotal + gift_rate
        else:
            self.final_total = subtotal
        if self.coupon_discount is not None:
            self.final_total = self.final_total - self.coupon_discount
        self.subtotal = subtotal
        self.save()
        return self.final_total


class CartItem(models.Model):
    cart = models.ForeignKey('Cart', related_name="cart_items", null=True, blank=True)
    product = models.ForeignKey(Product)
    quantity = models.IntegerField(default=1)
    line_total = models.DecimalField(default=10.99, max_digits=30, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        try:
            return str(self.cart.id)
        except:
            return self.product.title


def cart_item_pre_save_receiver(sender, instance, *args, **kwargs):
    qty = instance.quantity
    if int(qty) >= 0:
        price = instance.product.get_price()
        line_item_total = Decimal(qty) * Decimal(price)
        instance.line_total = line_item_total


pre_save.connect(cart_item_pre_save_receiver, sender=CartItem)


def cart_item_post_save_receiver(sender, instance, *args, **kwargs):
    instance.cart.update_subtotal()


post_save.connect(cart_item_post_save_receiver, sender=CartItem)

post_delete.connect(cart_item_post_save_receiver, sender=CartItem)