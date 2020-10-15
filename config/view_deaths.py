from measuremeterdata.models import Measure, Country, MeasureType, MeasureCategory, CHCases, CHCanton, CHMeasure, CasesDeaths, BELProvince, BELCases, BELAgeGroups
from django.shortcuts import get_object_or_404, render
from datetime import timedelta
import datetime
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

    countries = Country.objects.exclude(average_death_per_day=0).order_by("name")

    countries_values = []

    for country in countries:
        startdate = datetime.date(2020, 2, 17)

        cases = CasesDeaths.objects.filter(country=country, date__gte=startdate).order_by("date")

        week_values_coviddeaths = {}
        week_values_alldeaths = {}


        week = 8
        weekday = 1
        week_value_covid = 0
        week_value_all = 0

        print(cases)

        for case in cases:
            if weekday == 8:
                week_values_alldeaths[week] = week_value_all
                week_values_coviddeaths[week] = week_value_covid
                weekday = 1
                week_value_covid = 0
                week_value_all = 0
                week += 1

            week_value_covid += case.deaths
            week_value_all += case.deathstotal
            weekday += 1

        countr_toadd = {"country": country,
                          "covid": week_values_coviddeaths,
                          "all": week_values_alldeaths,
                       }
        countries_values.append(countr_toadd)

    template = loader.get_template('pages/deaths.html')

    context = {
        'countries': countries_values,
    }

    return HttpResponse(template.render(context, request))
