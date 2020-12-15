from measuremeterdata.models.models_ch import CHCanton, CHCases
from django.core.management.base import BaseCommand, CommandError
import datetime
from datetime import date, timedelta

def saveit(bezirk_id, ftdays, sdays, date):
    bezirk = CHCanton.objects.get(id=bezirk_id)
    try:
        cd_existing = CHCases.objects.get(canton=bezirk, date=date)
        cd_existing.incidence_past14days = ftdays
        cd_existing.incidence_past7days = sdays
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
        #BE

        start_be = get_start_date(2020,32)
        start_be2 = get_start_date(2020,41)
        start_be3 = get_start_date(2020,46)
        for cases in CHCases.objects.filter(canton=43).order_by('date'):
            if (cases.date < start_be):
                saveit(101, cases.incidence_past14days, cases.incidence_past7days, cases.date)
                saveit(102, cases.incidence_past14days, cases.incidence_past7days,cases.date)
                saveit(103, cases.incidence_past14days, cases.incidence_past7days,cases.date)
                saveit(104, cases.incidence_past14days, cases.incidence_past7days,cases.date)
                saveit(105, cases.incidence_past14days, cases.incidence_past7days,cases.date)
                saveit(106, cases.incidence_past14days, cases.incidence_past7days,cases.date)
                saveit(107, cases.incidence_past14days, cases.incidence_past7days,cases.date)
                saveit(108, cases.incidence_past14days, cases.incidence_past7days,cases.date)
                saveit(109, cases.incidence_past14days, cases.incidence_past7days,cases.date)
                saveit(110, cases.incidence_past14days, cases.incidence_past7days,cases.date)
            if (cases.date < start_be3 and cases.date > start_be2):
                saveit(101, cases.incidence_past14days, cases.incidence_past7days, cases.date)
                saveit(102, cases.incidence_past14days, cases.incidence_past7days,cases.date)
                saveit(103, cases.incidence_past14days, cases.incidence_past7days,cases.date)
                saveit(104, cases.incidence_past14days, cases.incidence_past7days,cases.date)
                saveit(105, cases.incidence_past14days, cases.incidence_past7days,cases.date)
                saveit(106, cases.incidence_past14days, cases.incidence_past7days,cases.date)
                saveit(107, cases.incidence_past14days, cases.incidence_past7days,cases.date)
                saveit(108, cases.incidence_past14days, cases.incidence_past7days,cases.date)
                saveit(109, cases.incidence_past14days, cases.incidence_past7days,cases.date)
                saveit(110, cases.incidence_past14days, cases.incidence_past7days,cases.date)


        #GR
        start_gr = get_start_date(2020,31)
        for cases in CHCases.objects.filter(canton=45).order_by('date'):
            if (cases.date < start_gr):
                saveit(111, cases.incidence_past14days, cases.incidence_past7days,cases.date)
                saveit(112, cases.incidence_past14days, cases.incidence_past7days,cases.date)
                saveit(113, cases.incidence_past14days, cases.incidence_past7days,cases.date)
                saveit(114, cases.incidence_past14days, cases.incidence_past7days,cases.date)
                saveit(115, cases.incidence_past14days, cases.incidence_past7days,cases.date)
                saveit(116, cases.incidence_past14days, cases.incidence_past7days,cases.date)
                saveit(117, cases.incidence_past14days, cases.incidence_past7days,cases.date)
                saveit(118, cases.incidence_past14days, cases.incidence_past7days,cases.date)
                saveit(119, cases.incidence_past14days, cases.incidence_past7days,cases.date)
                saveit(120, cases.incidence_past14days, cases.incidence_past7days,cases.date)
                saveit(121, cases.incidence_past14days, cases.incidence_past7days,cases.date)


        #VS
        start_vs = get_start_date(2020,31)
        for cases in CHCases.objects.filter(canton=49).order_by('date'):
            if (cases.date < start_vs):
                saveit(88, cases.incidence_past14days, cases.incidence_past7days,cases.date)
                saveit(89, cases.incidence_past14days, cases.incidence_past7days,cases.date)
                saveit(90, cases.incidence_past14days, cases.incidence_past7days,cases.date)
                saveit(91, cases.incidence_past14days, cases.incidence_past7days,cases.date)
                saveit(92, cases.incidence_past14days, cases.incidence_past7days,cases.date)
                saveit(93, cases.incidence_past14days, cases.incidence_past7days,cases.date)
                saveit(94, cases.incidence_past14days, cases.incidence_past7days,cases.date)
                saveit(95, cases.incidence_past14days, cases.incidence_past7days,cases.date)
                saveit(96, cases.incidence_past14days, cases.incidence_past7days,cases.date)
                saveit(97, cases.incidence_past14days, cases.incidence_past7days,cases.date)
                saveit(98, cases.incidence_past14days, cases.incidence_past7days,cases.date)
                saveit(99, cases.incidence_past14days, cases.incidence_past7days,cases.date)
                saveit(100, cases.incidence_past14days, cases.incidence_past7days,cases.date)


        #FR
        start_fr = get_start_date(2020,33)
        for cases in CHCases.objects.filter(canton=47).order_by('date'):
            if (cases.date < start_fr):
                saveit(81, cases.incidence_past14days, cases.incidence_past7days,cases.date)
                saveit(82, cases.incidence_past14days, cases.incidence_past7days,cases.date)
                saveit(83, cases.incidence_past14days, cases.incidence_past7days,cases.date)
                saveit(84, cases.incidence_past14days, cases.incidence_past7days,cases.date)
                saveit(85, cases.incidence_past14days, cases.incidence_past7days,cases.date)
                saveit(86, cases.incidence_past14days, cases.incidence_past7days,cases.date)
                saveit(87, cases.incidence_past14days, cases.incidence_past7days,cases.date)
        print(start_fr)


        #SO
        start_so = get_start_date(2020,39)
        for cases in CHCases.objects.filter(canton=40).order_by('date'):
            if (cases.date < start_so):
                saveit(141, cases.incidence_past14days, cases.incidence_past7days,cases.date)
                saveit(142, cases.incidence_past14days, cases.incidence_past7days,cases.date)
                saveit(143, cases.incidence_past14days, cases.incidence_past7days,cases.date)
                saveit(144, cases.incidence_past14days, cases.incidence_past7days,cases.date)
                saveit(145, cases.incidence_past14days, cases.incidence_past7days,cases.date)
                saveit(146, cases.incidence_past14days, cases.incidence_past7days,cases.date)
                saveit(147, cases.incidence_past14days, cases.incidence_past7days,cases.date)
                saveit(148, cases.incidence_past14days, cases.incidence_past7days,cases.date)
                saveit(149, cases.incidence_past14days, cases.incidence_past7days,cases.date)
                saveit(150, cases.incidence_past14days, cases.incidence_past7days,cases.date)


        print(start_fr)
