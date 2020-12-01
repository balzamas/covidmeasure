from measuremeterdata.models.models import Country
from measuremeterdata.models.models_ch import CHCanton, CHDeaths
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

def canton_deaths(request):

    cantons = CHCanton.objects.filter(level=0).order_by("name")

    cantons_values = []

    for canton in cantons:
        print(canton)

        cases = CHDeaths.objects.filter(canton=canton).order_by("week")

        week_values_deaths = []
        week_values_avg = []


        for case in cases:
            print(case.week)

            week_values_deaths.append(case.deaths)
            week_values_avg.append(case.average_deaths)

        canton_toadd = {"canton": canton,
                          "all": week_values_deaths,
                          "all_avg": week_values_avg,
                       }
        cantons_values.append(canton_toadd)

    template = loader.get_template('pages/deaths_ch.html')

    context = {
        'cantons': cantons_values,
    }

    return HttpResponse(template.render(context, request))
