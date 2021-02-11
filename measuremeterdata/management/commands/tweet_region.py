from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.tasks.socialmedia.tweet_region import tweet
from measuremeterdata.models.models_ch import CHCases, CHCanton

#Source: https://data.europa.eu/euodp/en/data/dataset/covid-19-coronavirus-data/resource/55e8f966-d5c8-438e-85bc-c7a5a26f4863

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('type',type=int)
    def handle(self, *args, **kwargs):
        type = kwargs['type']
        tweet(type)

