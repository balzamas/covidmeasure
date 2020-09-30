from django.contrib import admin
from django import forms
from .models import Country, MeasureCategory, MeasureType, Measure, Continent, CasesDeaths, CHCanton, CHMeasureType, CHMeasure, CHCases

admin.site.register(Continent)
admin.site.register(MeasureCategory)
admin.site.register(CasesDeaths)

class CHCasesAdmin(admin.ModelAdmin):
    list_display = ['canton', 'date', 'cases', 'cases_past14days', 'cases_past7days']
    search_fields = ['canton']
    list_filter = ('canton','date')
admin.site.register(CHCases, CHCasesAdmin)


class CountryAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']
admin.site.register(Country, CountryAdmin)


class MeasureTypeAdmin(admin.ModelAdmin):
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
    ordering = ['country__name', 'type__category', 'type__name']
    autocomplete_fields = ['country', 'type']
    actions = [duplicate_record]
    list_filter = ('country', 'type', 'type__category')
    form = MeasureAddForm
admin.site.register(Measure, MeasureAdmin)

class CantonAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']
    ordering = ['name']
    search_fields = ['name']
admin.site.register(CHCanton, CantonAdmin)

class CHMeasureTypeAdmin(admin.ModelAdmin):
    # a list of displayed columns name.
    list_display = ['name', 'isactive', 'comment']
    ordering = ['name']
    search_fields = ['name']
admin.site.register(CHMeasureType, CHMeasureTypeAdmin)

def duplicate_record(modeladmin, request, queryset):
    for object in queryset:
        object.id = None
        object.save()
duplicate_record.short_description = "Duplicate selected record"

class CHMeasureAddForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start")
        end_date = cleaned_data.get("end")
        print(end_date)
        if end_date != None and start_date != None and end_date < start_date:
            raise forms.ValidationError("End date should be greater than start date.")

class CHMeasureAdmin(admin.ModelAdmin):
    # a list of displayed columns name.
    list_display = ['canton', 'type', 'level', 'comment', 'start', 'end']
    ordering = ['canton__name', 'type__name']
    autocomplete_fields = ['canton', 'type']
    actions = [duplicate_record]
    list_filter = ('canton', 'type')
    form = CHMeasureAddForm
admin.site.register(CHMeasure, CHMeasureAdmin)
