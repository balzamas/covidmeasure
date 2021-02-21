from measuremeterdata.models.models_ch import DoomsdayClock
from django.shortcuts import get_object_or_404, render
from datetime import date, timedelta
from django.template import loader
from django.http import HttpResponse
from django.db.models import F, Func

def load_data(request):
    doom_clock = DoomsdayClock.objects.get(name="Master")
    template = loader.get_template('pages/doomsdayclock.html')

    quota = doom_clock.hosp_cov19_patients * 100 / doom_clock.hosp_capacity

    value = 0

    if doom_clock.positivity < 5:
        value += 1

    if quota < 25:
        value += 1

    if doom_clock.r_okay:
        value += 1

    if doom_clock.incidence_mar1 >= doom_clock.incidence_latest:
        value += 1

    context = {
        'hosp_cov19_patients' : doom_clock.hosp_cov19_patients,
        'hosp_capacity' : doom_clock.hosp_capacity ,
        'hosp_date' : doom_clock.hosp_date,
        'hosp_quota': quota,
        'positivity' : doom_clock.positivity,
        'positivity_date' : doom_clock.positivity_date,
        'r1_value' : doom_clock.r1_value,
        'r1_date' : doom_clock.r1_date,
        'r2_value' : doom_clock.r2_value,
        'r2_date' : doom_clock.r2_date,
        'r3_value' : doom_clock.r3_value,
        'r3_date' : doom_clock.r3_date,
        'r4_value' : doom_clock.r4_value,
        'r4_date' : doom_clock.r4_date,
        'r5_value' : doom_clock.r5_value,
        'r5_date' : doom_clock.r5_date,
        'r_okay' : doom_clock.r_okay,
        'incidence_mar1' : doom_clock.incidence_mar1,
        'incidence_latest' : doom_clock.incidence_latest,
        'incidence_latest_date' : doom_clock.incidence_latest_date,
        "value": value
    }
    return HttpResponse(template.render(context, request))
