from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.tasks.socialmedia.tweet_vacc_speed import tweet

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        tweet()

