from measuremeterdata.models.models import CountryMeasure, CasesDeaths
from django.template import loader
from django.http import HttpResponse
from datetime import date, timedelta
import ast

def measures_noparam(request):
    return measures_ch(request, '1,','1,')


def measures_ch(request, countries, measuretypes):
    print(countries)
    print(measuretypes)
    countries_options = ast.literal_eval(countries)
    measuretypes_options = ast.literal_eval(measuretypes)
    print(ast.literal_eval(countries))
    measures = CountryMeasure.objects.filter(country__in=countries_options, type__in=measuretypes_options, start__gte="2020-02-01").order_by('country', 'start')

    measure_records = []


    for measure in measures:
        print(measure.country)
        print(measure.start)
        print(measure.level)
        print(measure.last_level)

        #Using R
        date_2week_before = measure.start - timedelta(days=14)
        date_1week_before = measure.start - timedelta(days=7)
        date_during = measure.start
        date_1week_later = measure.start + timedelta(days=7)
        date_2week_later = measure.start + timedelta(days=14)

        try:
            data_2week_before = CasesDeaths.objects.get(country=measure.country, date=date_2week_before).r0median
            data_1week_before = CasesDeaths.objects.get(country=measure.country, date=date_1week_before).r0median
            data_during = CasesDeaths.objects.get(country=measure.country, date=date_during).r0median
            data_1week_later = CasesDeaths.objects.get(country=measure.country, date=date_1week_later).r0median
            data_2week_later = CasesDeaths.objects.get(country=measure.country, date=date_2week_later).r0median

            diff_2week_before = (data_1week_before * 100 / data_2week_before) -100
            diff_1week_before = (data_during * 100 / data_1week_before) -100
            diff_during = (data_1week_later * 100 / data_during) - 100
            diff_1week_later = (data_2week_later * 100 / data_1week_later) - 100


            print(data_2week_before)
            print(data_1week_before)
            print(data_during)
            print(data_1week_later)
            print(data_2week_later)

            measure_toadd = {"country": measure.country,
                             "start": measure.start,
                             "level": measure.level,
                             "last_level": measure.last_level,
                             "measure": measure,
                             "date_2week_before": date_2week_before,
                             "date_1week_before": date_1week_before,
                             "date_during": date_during,
                             "date_1week_later": date_1week_later,
                             "date_2week_later": date_2week_later,
                             "data_2week_before": data_2week_before,
                             "data_1week_before": data_1week_before,
                             "data_during": data_during,
                             "data_1week_later": data_1week_later,
                             "data_2week_later": data_2week_later,
                             "diff_2week_before":  diff_2week_before,
                             "diff_1week_before": diff_1week_before,
                             "diff_during": diff_during,
                             "diff_1week_later": diff_1week_later
                            }

            measure_records.append(measure_toadd)
        except:
            pass


        print("......")


    template = loader.get_template('pages/world_measures.html')

    context = {
        'countries':countries,
        'measuretypes':measuretypes,
        'measures': measure_records,
    }

    return HttpResponse(template.render(context, request))
