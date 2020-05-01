from django.contrib import admin
from .models import Country, MeasureCategory, MeasureType, Measure, Continent

admin.site.register(Continent)
admin.site.register(MeasureCategory)

class CountryAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']
admin.site.register(Country, CountryAdmin)


class MeasureTypeAdmin(admin.ModelAdmin):
    # a list of displayed columns name.
    list_display = ['name', 'category', 'isactive', 'comment']
    ordering = ['category', 'name']
    search_fields = ['name']
admin.site.register(MeasureType, MeasureTypeAdmin)

def duplicate_record(modeladmin, request, queryset):
    for object in queryset:
        object.id = None
        object.save()
duplicate_record.short_description = "Duplicate selected record"

class MeasureAdmin(admin.ModelAdmin):
    # a list of displayed columns name.
    list_display = ['country', 'type', 'partial',  'comment', 'start', 'end']
    ordering = ['country', 'type']
    autocomplete_fields = ['country', 'type']
    actions = [duplicate_record]
    list_filter = ('country', 'type')
admin.site.register(Measure, MeasureAdmin)
