from __future__ import unicode_literals
from managing_users.models import NFLMUser
from products.models import Product
from django.db import models

# Create your models here.


class Coupon(models.Model):
    coupon_code = models.CharField(max_length=20,unique=True)
    absolute_discount = models.BooleanField(default=False, help_text="Check this if discount offered is Absolute Amount.")
    cart_discount = models.BooleanField(default=True, help_text="Check this if discount to be offered is on total cart amount.")
    coupon_amount = models.IntegerField(default=0)
    expiry_date = models.DateField(null=True,blank=True)
    minimum_spend = models.IntegerField(default=0)
    maximum_spend = models.IntegerField(default=0)
    exclude_sale_items = models.BooleanField(default=False,help_text="Check this box if coupon should not apply to items on sale")
    products_included = models.ManyToManyField(Product, related_name="products_included_in_coupon",blank=True)
    products_excluded = models.ManyToManyField(Product, related_name="products_excluded_in_coupon",blank=True)
    users_restricted = models.ManyToManyField(NFLMUser,related_name="users_restricted",blank=True)
    usage_limit_per_coupon = models.IntegerField(default=0)
    usage_limit_per_user = models.IntegerField(default=0)
    usage_count = models.IntegerField(default=0)
    active = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return self.coupon_code


class CouponUser(models.Model):
    coupon = models.ForeignKey(Coupon)
    user = models.ForeignKey(NFLMUser,related_name="coupon_user")
    coupon_usage_count = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return self.user.username


class ReferralProgram(models.Model):
    user = models.ForeignKey(NFLMUser, related_name="user_referral")
    coupon = models.ForeignKey(Coupon,null=True,blank=True)
    referral_list = models.ManyToManyField(NFLMUser, related_name="user_referral_list",blank=True)
    referrals_added_count = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return self.user.username


class ReferredList(models.Model):
    referral = models.ForeignKey(ReferralProgram,related_name="referred_list")
    name = models.CharField(max_length=30, blank=True,null=True)
    email = models.EmailField(null=True,blank=True)
    mobile = models.BigIntegerField(null=True,blank=True, default="9999999999")
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return self.email


class AffiliateProgram(models.Model):
    user = models.ForeignKey(NFLMUser, related_name="affiliate_user")
    first_name = models.CharField(max_length=20,blank=True)
    last_name=models.CharField(max_length=20,blank=True)
    company_name = models.CharField(max_length=30,null=True,blank=True)
    website=models.URLField(blank=True)
    coupon = models.ForeignKey(Coupon)
    coupon_used_users = models.ManyToManyField(NFLMUser, related_name="affiliate_coupon_used_users",blank=True)
    successful_usage_count = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return self.user.username


class AffiliateBankingDetails(models.Model):
    affiliate = models.OneToOneField(AffiliateProgram, related_name="affiliate_banking_details",null=True,blank=True)
    bank_name = models.CharField(max_length=30)
    account_no = models.BigIntegerField()
    name = models.CharField(max_length=30)
    branch = models.CharField(max_length=20)
    IFSC_code = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return self.affiliate.first_name
