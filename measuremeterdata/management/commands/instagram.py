from instabot import Bot
from django.core.management.base import BaseCommand, CommandError
import time

class Command(BaseCommand):
    def handle(self, *args, **options):

        bot = Bot()
        time.sleep(5)
        bot.login(username="fuerst@gmx.li",
                  password="EcMnvtR7p8Uv5zZ")

        print("..........logged in..................")
        # Recommended to put the photo
        # you want to upload in the same
        # directory where this Python code
        # is located else you will have
        # to provide full path for the photo
        bot.upload_photo("output.jpg",
                         caption="Technical Scripter Event 2019")




