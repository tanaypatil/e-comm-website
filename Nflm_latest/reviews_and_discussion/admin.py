from django.contrib import admin
from .models import Review,Discussion,ReviewImage

# Register your models here.


class ReviewAdmin(admin.ModelAdmin):
    model = Review
    list_display = ('user', 'product', 'rating',)
    search_fields = ['product__title', 'user__username']

admin.site.register(Review, ReviewAdmin)


class ReviewImageAdmin(admin.ModelAdmin):
    model = ReviewImage
    list_display = ('review', 'active',)
    list_filter = ['active',]
    search_fields = ['review__nickname',]
    readonly_fields = ['updated']

admin.site.register(ReviewImage, ReviewImageAdmin)


class DiscussionAdmin(admin.ModelAdmin):
    model = Discussion
    list_display = ('user', 'product', 'text',)
    search_fields = ['user', 'product']

admin.site.register(Discussion, DiscussionAdmin)
