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
        week_values_deaths15 = []
        week_values_deaths19 = []

        total20 = 0
        total19 = 0
        total15 = 0
        total_avg = 0


        for case in cases:
            print(case.week)

            week_values_deaths.append(case.deaths)
            week_values_avg.append(case.average_deaths)
            week_values_deaths19.append(case.deaths19)
            week_values_deaths15.append(case.deaths15)

            total20 += case.deaths
            total19 += case.deaths19
            total15 += case.deaths15
            total_avg += case.average_deaths

            diff19= (total20 * 100 / total19) - 100
            diff15 = (total20 * 100 / total15) - 100
            diff_avg = (total20 * 100 / total_avg) - 100

        if (canton.code != 'fl'):
            canton_toadd = {"canton": canton,
                              "all": week_values_deaths,
                              "all_avg": week_values_avg,
                            "all19": week_values_deaths19,
                            "all15": week_values_deaths15,
                            "total20" : total20,
                            "total19":  total19,
                            "total15": total15,
                            "total_avg": total_avg,
                            "diff19": diff19,
                            "diff15": diff15,
                            "diff_avg": diff_avg

                            }
            cantons_values.append(canton_toadd)

    template = loader.get_template('pages/deaths_ch.html')

    context = {
        'cantons': cantons_values,
    }

    return HttpResponse(template.render(context, request))
