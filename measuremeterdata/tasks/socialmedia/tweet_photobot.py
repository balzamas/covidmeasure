from measuremeterdata.models.models import Country, CasesDeaths
import os, random
import csv
import datetime
import requests
import pandas as pd
from datetime import date, timedelta, datetime
import tweepy
from django.conf import settings
import imgkit
import facebook
import telepot
from PIL import Image, ImageChops
from django.db.models import F, Func
from mastodon import Mastodon


def tweet():
    img = random.choice(os.listdir("/app/measuremeter/static/images/holiday"))

    Mastodon.create_app(
         'photobotapp',
         api_base_url = 'https://bahn.social',
         to_file = 'pytooter_clientcred.secret'
    )

    mastodon = Mastodon(
        client_id='pytooter_clientcred.secret',
        api_base_url='https://bahn.social'
    )

    mastodon.log_in(
        settings.MASTODON_USER,
        settings.MASTODON_PASSWORD,
        to_file='pytooter_usercred.secret'
    )

    media = mastodon.media_post("/app/measuremeter/static/images/holiday/" + img)
    mastodon.status_post("Where is this? Guess! #quiz #geographyquiz", media_ids=media)

    auth = tweepy.OAuthHandler(settings.TWITTER_PHOTO_API_KEY, settings.TWITTER_PHOTO_SECRET_KEY)
    auth.set_access_token(settings.TWITTER_PHOTO_ACCESS_TOKEN, settings.TWITTER_PHOTO_ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth)

    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")

    message=""

    media = api.media_upload("/app/measuremeter/static/images/holiday/" + img)
    api.update_status(
       status=f"{message}",
       media_ids=[media.media_id_string])

