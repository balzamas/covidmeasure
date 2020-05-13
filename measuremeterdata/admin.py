from django.contrib import admin
from django import forms
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

class MeasureAddForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start")
        end_date = cleaned_data.get("end")
        print(end_date)
        if end_date != None and start_date != None and end_date < start_date:
            raise forms.ValidationError("End date should be greater than start date.")

class MeasureAdmin(admin.ModelAdmin):
    # a list of displayed columns name.
    list_display = ['country', 'type', 'level', 'comment', 'start', 'end']
    ordering = ['country', 'type']
    autocomplete_fields = ['country', 'type']
    actions = [duplicate_record]
    list_filter = ('country', 'type', 'type__category')
    form = MeasureAddForm
admin.site.register(Measure, MeasureAdmin)
