from django.contrib import admin
from django import forms
from measuremeterdata.models.models import Country, MeasureCategory, MeasureType_old, Measure_old, Continent, CasesDeaths, CountryMeasure, CountryMeasureType
from measuremeterdata.models.models_ch import CHCanton, CHMeasureType, CHMeasure, CHCases, CHDeaths, DoomsdayClock
from measuremeterdata.models.models_bel import BELCases, BELProvince, BELAgeGroups
from import_export.admin import ImportExportModelAdmin
from import_export import resources

admin.site.register(Continent)
admin.site.register(MeasureCategory)
admin.site.register(BELProvince)
admin.site.register(BELAgeGroups)
admin.site.register(CHDeaths)


def duplicate_record(modeladmin, request, queryset):
    for object in queryset:
        object.id = None
        object.save()
duplicate_record.short_description = "Duplicate selected record"

class MeasureTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'isactive']
    ordering = ['name']
    search_fields = ['name']
admin.site.register(CountryMeasureType, MeasureTypeAdmin)

admin.site.register(DoomsdayClock)

class MeasureAdmin(admin.ModelAdmin):
    list_display = ['country', 'type', 'level', 'last_level','comment', 'start', 'end']
    ordering = ['country__name', 'type__name']
    actions = [duplicate_record]
    search_fields = ['country']
    autocomplete_fields = ['country', 'type']
    list_filter = ('country', 'type')
admin.site.register(CountryMeasure, MeasureAdmin)

class BELCasesAdmin(admin.ModelAdmin):
    list_display = ['province', 'date']
    list_filter = ('province','date')
admin.site.register(BELCases, BELCasesAdmin)


class CasesDeathResource(resources.ModelResource):
    class Meta:
        model = CasesDeaths

class CasesDeathsAdmin(ImportExportModelAdmin):
    list_display = ['country', 'date', 'iso_code', 'cases', 'deaths', 'cases_past14days', 'deaths_past14days', 'development7to7', 'r0median', 'hosp_per_million', 'people_vaccinated_per_hundred', 'tests_smoothed_per_thousand', 'positivity']
    list_filter = ('country','date', 'country__continent')
    resource_class = CasesDeathResource
    def iso_code(self,obj):
        return obj.country.iso_code

admin.site.register(CasesDeaths, CasesDeathsAdmin)

class CHCasesAdmin(admin.ModelAdmin):
    list_display = ['canton', 'date', 'cases', 'incidence_past14days', 'incidence_past7days']
    search_fields = ['canton']
    list_filter = ('canton','date')


admin.site.register(CHCases, CHCasesAdmin)


class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'iso_code',]
    ordering = ['name']
    search_fields = ['name']
admin.site.register(Country, CountryAdmin)


class MeasureTypeAdmin_old(admin.ModelAdmin):
    list_display = ['name', 'category', 'isactive', 'comment']
    ordering = ['category', 'name']
    search_fields = ['name']
admin.site.register(MeasureType_old, MeasureTypeAdmin_old)

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

class MeasureAdmin_old(admin.ModelAdmin):
    # a list of displayed columns name.
    list_display = ['country', 'type', 'level', 'comment', 'start', 'end']
    ordering = ['country__name', 'type__category', 'type__name']
    autocomplete_fields = ['country', 'type']
    actions = [duplicate_record]
    list_filter = ('country', 'type', 'type__category')
    form = MeasureAddForm
admin.site.register(Measure_old, MeasureAdmin_old)

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
