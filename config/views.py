from measuremeterdata.models.models import Country, MeasureCategory,CasesDeaths
from measuremeterdata.models.models_ch import CHCases, CHCanton, CHMeasure
from measuremeterdata.models.models_bel import BELProvince, BELCases, BELAgeGroups

from django.shortcuts import get_object_or_404, render
from datetime import date, timedelta
from django.template import loader
from django.http import HttpResponse
from django.db.models import F, Func

def render_country(request, country_name):
    item = get_object_or_404(Country, code=country_name)
    return render(request, 'pages/country.html', {'item': item })

def render_euromap(request, measure_id):
    item = get_object_or_404(CountryMeasureType, pk=measure_id)
    return render(request, 'pages/euromap.html', {'item': item })

def render_timeline(request, country_name):
    return render(request, 'pages/timeline.html', {'items': country_name })

def render_compare(request, country_name):
    return render(request, 'pages/compare.html', {'items': country_name })

def render_cantons(request, options):
    return render(request, 'pages/canton.html', {'items': options })

def international(request):
    measures = CountryMeasure.objects.all().order_by('-created')[:10]

    template = loader.get_template('pages/home.html')
    context = {
        'measures': measures,
    }
    return HttpResponse(template.render(context, request))

