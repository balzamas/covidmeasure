from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.tasks.socialmedia.tweet_vacc2 import tweet

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('year',type=int)
        parser.add_argument('week',type=int)
        parser.add_argument('geo',type=str)

    def handle(self, *args, **kwargs):
        year = kwargs['year']
        week = kwargs['week']
        geo = kwargs['geo']
        tweet(year, week, geo)

