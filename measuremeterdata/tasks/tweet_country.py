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

    countries = Country.objects.filter(continent=1,isactive=True)
    scores = create_list(countries)

    message = create_messages(scores, 1)
    print("Tweet:")
    print(message)
    send_tweet(message)

    message = create_messages(scores, 2)
    print("Tweet:")
    print(message)
    send_tweet(message)

 #   last_date = create_image(countries)

#    page_access_token = settings.FACEBOOK_ACCESS_TOKEN
#    graph = facebook.GraphAPI(page_access_token)
#    facebook_page_id = settings.FACEBOOK_PAGE_ID
#    graph.put_object(facebook_page_id, "feed", message='test message')


    # #Telegram
    #
    # bot = telepot.Bot(settings.TELEGRAM_TOKEN)
    # print(bot.getMe())
    # bot.sendMessage(settings.TELEGRAM_CHATID, f"Corona-Fälle in den Bezirken von {canton.name}\n\nStand: {last_date}\n\nGanze Rangliste: https://covidlaws.net/ranking7all/")
    # bot.sendPhoto(settings.TELEGRAM_CHATID, photo=open("/tmp/out_image.jpg", 'rb'))
    #
    #

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

def create_list(countries):
    country_vals = []

    for country in countries:

        #skip Noth Korea, it only makes problems
        if country.pk != 11:
            date_tocheck = date.today()
            print(country)

            cases = CasesDeaths.objects.filter(country=country, date__range=[date_tocheck - timedelta(days=60), date_tocheck]).order_by("-date")

            last_date = cases[0].date
            last_prev14 = cases[0].cases_past14days
            last_deaths14 = cases[0].deaths_past14days
            last_tendency = cases[0].development7to7
            last_positivity = None
            last_positivity_date = None
            last_R = None
            last_R_date = None
            positivity_before7 = None
            last_stringency = None
            for case in cases:
                if (case.stringency_index != None and last_stringency == None):
                    last_stringency = case.stringency_index
                    last_stringency_date = case.date

                if (case.r0median != None and last_R == None):
                    last_R = case.r0median
                    last_R_date = case.date

                if (case.positivity != None and last_positivity == None):
                    last_positivity = case.positivity
                    last_positivity_calc = last_positivity
                    last_positivity_date = case.date

            past_date_tocheck = last_date - timedelta(days=14)

            case_14days_7daysago = CasesDeaths.objects.get(country=country, date=last_date - timedelta(days=7))
            case_14days_14daysago = CasesDeaths.objects.get(country=country, date=past_date_tocheck)


            if (last_positivity == None):
                last_positivity_calc = 5

            if positivity_before7 == None:
                positivity_before7 = 5


#            try:
            score = float(cases[0].cases_past14days) + float(cases[0].cases_past7days) + (float(cases[0].development7to7) * float(cases[0].cases_past7days) /100) + (float(last_positivity_calc) * float(cases[0].cases_past7days) / 50) + float((cases[0].deaths_past14days * 20))
            score_7days_before = float(case_14days_7daysago.cases_past14days) + float(case_14days_7daysago.cases_past7days) + (float(case_14days_7daysago.development7to7) * float(case_14days_7daysago.cases_past7days) /100) + (float(positivity_before7) * float(case_14days_7daysago.cases_past7days) / 50) + float((case_14days_7daysago.deaths_past14days * 20))
#            except:
#                print(f"{country} failed...")
#                score = None

            if (score):
                if (score > score_7days_before):
                    arrow = "arrow circle up red"
                elif (score == score_7days_before):
                    arrow = "arrow circle left orange"
                else:
                    arrow = "arrow circle down green"

                peak_cases_ds = CasesDeaths.objects.filter(country=country).order_by("-cases_past14days")
                peak_cases = peak_cases_ds[0].cases_past14days
                peak_cases_date = peak_cases_ds[0].date

                peak_deaths_ds = CasesDeaths.objects.filter(country=country).order_by("-deaths_past14days")
                peak_deaths = peak_deaths_ds[0].deaths_past14days
                peak_deaths_date = peak_deaths_ds[0].date

                positivity_ds = CasesDeaths.objects.filter(country=country).order_by(F('positivity').desc(nulls_last=True))
                peak_positivity = positivity_ds[0].positivity
                peak_positivity_date = positivity_ds[0].date

                canton_toadd = {"name": country.name, "score": int(score), "score_before": int(score_7days_before),
                                "date": last_date, "code": country.code,
                                "cur_prev14": last_prev14, "tendency": last_tendency,
                                "cur_prev7": case_14days_14daysago.cases_past7days,
                                "positivity": last_positivity, "positivity_date":last_positivity_date, "deaths": last_deaths14,
                                "has_measures": country.has_measures, "continent": country.continent.pk, "icon": arrow,
                                "peak_cases": peak_cases, "peak_cases_date": peak_cases_date,
                                "peak_deaths": peak_deaths, "peak_deaths_date": peak_deaths_date,
                                "peak_positivity": peak_positivity, "peak_positivity_date": peak_positivity_date,
                                "R": last_R, "R_date": last_R_date, "stringency": last_stringency, "stringency_date": last_stringency_date
                                }

                country_vals.append(canton_toadd)

    scores = sorted(country_vals, key=lambda i: i['score_before'],reverse=False)
    rank = 1
    for score in scores:
        score["rank_old"] = rank
        rank += 1

    scores = sorted(scores, key=lambda i: i['score'],reverse=False)
    rank = 1
    for score in scores:
        score["rank"] = rank
        score["rank_diff"] = score["rank_old"] - rank
        rank += 1
        if (score["rank"] < score["rank_old"]):
            score["rank_icon"] = "arrow circle up green"
        elif (score["rank"] == score["rank_old"]):
            score["rank_icon"] = "arrow circle left orange"
        else:
            score["rank_icon"] = "arrow circle down red"


    return scores

