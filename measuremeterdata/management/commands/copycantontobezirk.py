from measuremeterdata.models import Country, MeasureCategory, MeasureType, Measure, Continent, CasesDeaths, CHCanton, CHCases
from django.core.management.base import BaseCommand, CommandError

def saveit(bezirk_id, ftdays, date):
    bezirk = CHCanton.objects.get(id=bezirk_id)
    try:
        cd_existing = CHCases.objects.get(canton=bezirk, date=date)
        cd_existing.cases_past14days = ftdays
        cd_existing.save()
    except CHCases.DoesNotExist:
        cd = CHCases(canton=bezirk, cases_past14days=ftdays, date=date)
        cd.save()


class Command(BaseCommand):
    def handle(self, *args, **options):
        #BE
        for cases in CHCases.objects.filter(canton=43).order_by('date'):
            saveit(101, cases.cases_past14days, cases.date)
            saveit(102, cases.cases_past14days, cases.date)
            saveit(103, cases.cases_past14days, cases.date)
            saveit(104, cases.cases_past14days, cases.date)
            saveit(105, cases.cases_past14days, cases.date)
            saveit(106, cases.cases_past14days, cases.date)
            saveit(107, cases.cases_past14days, cases.date)
            saveit(108, cases.cases_past14days, cases.date)
            saveit(109, cases.cases_past14days, cases.date)
            saveit(110, cases.cases_past14days, cases.date)


        #GR
        for cases in CHCases.objects.filter(canton=45).order_by('date'):
            saveit(111, cases.cases_past14days, cases.date)
            saveit(112, cases.cases_past14days, cases.date)
            saveit(113, cases.cases_past14days, cases.date)
            saveit(114, cases.cases_past14days, cases.date)
            saveit(115, cases.cases_past14days, cases.date)
            saveit(116, cases.cases_past14days, cases.date)
            saveit(117, cases.cases_past14days, cases.date)
            saveit(118, cases.cases_past14days, cases.date)
            saveit(119, cases.cases_past14days, cases.date)
            saveit(120, cases.cases_past14days, cases.date)
            saveit(121, cases.cases_past14days, cases.date)


        #VS
        for cases in CHCases.objects.filter(canton=49).order_by('date'):
            saveit(88, cases.cases_past14days, cases.date)
            saveit(89, cases.cases_past14days, cases.date)
            saveit(90, cases.cases_past14days, cases.date)
            saveit(91, cases.cases_past14days, cases.date)
            saveit(92, cases.cases_past14days, cases.date)
            saveit(93, cases.cases_past14days, cases.date)
            saveit(94, cases.cases_past14days, cases.date)
            saveit(95, cases.cases_past14days, cases.date)
            saveit(96, cases.cases_past14days, cases.date)
            saveit(97, cases.cases_past14days, cases.date)
            saveit(98, cases.cases_past14days, cases.date)
            saveit(99, cases.cases_past14days, cases.date)
            saveit(100, cases.cases_past14days, cases.date)


        #FR
        for cases in CHCases.objects.filter(canton=47).order_by('date'):
            saveit(81, cases.cases_past14days, cases.date)
            saveit(82, cases.cases_past14days, cases.date)
            saveit(83, cases.cases_past14days, cases.date)
            saveit(84, cases.cases_past14days, cases.date)
            saveit(85, cases.cases_past14days, cases.date)
            saveit(86, cases.cases_past14days, cases.date)
            saveit(87, cases.cases_past14days, cases.date)

