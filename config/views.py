from measuremeterdata.models import Measure, Country, MeasureType, MeasureCategory, CHCases, CHCanton
from django.shortcuts import get_object_or_404, render
from datetime import date, timedelta
from django.template import loader
from django.http import HttpResponse

def render_country(request, country_name):
    item = get_object_or_404(Country, code=country_name)
    return render(request, 'pages/country.html', {'item': item })

def render_euromap(request, measure_id):
    item = get_object_or_404(MeasureType, pk=measure_id)
    return render(request, 'pages/euromap.html', {'item': item })

def render_timeline(request, country_name):
    return render(request, 'pages/timeline.html', {'items': country_name })

def render_compare(request, country_name):
    return render(request, 'pages/compare.html', {'items': country_name })

def ranking(request):

    cantons = CHCanton.objects.filter(level=0)
    canton_vals = []

    for canton in cantons:
        date_tocheck = date.today()

        cases = CHCases.objects.filter(canton=canton, date__range=[date_tocheck - timedelta(days=10), date_tocheck]).order_by("-date")

        last_date = cases[0].date
        last_prev = cases[0].cases_past7days
        past_date_tocheck = last_date - timedelta(days=7)

        case_7days_before = CHCases.objects.get(canton=canton, date=past_date_tocheck)

        if (case_7days_before.cases_past7days > 0):
            tendency = ((cases[0].cases_past7days * 100 / case_7days_before.cases_past7days) - 100)
        else:
            tendency = ((cases[0].cases_past7days * 100 / 1) - 100)

        score = 0 - cases[0].cases_past7days - (tendency / 10)

        canton_toadd = {"name": canton.name, "score": int(score), "date": last_date, "cur_prev": last_prev,
                        "tendency": int(tendency)}
        canton_vals.append(canton_toadd)

    scores = sorted(canton_vals, key=lambda i: i['score'],reverse=True)

    template = loader.get_template('pages/ranking.html')
    context = {
        'cantons': scores,
    }
    return HttpResponse(template.render(context, request))
