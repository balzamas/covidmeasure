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


def tweet():
    img = random.choice(os.listdir("/app/measuremeter/static/images/holiday"))

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

