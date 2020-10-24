from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.models import Country, MeasureCategory, MeasureType, Measure, Continent, CasesDeaths, CHCanton, CHCases


class Command(BaseCommand):
    def handle(self, *args, **options):

        for x in CasesDeaths.objects.all().iterator(): x.delete()
