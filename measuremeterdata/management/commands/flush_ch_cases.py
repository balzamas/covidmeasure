from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.models.models_ch import CHCanton, CHCases


class Command(BaseCommand):
    def handle(self, *args, **options):

        for x in CHCases.objects.all().iterator(): x.delete()
