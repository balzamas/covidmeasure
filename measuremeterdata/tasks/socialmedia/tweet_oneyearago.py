from measuremeterdata.models.models import Country, CasesDeaths
import os
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
import emoji
import flag

def tweet():

    country = Country.objects.get(pk=1)

    message = create_list(country)

    print("Tweet:")
    print(message)
    send_tweet(message)
    send_telegram(message)

 #   last_date = create_image(countries)

#    page_access_token = settings.FACEBOOK_ACCESS_TOKEN
#    graph = facebook.GraphAPI(page_access_token)
#    facebook_page_id = settings.FACEBOOK_PAGE_ID
#    graph.put_object(facebook_page_id, "feed", message='test message')

def create_messages(scores, type):

    message_twitter = ""

    if type == 1:
        #Tendency bad
        scores = sorted(scores, key=lambda i: i['tendency'],reverse=True)
        message_twitter = "Euro Stats\nHöchste Zunahme Fälle im Vergleich zur Vorwoche in %\n\n"
        gen_message, countries = generate_list(scores, "tendency")
        message_twitter += gen_message

    if type == 2:
        #Tendency good
        scores = sorted(scores, key=lambda i: i['tendency'],reverse=False)
        message_twitter = "Euro Stats\nHöchste Rückgänge Fälle im Vergleich zur Vorwoche in %\n"
        gen_message, countries = generate_list(scores, "tendency")
        message_twitter += gen_message

    if type == 3:
        #deaths bad
        scores = sorted(scores, key=lambda i: i['deaths'],reverse=True)
        message_twitter = emoji.emojize('Euro Stats\nCovid-Tote/100k Einwohner in den verg. 2 Wochen (worst)\n')
        gen_message, countries = generate_list(scores, "deaths")
        message_twitter += gen_message

    if type == 4:
        #Tendency good
        scores = sorted(scores, key=lambda i: i['deaths'],reverse=False)
        message_twitter = emoji.emojize("Euro Stats\nCovid-Tote/100k Einwohner in den verg. 2 Wochen (best)\n")
        gen_message, countries = generate_list(scores, "deaths")
        message_twitter += gen_message

    cntry_list = ""
    for country in countries:
       cntry_list+=str(country)+","

    end_date = datetime.now()
    start_date =  end_date - timedelta(days=62)

    message_twitter += "\n\ncovidlaws.net/ranking_europe\n"
    message_twitter += f"covidlaws.net/compare/{cntry_list}&1,2,5&{start_date.strftime('%Y-%m-%d')}&{end_date.strftime('%Y-%m-%d')}"
    return message_twitter

def send_telegram(message):
    #Telegram

    bot = telepot.Bot(settings.TELEGRAM_TOKEN)
    bot.sendMessage(settings.TELEGRAM_CHATID, message)

def send_tweet(message):
    # #Twitter
    #
    auth = tweepy.OAuthHandler(settings.TWITTER_API_KEY, settings.TWITTER_SECRET_KEY)
    auth.set_access_token(settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth)

    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")

    api.update_status(
       status=message)

def create_list(country):

    date_now = datetime.now().date() - timedelta(days=1)

    numbers_now = CasesDeaths.objects.get(country=country, date=date_now)
    numbers_then = CasesDeaths.objects.get(country=country, date=(date_now - timedelta(days=365)))

    message_twitter = "Schweiz @ " + date_now.strftime('%m/%d') + "\n"
    message_twitter += "Vergleich 21 // 20\n\n"

    message_twitter += "Fälle: " + str(numbers_now.cases_past7days) + " // " + str(numbers_then.cases_past7days) + "\n"
    message_twitter += "Tote: " + str(numbers_now.deaths_past7days) + " // " + str(numbers_then.deaths_past7days) + "\n"
    message_twitter += "Entwicklung: " + str(numbers_now.development7to7) + "% // " + str(numbers_then.development7to7) + "%\n"
    message_twitter += "Tests: " + str(numbers_now.tests_smoothed_per_thousand) + " // " + str(numbers_then.tests_smoothed_per_thousand) + "\n"
    message_twitter += "Pos.-Rate: " + str(numbers_now.positivity) + " // " + str(numbers_then.positivity) + "\n"
    message_twitter += "\nFälle/Tote: Inzidenz 7T/100k\n"
    message_twitter += "Entw.: Woche/Vorwoche\n"
    message_twitter += "Tests: per 1000 Einw.\n"
    message_twitter += "Quellen: JHU, OWD"

    return message_twitter
