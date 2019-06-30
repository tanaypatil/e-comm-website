from django.contrib import admin
from django.db import models
from .models import Coupon,ReferralProgram,AffiliateProgram,AffiliateBankingDetails,CouponUser,ReferredList
from django.contrib.admin.widgets import FilteredSelectMultiple
from import_export import resources
from import_export.admin import ImportExportModelAdmin
# Register your models here.


class CouponAdmin(admin.ModelAdmin):
    search_fields = ['coupon_code', 'coupon_amount']
    list_display = ['coupon_code', 'coupon_amount', 'expiry_date',]
    list_filter = ['absolute_discount', 'active']
    readonly_fields = ['updated', 'timestamp']
    formfield_overrides = {
        models.ManyToManyField: {'widget': FilteredSelectMultiple("Selected", is_stacked=False)},
    }

    fieldsets = (
        (None, {'fields': ('coupon_code', 'absolute_discount', 'coupon_amount', 'usage_count', 'expiry_date','active')}),
        ('Usage Restriction', {'fields': ('minimum_spend', 'maximum_spend','exclude_sale_items','products_included','products_excluded','users_restricted')}),
        ('Usage Limits', {'fields': ('usage_limit_per_coupon','usage_limit_per_user',)}),
    )

    class Meta:
        model = Coupon

admin.site.register(Coupon,CouponAdmin)


class CouponUserAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': FilteredSelectMultiple("Selected", is_stacked=False)},
    }
    list_display = ('coupon', 'user', 'coupon_usage_count',)
    search_fields = ['coupon__coupon_code', 'user__username',]
    readonly_fields = ['updated', 'timestamp']


    class Meta:
        model = CouponUser


admin.site.register(CouponUser,CouponUserAdmin)


class ReferredListInline(admin.TabularInline):
    model = ReferredList
    extra = 0


class ReferralAdmin(admin.ModelAdmin):
    inlines = [ReferredListInline, ]
    formfield_overrides = {
        models.ManyToManyField: {'widget': FilteredSelectMultiple("Selected", is_stacked=False)},
    }
    model = ReferralProgram
    list_display = ('user', 'coupon', 'referrals_added_count',)
    search_fields = ['user',]
    readonly_fields = ['updated',]

admin.site.register(ReferralProgram, ReferralAdmin)
admin.site.register(ReferredList)


class AffiliateAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': FilteredSelectMultiple("Selected", is_stacked=False)},
    }
    model = AffiliateProgram
    list_display = ('user', 'user_mobile', 'first_name', 'coupon', 'successful_usage_count',)
    search_fields = ['user', 'user__mobile', 'coupon', ]
    readonly_fields = ['updated', ]

    def user_mobile(self, obj):
        return obj.user.mobile

    user_mobile.short_description = 'Mobile'
    user_mobile.admin_order_field = 'user__mobile'

admin.site.register(AffiliateProgram, AffiliateAdmin)


class AffiliateBankingResource(resources.ModelResource):
    class Meta:
        model = AffiliateBankingDetails


class AffiliateBankingAdmin(ImportExportModelAdmin):
    model = AffiliateBankingDetails
    list_display = ('affiliate', 'bank_name', 'branch',)
    search_fields = ['affiliate', 'bank_name', 'branch']
    readonly_fields = ['updated',]

admin.site.register(AffiliateBankingDetails, AffiliateBankingAdmin)