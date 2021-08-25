from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.tasks.socialmedia.tweet_vacc import tweet

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('weekfrom',type=int)
        parser.add_argument('weekto', type=int)
        parser.add_argument('weekvacc',type=int)
        parser.add_argument('geo',type=str)

    def handle(self, *args, **kwargs):
        weekfrom = kwargs['weekfrom']
        weekto = kwargs['weekto']
        weekvacc = kwargs['weekvacc']
        geo = kwargs['geo']
        tweet(weekfrom, weekto, weekvacc, geo)

