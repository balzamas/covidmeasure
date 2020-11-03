from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.models.models import Country, MeasureCategory, MeasureType, Measure, Continent

#Switch to new level field, migrate data
class Command(BaseCommand):
    def handle(self, *args, **options):
        for each in  Measure.objects.all():
            if each.partial is True:
                each.level = 1

            if each.partial is False and each.none is False:
                each.level = 2

            each.save()

