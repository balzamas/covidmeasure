from django.contrib import admin
from .models import Country, MeasureCategory, MeasureType, Measure, Continent

admin.site.register(Country)
admin.site.register(Continent)
admin.site.register(MeasureCategory)

class MeasureTypeAdmin(admin.ModelAdmin):
    # a list of displayed columns name.
    list_display = ['name', 'category', 'isactive', 'comment']
    ordering = ['category', 'name']
    search_fields = ['name']
admin.site.register(MeasureType, MeasureTypeAdmin)


class MeasureAdmin(admin.ModelAdmin):
    # a list of displayed columns name.
    list_display = ['country', 'type', 'comment', 'start', 'end']
    ordering = ['country', 'type']
    autocomplete_fields = ['type']
admin.site.register(Measure, MeasureAdmin)
