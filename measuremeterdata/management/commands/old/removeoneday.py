from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.models.models import Country, MeasureCategory, MeasureType_old, Measure_old, Continent
from datetime import timedelta

#Switch to new level field, migrate data
class Command(BaseCommand):
    def handle(self, *args, **options):
        measures = Measure_old.objects.all()
        for row in measures:
            if (row.end):
                row.end += timedelta(days=-1)
                row.save()