def create_messages(scores, type):

    if type == 1:
        #Tendency bad
        scores = sorted(scores, key=lambda i: i['tendency'],reverse=True)
        message_twitter = "Euro Stats\nHöchste Zunahme an Fällen im Vergleich zur Vorwoche in %\n\n"
        message_twitter += generate_list(scores, "tendency")

    if type == 2:
        #Tendency good
        scores = sorted(scores, key=lambda i: i['tendency'],reverse=False)
        message_twitter = "Euro Stats\nHöchste Rückgänge an Fällen im Vergleich zur Vorwoche in %\n\n"
        message_twitter += generate_list(scores, "tendency")

    message_twitter += "\n\nKomplette Liste: https://covidlaws.net/ranking_europe"
    return message_twitter


def generate_list(scores, field):
    count = 0

    list = ""

    for score in scores:
        if (count < 7):
            list += str(score[field]) + " " + flag.flag(score["code"]) + " " + score["name"] +"\n"
        count += 1

    return list


def create_image(countries):

    scores = create_list(countries)


    #'#container_2 { -webkit-transform: rotate(90deg); -moz-transform: rotate(90deg); -o-transform: rotate(90deg); -ms-transform: rotate(90deg); transform: rotate(90deg);}' \

    html = f'<html><head><meta charset="UTF-8" /><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.css"/><script src="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.js"></script>' \
           '<style>table, th, td { padding: 10px; font-size: 14; }' \
            '.columnl { float: left; width: 80px; } .columnr { float: left; width: 1000px; }/* Clear floats after the columns */ .row:after {   content: "";   display: table;   clear: both; }' \
            '#rotate-text { width: 45px; transform: rotate(90deg); }' \
            '</style>' \
           f'</head>' \
           '<body style="background-color: #edeeee;"><div style="margin-top: 20px;margin-bottom: 20px;margin-left: 150px;margin-right: 150px;">' \
           '<table>' \
           '<tr style="vertical-align: top;"><td style="vertical-align: top;text-align: right" nowrap>' \
           f'<img src = https://covidlaws.net/static/images/flags_ch/{canton.code}_circle.png><br><br>' \
           f'<div id="rotate-text"><h1>&nbsp;&nbsp;&nbsp;{canton.name}</h1></div>' \
            '</td><td>' \
           '<table class="ui celled table" style="width: 800px;">' \
           '<tr><th>Rang</th>' \
           '<th>Veränderung<br>zur Vorwoche</th>' \
           '<th>Bezirk</th>' \
           '<th>Inzidenz 7T/100k</th>' \
           '<th>Entwicklung<br>Woche/Vorwoche</th>' \
           '</tr>'

    scores = sorted(scores, key=lambda i: i['score'],reverse=False)


    for score in scores:
        html += f'<tr>' \
                f'<td>{score["rank"]}</td>' \
                f'<td><i class ="{score["rank_icon"]} icon" > </i>{score["rank_diff"]}</td>' \
                f'<td><b>{score["name"]}</b></td>' \
                f'<td><div class ="centered"> {score["cur_prev"]}</div></td>'

        if score["tendency"] < 0:
            html += f'<td class="positive"><div class ="centered">{score["tendency"]} %</div></td>' \
                '</tr>'
        else:
            html += f'<td class="negative"><div class ="centered">{score["tendency"]} %</div></td>' \
                '</tr>'


    html += f'</table><b>Stand: {last_date}</b>' \
            "// covidlaws.net // Quelle: @OpenDataZH & der Kanton</td></tr></table>" \
            '</div>' \
            '</body></html>'

    print(html)

    options = {'width': '1200', 'height': '675', 'encoding': "UTF-8", }
    imgkit.from_string(html, "out_image.jpg", options=options)

    return last_date
