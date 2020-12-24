from measuremeterdata.models.models_ch import CHMeasure
from riskcalc.models import BELCases
from django.core.management.base import BaseCommand, CommandError
from datetime import date

class Command(BaseCommand):
    def handle(self, *args, **options):
        for measure in CHMeasure.objects.all():
            if (measure.level > -1):
                    measure.level += 1
                    measure.save()
