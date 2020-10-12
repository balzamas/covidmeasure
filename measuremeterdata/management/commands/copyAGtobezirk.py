from measuremeterdata.models import Country, MeasureCategory, MeasureType, Measure, Continent, CasesDeaths, CHCanton, CHCases
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
        #AG

        start_be = get_start_date(2020,41)
        for cases in CHCases.objects.filter(canton=41).order_by('date'):
            if (cases.date < start_be):
                saveit(1901, cases.incidence_past14days, cases.date)
                saveit(1902, cases.incidence_past14days, cases.date)
                saveit(1903, cases.incidence_past14days, cases.date)
                saveit(1904, cases.incidence_past14days, cases.date)
                saveit(1905, cases.incidence_past14days, cases.date)
                saveit(1906, cases.incidence_past14days, cases.date)
                saveit(1907, cases.incidence_past14days, cases.date)
                saveit(1908, cases.incidence_past14days, cases.date)
                saveit(1909, cases.incidence_past14days, cases.date)
                saveit(1910, cases.incidence_past14days, cases.date)
                saveit(1911, cases.incidence_past14days, cases.date)


