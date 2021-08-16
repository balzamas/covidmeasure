from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.tasks.socialmedia.tweet_vacc import tweet

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('week',type=int)
    def handle(self, *args, **kwargs):
        week = kwargs['week']
        tweet(week)

