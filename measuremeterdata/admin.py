from django.contrib import admin
from .models import Country, MeasureCategory, MeasureType, Measure, Continent

admin.site.register(Country)
admin.site.register(Continent)
admin.site.register(MeasureCategory)

class MeasureTypeAdmin(admin.ModelAdmin):
    # a list of displayed columns name.
    list_display = ['name', 'category', 'isactive', 'comment']
    ordering = ['category', 'name']
admin.site.register(MeasureType, MeasureTypeAdmin)


class MeasureAdmin(admin.ModelAdmin):
    # a list of displayed columns name.
    list_display = ['country', 'type', 'start', 'end']
    ordering = ['country', 'type']
admin.site.register(Measure, MeasureAdmin)
