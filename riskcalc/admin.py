from django.contrib import admin
from riskcalc.models import BELCases, BELProvince, BELAgeGroups

# Register your models here.
admin.site.register(BELProvince)
admin.site.register(BELAgeGroups)

class BELCasesAdmin(admin.ModelAdmin):
    list_display = ['province', 'date']
    list_filter = ('province','date')
admin.site.register(BELCases, BELCasesAdmin)
