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
    send_telegram()

def send_telegram():
    #Telegram

    img = random.choice(os.listdir("/app/measuremeter/static/images/love"))

    bot = telepot.Bot(settings.TELEGRAM_TOKEN_LOVE)
    print(bot.getMe())
    #bot.sendMessage(settings.TELEGRAM_CHATID_LOVE, f"Hoi du")
    bot.sendPhoto(settings.TELEGRAM_CHATID_LOVE, photo=open("/app/measuremeter/static/images/love/" + img, 'rb'))

