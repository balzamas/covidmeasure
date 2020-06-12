from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.models import Country, MeasureCategory, MeasureType, Measure, Continent
from datetime import timedelta

#Switch to new level field, migrate data
class Command(BaseCommand):
    def handle(self, *args, **options):
        measures = Measure.objects.all()
        for row in measures:
            if (row.end):
                row.end += timedelta(days=-1)
                row.save()

