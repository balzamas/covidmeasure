from measuremeterdata.models.models_bel import BELProvince, BELCases, BELAgeGroups
from django.shortcuts import get_object_or_404, render
from datetime import date, timedelta
from django.template import loader
from django.http import HttpResponse
from django.db.models import F, Func

def hallo_welt(request):
    datum = date.today()
    if datum.weekday() > 4:
        hans = "it's weekend!"
    else:
        hans = "oh, no!"

    template = loader.get_template('pages/madlaina.html')
    context = {
        'hans': hans,
        "datum": datum
    }
    return HttpResponse(template.render(context, request))
