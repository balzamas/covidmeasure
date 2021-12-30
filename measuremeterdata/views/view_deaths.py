from measuremeterdata.models.models import Country, MeasureType_old, MeasureCategory, CasesDeaths
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
        startdate = datetime.date(2019, 12, 30)

        cases = CasesDeaths.objects.filter(country=country, date__gte=startdate).order_by("date")

        week_values_coviddeaths20 = {}
        week_values_alldeaths = {}
        week_values_alldeaths_peak = {}
        week_values_avg_and_covid = {}
        week_values_avg = {}

        week = 1
        weekday = 1
        week_value_covid = 0
        week_value_all = 0
        week_value_peak_all = None

        death_peak_week2 = None

        death_total_week2 = 0
        death_total_week12 = 0

        death_covid_week2 = 0
        death_covid_week8 = 0

        weeks_wdata = 0

        now20_11_32 = 0
        now20_33_53 = 0
        now21_1_25 = 0
        now21_rest = 0
        avg20_11_32 = 0
        avg20_33_53 = 0
        avg21_1_25 = 0
        avg21_rest = 0

        last_week = 46
        last_week_def = 0


        for case in cases:
            week_value_covid += case.deaths
            if case.deathstotal:
                week_value_all += case.deathstotal
                death_covid_week2 += case.deaths
                death_total_week2 += case.deathstotal
                if case.deathstotal_peak:
                    if (death_peak_week2 == None):
                        death_peak_week2 = 0
                    death_peak_week2 += case.deathstotal_peak

                weeks_wdata = week
                if week > 7:
                    death_covid_week8 += case.deaths
                    death_total_week12 += case.deathstotal

            if case.deathstotal_peak:
                if week_value_peak_all == None:
                    week_value_peak_all = 0
                week_value_peak_all += case.deathstotal_peak

            weekday += 1
            if weekday == 8:
                if week_value_all > -1:
                    week_values_alldeaths[week] = int(week_value_all)
                if week_value_peak_all:
                    week_values_alldeaths_peak[week] = int(week_value_peak_all)
                week_values_coviddeaths20[week] = week_value_covid
                if case.deathstotal_average:
                    week_values_avg[week] = int(case.deathstotal_average * 7)
                    week_values_avg_and_covid[week] = int((case.deathstotal_average * 7) + week_value_covid)
                else:
                    week_values_avg[week] = int(country.average_death_per_day * 7)
                    week_values_avg_and_covid[week] = int((country.average_death_per_day * 7) + week_value_covid)

                if week_value_all > -1 and case.date.year == 2020 and case.date.isocalendar()[1] > 10 and case.date.isocalendar()[1] < 33:
                    now20_11_32 += week_values_alldeaths[week]
                    avg20_11_32 += week_values_avg[week]
                elif week_value_all > -1 and case.date.year == 2020 and case.date.isocalendar()[1] > 32:
                    now20_33_53 += week_values_alldeaths[week]
                    avg20_33_53 += week_values_avg[week]
                elif week_value_all > -1 and case.date.year == 2021 and case.date.isocalendar()[1] < 26:
                    now21_1_25 += week_values_alldeaths[week]
                    avg21_1_25 += week_values_avg[week]
                elif week_value_all > -1 and case.date.year == 2021 and case.date.isocalendar()[1] > 25:
                    now21_rest += week_values_alldeaths[week]
                    avg21_rest += week_values_avg[week]
                    last_week_def = case.date.isocalendar()[1]


                weekday = 1
                week_value_covid = 0
                week_value_all = -1
                week_value_peak_all = 0
                week += 1

            diff_week2_peak = None
            if case.deathstotal_average:
                diff_week2 = int(death_total_week2 - ((weeks_wdata - 1) * 7 * case.deathstotal_average))
                if death_peak_week2:
                    diff_week2_peak = int(death_total_week2 - death_peak_week2)
                diff_week12 = int(death_total_week12 - ((weeks_wdata - 11) * 7 * case.deathstotal_average))
            else:
                diff_week2 = int(death_total_week2 - ((weeks_wdata - 1) * 7 * country.average_death_per_day))
                if death_peak_week2:
                    diff_week2_peak = int(death_total_week2 - death_peak_week2)
                diff_week12 = int(death_total_week12 - ((weeks_wdata - 11) * 7 * country.average_death_per_day))

        all_num = now20_11_32 + now20_33_53 + now21_1_25 + now21_rest
        all_avg = avg20_11_32 + avg20_33_53 + avg21_1_25 + avg21_rest

        percent_peak = None
        if (death_peak_week2):
            percent_peak = (100 * diff_week2_peak / death_peak_week2)

        if last_week_def < last_week:
            last_week = None

        countr_toadd = {"country": country,
                          "covid20": week_values_coviddeaths20,
                          "all": week_values_alldeaths,
                          "all_peak": week_values_alldeaths_peak,
                          "avg_and_covid": week_values_avg_and_covid,
                           "week_values_avg": week_values_avg,
                        "now20_11_32": now20_11_32,
                        "now20_33_53": now20_33_53,
                        "now21_1_25": now21_1_25,
                        "avg20_11_32": avg20_11_32,
                        "avg20_33_53": avg20_33_53,
                        "avg21_1_25": avg21_1_25,
                        "all_num": all_num,
                        "all_avg": all_avg,
                        "last_week": last_week
                        }
        countries_values.append(countr_toadd)

    template = loader.get_template('pages/deaths.html')

    context = {
        'countries': countries_values,
    }

    return HttpResponse(template.render(context, request))
