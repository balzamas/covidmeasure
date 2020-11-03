from measuremeterdata.models.models_ch import CHCanton, CHCases
from django.core.management.base import BaseCommand, CommandError
import datetime
from datetime import date, timedelta

def saveit(bezirk_id, ftdays, date):
    bezirk = CHCanton.objects.get(id=bezirk_id)
    try:
        cd_existing = CHCases.objects.get(canton=bezirk, date=date)
        cd_existing.incidence_past14days = ftdays
        cd_existing.save()
    except CHCases.DoesNotExist:
        cd = CHCases(canton=bezirk, incidence_past14days=ftdays, date=date)
        cd.save()

def get_start_date(year, week):
    d = datetime.date(year, 1, 1)
    if (d.weekday() <= 3):
        d = d - timedelta(d.weekday())
    else:
        d = d + timedelta(7 - d.weekday())
    dlt = timedelta(days=(week - 1) * 7)
    return d + dlt

class Command(BaseCommand):
    def handle(self, *args, **options):
        #TG

        start_be = get_start_date(2020,31)
        for cases in CHCases.objects.filter(canton=52).order_by('date'):
            if (cases.date < start_be):
                print("save")
                saveit(174, cases.incidence_past14days, cases.date)
                saveit(175, cases.incidence_past14days, cases.date)
                saveit(176, cases.incidence_past14days, cases.date)
                saveit(177, cases.incidence_past14days, cases.date)
                saveit(178, cases.incidence_past14days, cases.date)
