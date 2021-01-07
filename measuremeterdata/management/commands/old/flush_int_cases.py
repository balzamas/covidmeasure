from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.models.models import Country, MeasureCategory, MeasureType_old, Measure_old, Continent, CasesDeaths

class Command(BaseCommand):
    def handle(self, *args, **options):

        for x in CasesDeaths.objects.all().iterator(): x.delete()
