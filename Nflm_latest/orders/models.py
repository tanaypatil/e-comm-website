from __future__ import unicode_literals
from decimal import Decimal
from django.conf import settings
from django.db import models
from datetime import datetime
from products.models import Product
from marketing.models import Coupon


# Create your models here.
from managing_users.models import NFLMUser, UserAddress
from carts.models import Cart


STATUS_CHOICES = (
        ("Started", "Started"),
        ("Processing", "Processing"),
        ("Payment Initiated","payment_initiated"),
        ("Payment Successful", "payment_successful"),
        ("Cancelled", "Cancelled"),
        ("Refunded", "Refunded"),
        ("Completed", "Completed"),
    )

#python tuples
try:
    tax_rate = settings.DEFAULT_TAX_RATE
    shipping_rate = settings.DEFAULT_SHIPPING_CHARGE
except Exception as e:
    print(str(e))
    raise NotImplementedError(str(e))

PAYMENT_CHOICES = (
    ("CCAvenue", 'CCAvenue'),
    ("Instamojo", 'Instamojo'),
)


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    order_id = models.CharField(max_length=120, default='ABC', unique=True)
    date = models.DateTimeField(default=datetime.now)
    guest_customer = models.BooleanField(default=False)
    guest_email = models.EmailField(max_length=30,null=True,blank=True)
    cart = models.ForeignKey(Cart, models.SET_NULL, null=True, blank=True)
    coupon = models.ForeignKey(Coupon, null=True, blank=True)
    coupon_discount = models.IntegerField(null=True,blank=True)
    status = models.CharField(max_length=120, choices=STATUS_CHOICES, default="Started")
    shipping_address = models.ForeignKey(UserAddress, null=True, blank=True)
    shipping_charge = models.IntegerField(default=0)
    payment_method = models.CharField(max_length=20,choices=PAYMENT_CHOICES,default="CCAvenue")
    gift_wrap = models.BooleanField(default=False)
    notes = models.TextField(null=True, blank=True)
    sub_total = models.DecimalField(default=0.00, max_digits=30, decimal_places=2)
    tax_total = models.DecimalField(default=0.00, max_digits=30, decimal_places=2)
    final_total = models.DecimalField(default=0.00, max_digits=30, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return "Order id: %s" %(self.id)

    def get_final_amount(self):
        instance = Order.objects.get(id=self.id)
        two_places = Decimal(10) ** -2
        tax_rate_dec = Decimal("%s" %(tax_rate))
        sub_total_dec = self.sub_total
        tax_total_dec = Decimal(tax_rate_dec * sub_total_dec).quantize(two_places)
        instance.tax_total = tax_total_dec
        instance.final_total = sub_total_dec + tax_total_dec + self.shipping_charge
        instance.save()
        return instance.final_total


class OrderItem(models.Model):
    order = models.ForeignKey('Order',related_name="order_items", null=True, blank=True)
    product = models.ForeignKey(Product)
    quantity = models.IntegerField(default=1)
    line_total = models.DecimalField(default=0.00, max_digits=30, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        try:
            return str(self.cart.id)
        except:
            return self.product.sku


class PaymentDetails(models.Model):
    order = models.ForeignKey(Order)
    payment_id = models.CharField(max_length=40,default="ABCD")
    payment_request_id = models.CharField(max_length=50,default="requestid")
    shorturl = models.URLField(null=True, blank=True)
    longurl = models.URLField(null=True, blank=True)
    mac = models.CharField(max_length=60, null=True, blank=True)
    status = models.CharField(max_length=20, null=True, blank=True)

    def __unicode__(self):
        if self.payment_id:
            return self.payment_id
        else:
            return self.payment_request_id


