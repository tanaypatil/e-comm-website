from django.contrib import admin
from django.db import models
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from.models import Blog,BlogImage,BlogMetaTag
from django.contrib.admin.widgets import FilteredSelectMultiple

# Register your models here.


class BlogResource(resources.ModelResource):
    class Meta:
        model = Blog


class MetaTagInline(admin.StackedInline):
    model = BlogMetaTag
    extra = 0


class BlogAdmin(ImportExportModelAdmin):
    inlines = [MetaTagInline, ]
    formfield_overrides = {
        models.ManyToManyField: {'widget': FilteredSelectMultiple("Selected", is_stacked=False)},
    }
    date_hierarchy = 'timestamp'#updated
    search_fields = ['title', 'description']
    list_display = ['title', 'user', 'updated']
    readonly_fields = ['updated', 'timestamp']
    prepopulated_fields = {"slug": ("title",)}
    resource_class = BlogResource

    class Meta:
        model = Blog

admin.site.register(Blog, BlogAdmin)


class ImageAdmin(admin.ModelAdmin):
    model = BlogImage
    list_display = ('blog', 'alt_text', 'active', 'updated',)
    list_filter = ['active']
    search_fields = ['blog__title']

admin.site.register(BlogImage, ImageAdmin)


class MetaAdmin(admin.ModelAdmin):
    model = BlogMetaTag
    list_display = ('blog', 'title', 'description',)
    search_fields = ['blog', 'title']

admin.site.register(BlogMetaTag, MetaAdmin)
