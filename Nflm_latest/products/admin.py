from django.contrib import admin
from django.db import models
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Product, Tag, ProductImage, MetaTag, StockNotification
from django.contrib.admin.widgets import FilteredSelectMultiple


class ProductResource(resources.ModelResource):
    class Meta:
        model = Product


class MetaTagInline(admin.StackedInline):
    model = MetaTag
    extra = 0


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 2


class ProductAdmin(ImportExportModelAdmin):
    inlines = [MetaTagInline, ProductImageInline, ]
    formfield_overrides = {
        models.ManyToManyField: {'widget': FilteredSelectMultiple("Selected", is_stacked=False)},
    }
    date_hierarchy = 'timestamp'
    search_fields = ['title', 'description']
    list_display = ['title', 'sku', 'stock', 'price', 'active', 'updated']
    list_editable = ['price', 'active']
    list_filter = ['price', 'active', 'custom_made']
    readonly_fields = ['updated', 'timestamp']
    prepopulated_fields = {"slug": ("title",)}
    resource_class = ProductResource

    fieldsets = (
        (None, {'fields': ('title', 'slug', 'sku', 'stock',)}),
        ('Description', {'fields': ('tags', 'highlights', 'description',)}),
        ('Price', {'fields': ('price', 'sale_price',)}),
        ('Boolean Fields', {'fields': ('active', 'exclusive', 'new_arrival', 'occasional', 'custom_made')}),
        ('Time', {'fields': ('timestamp', 'updated',)}),
    )

    class Meta:
        model = Product

admin.site.register(Product, ProductAdmin)


class TagAdmin(admin.ModelAdmin):
    model = Tag
    list_display = ('title', 'description', 'active')
    list_filter = ['active']
    search_fields = ['title']

admin.site.register(Tag, TagAdmin)


class ImageAdmin(admin.ModelAdmin):
    model = ProductImage
    list_display = ['product', 'alt_text', 'active', 'updated']
    list_filter = ['active']
    search_fields = ['product__title']

admin.site.register(ProductImage, ImageAdmin)


class MetaAdmin(admin.ModelAdmin):
    model = MetaTag
    list_display = ('product', 'title', 'description',)
    search_fields = ['product', 'title']

admin.site.register(MetaTag, MetaAdmin)


class StockNotificationAdmin(admin.ModelAdmin):
    model = StockNotification
    list_display = ('product', 'email', 'mobile', 'date_added')
    search_fields = ['product', 'email']

admin.site.register(StockNotification, StockNotificationAdmin)