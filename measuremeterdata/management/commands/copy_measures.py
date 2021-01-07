from measuremeterdata.models.models import Measure_old, CountryMeasure, CountryMeasureType
from riskcalc.models import BELCases
from django.core.management.base import BaseCommand, CommandError
from datetime import date

def CopyRecords(cat_old, cat_new):
    records = Measure_old.objects.filter(type=cat_old).filter(start__isnull=False).order_by('country','start')

    type = CountryMeasureType.objects.get(pk=cat_new)

    last_level = 0
    old_country = None

    for record in records:
        if record.country != old_country:
            last_level = 0
            old_country = record.country

        if record.comment == "":
            if record.level == 0:
                comment = type.text_level0
            elif record.level == 1:
                comment = type.text_level1
            elif record.level == 2:
                comment = type.text_level2
        else:
            comment = record.comment


        try:
            measure = CountryMeasure.objects.get(country=record.country, type=type, start=record.start)
            measure.level = record.level
            measure.end = record.end
            measure.comment = comment
            measure.last_level = last_level
            measure.save()
        except:
            measure = CountryMeasure(country=record.country, type=type, comment=comment, start=record.start, end=record.end, level=record.level,
                                     last_level=last_level)
            measure.save()

        last_level = record.level



class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('source', type=int)
        parser.add_argument('target', type=int)

    def handle(self, *args, **kwargs):
        #Restaurants: 2
        # Shops 16

        CopyRecords(kwargs['source'],kwargs['target'])

