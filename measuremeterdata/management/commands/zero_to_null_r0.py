from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.models.models import Country, MeasureCategory, MeasureType, Measure, Continent, CasesDeaths

class Command(BaseCommand):
    def handle(self, *args, **options):

        for x in CasesDeaths.objects.all():
            if (x.r0peak == 0):
                x.r0peak = None

            if (x.r0low == 0):
                x.r0low = None

            if (x.r0median == 0):
                x.r0median = None

            x.save()
