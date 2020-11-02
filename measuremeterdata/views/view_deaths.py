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
        #startdate = datetime.date(2020, 2, 17)
        startdate = datetime.date(2020, 1, 6)

        cases = CasesDeaths.objects.filter(country=country, date__gte=startdate).order_by("date")

        week_values_coviddeaths = {}
        week_values_alldeaths = {}


        #week = 8
        week = 2
        weekday = 1
        week_value_covid = 0
        week_value_all = 0

        death_total_week2 = 0
        death_total_week8 = 0

        death_covid_week2 = 0
        death_covid_week8 = 0

        weeks_wdata = 0

        week_stop = datetime.datetime.now().isocalendar()[1] -3

        for case in cases:
            if weekday == 8:
                week_values_alldeaths[week] = week_value_all
                week_values_coviddeaths[week] = week_value_covid
                weekday = 1
                week_value_covid = 0
                week_value_all = 0
                week += 1

            week_value_covid += case.deaths
            if case.deathstotal and week < week_stop:
                week_value_all += case.deathstotal
                death_covid_week2 += case.deaths
                death_total_week2 += case.deathstotal
                weeks_wdata = week
                if week > 7:
                    death_covid_week8 += case.deaths
                    death_total_week8 += case.deathstotal
            weekday += 1

            diff_week2 = int(death_total_week2 - ((weeks_wdata - 1) * 7 * country.average_death_per_day))
            diff_week8 = int(death_total_week8 - ((weeks_wdata - 7) * 7 * country.average_death_per_day))

        countr_toadd = {"country": country,
                          "covid": week_values_coviddeaths,
                          "all": week_values_alldeaths,

                        "death_covid_week2": death_covid_week2,
                        "death_total_week2" : death_total_week2,
                        "death_covid_week8": death_covid_week8,
                        "death_total_week8": death_total_week8,
                        "diff_week2": diff_week2,
                        "diff_week8": diff_week8,
                        "percent_week2": (100 * diff_week2 / death_total_week2),
                        "percent_week8": (100 * diff_week8 / death_total_week8),
                        "weeks_wdata" : weeks_wdata
                       }
        countries_values.append(countr_toadd)

    template = loader.get_template('pages/deaths.html')

    context = {
        'countries': countries_values,
    }

    return HttpResponse(template.render(context, request))
