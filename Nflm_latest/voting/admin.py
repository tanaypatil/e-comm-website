from django.contrib import admin
from .models import *


class PairAdmin(admin.ModelAdmin):
    list_display = ['pid', 's1', 'a1', 's2', 'a2']
    search_fields = ['pid', 'alt_1', 'alt_2']

    class Meta:
        model = Pairs


admin.site.register(Pairs, PairAdmin)
