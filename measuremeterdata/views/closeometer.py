from measuremeterdata.models.models_ch import DoomsdayClock
from django.shortcuts import get_object_or_404, render
from datetime import date, timedelta
from django.template import loader
from django.http import HttpResponse
from django.db.models import F, Func

def load_data(request):
    doom_clock = DoomsdayClock.objects.get(name="Master")
    template = loader.get_template('pages/closeometer.html')

    quota = doom_clock.hosp_cov19_patients * 100 / doom_clock.hosp_capacity

    value = 0

    r_okay = False

    if doom_clock.hosp_average < 80:
        value += 1

    if doom_clock.hosp_cov19_patients < 300:
        value += 1

    if doom_clock.r_average < 1.15:
        value += 1
        r_okay = True

    if 350 > doom_clock.incidence_latest:
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
        'r6_value': doom_clock.r6_value,
        'r6_date': doom_clock.r6_date,
        'r7_value': doom_clock.r7_value,
        'r7_date': doom_clock.r7_date,
        'r_average': doom_clock.r_average,
        'r_okay' : r_okay,
        'hosp1_value': doom_clock.hosp1_value,
        'hosp1_date': doom_clock.hosp1_date,
        'hosp2_value': doom_clock.hosp2_value,
        'hosp2_date': doom_clock.hosp2_date,
        'hosp3_value': doom_clock.hosp3_value,
        'hosp3_date': doom_clock.hosp3_date,
        'hosp4_value': doom_clock.hosp4_value,
        'hosp4_date': doom_clock.hosp4_date,
        'hosp5_value': doom_clock.hosp5_value,
        'hosp5_date': doom_clock.hosp5_date,
        'hosp6_value': doom_clock.hosp6_value,
        'hosp6_date': doom_clock.hosp6_date,
        'hosp7_value': doom_clock.hosp7_value,
        'hosp7_date': doom_clock.hosp7_date,
        'hosp_average': doom_clock.hosp_average,
        'incidence_mar1' : doom_clock.incidence_mar1,
        'incidence_latest' : doom_clock.incidence_latest,
        'incidence_latest_date' : doom_clock.incidence_latest_date,
        "value": value
    }
    return HttpResponse(template.render(context, request))
