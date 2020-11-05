from measuremeterdata.models.models import Measure, Country, MeasureType, MeasureCategory, CasesDeaths
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
        print(country)
        #startdate = datetime.date(2020, 2, 17)
        startdate = datetime.date(2020, 1, 6)

        cases = CasesDeaths.objects.filter(country=country, date__gte=startdate).order_by("date")

        week_values_coviddeaths = {}
        week_values_alldeaths = {}
        week_values_alldeaths_peak = {}

        #week = 8
        week = 2
        weekday = 1
        week_value_covid = 0
        week_value_all = 0
        week_value_peak_all = None

        death_peak_week2 = None

        death_total_week2 = 0
        death_total_week8 = 0

        death_covid_week2 = 0
        death_covid_week8 = 0

        weeks_wdata = 0

        week_stop = datetime.datetime.now().isocalendar()[1] -2

        for case in cases:
            week_value_covid += case.deaths
            if case.deathstotal:
                week_value_all += case.deathstotal
                if week < week_stop:
                    death_covid_week2 += case.deaths
                    death_total_week2 += case.deathstotal
                    if case.deathstotal_peak:
                        if (death_peak_week2 == None):
                            death_peak_week2 = 0
                        death_peak_week2 += case.deathstotal_peak

                    weeks_wdata = week
                    if week > 7:
                        death_covid_week8 += case.deaths
                        death_total_week8 += case.deathstotal

            if case.deathstotal_peak:
                if week_value_peak_all == None:
                    week_value_peak_all = 0
                week_value_peak_all += case.deathstotal_peak

            weekday += 1
            if weekday == 8:
                print(case.date)
                print(week)
                print(week_value_all)
                if week_value_all > -1:
                    week_values_alldeaths[week] = int(week_value_all)
                if week_value_peak_all:
                    week_values_alldeaths_peak[week] = int(week_value_peak_all)
                week_values_coviddeaths[week] = week_value_covid
                weekday = 1
                week_value_covid = 0
                week_value_all = -1
                week_value_peak_all = 0
                week += 1

            diff_week2 = int(death_total_week2 - ((weeks_wdata - 1) * 7 * country.average_death_per_day))
            if death_peak_week2:
                diff_week2_peak = int(death_total_week2 - death_peak_week2)
            diff_week8 = int(death_total_week8 - ((weeks_wdata - 7) * 7 * country.average_death_per_day))

        print(country)
        print(week_values_alldeaths)
        print(week_values_alldeaths_peak)

        percent_peak = None
        if (death_peak_week2):
            percent_peak = (100 * diff_week2_peak / death_peak_week2)

        countr_toadd = {"country": country,
                          "covid": week_values_coviddeaths,
                          "all": week_values_alldeaths,
                          "all_peak": week_values_alldeaths_peak,

                        "death_covid_week2": int(death_covid_week2),
                        "death_total_week2" : int(death_total_week2),
                        "death_peak_week2" : death_peak_week2,
                        "death_covid_week8": int(death_covid_week8),
                        "death_total_week8": int(death_total_week8),
                        "diff_peak": diff_week2_peak,
                        "diff_week2": diff_week2,
                        "diff_week8": diff_week8,
                        "percent_week2": (100 * diff_week2 / death_total_week2),
                        "percent_peak": percent_peak,
                        "percent_week8": (100 * diff_week8 / death_total_week8),
                        "weeks_wdata" : weeks_wdata
                       }
        countries_values.append(countr_toadd)

    template = loader.get_template('pages/deaths.html')

    context = {
        'countries': countries_values,
    }

    return HttpResponse(template.render(context, request))
