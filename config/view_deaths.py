from measuremeterdata.models import Measure, Country, MeasureType, MeasureCategory, CHCases, CHCanton, CHMeasure, CasesDeaths, BELProvince, BELCases, BELAgeGroups
from django.shortcuts import get_object_or_404, render
from datetime import date, timedelta
from django.template import loader
from django.http import HttpResponse
from django.db.models import F, Func

def get_deaths(country_id):
    country = Country.objects.get(pk=country_id)
    deaths = CasesDeaths.objects.filter(country=country).order_by("date")
    return deaths

def get_globalvalues(country_id):
    country = Country.objects.get(pk=country_id)
    return country

def country_deaths(request):

    deaths = get_deaths(1)
    country = get_globalvalues(1)

    template = loader.get_template('pages/deaths.html')

    context = {
        'deaths': deaths,
        'country': country
    }

    return HttpResponse(template.render(context, request))
