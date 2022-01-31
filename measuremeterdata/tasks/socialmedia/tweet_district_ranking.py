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
from measuremeterdata.models.models_ch import CHCases, CHCanton


def tweet(canton):

    districts = CHCanton.objects.filter(level=1, code=canton.code)
    last_date = create_image(districts, canton)

#    page_access_token = settings.FACEBOOK_ACCESS_TOKEN
#    graph = facebook.GraphAPI(page_access_token)
#    facebook_page_id = settings.FACEBOOK_PAGE_ID
#    graph.put_object(facebook_page_id, "feed", message='test message')

    send_telegram(canton, last_date)
    send_tweet(canton, last_date)

def send_telegram(canton, last_date):
    #Telegram

    bot = telepot.Bot(settings.TELEGRAM_TOKEN)
    print(bot.getMe())
    bot.sendMessage(settings.TELEGRAM_CHATID, f"Corona-Fälle in den Bezirken von {canton.name}\n\nStand: {last_date}\n\nGanze Rangliste: https://covidlaws.net/ranking7all/\nKartenansicht: https://covidlaws.net/districts7/")
    bot.sendPhoto(settings.TELEGRAM_CHATID, photo=open("/tmp/out_image.jpg", 'rb'))



def send_tweet(canton, last_date):
    #Twitter

    auth = tweepy.OAuthHandler(settings.TWITTER_API_KEY, settings.TWITTER_SECRET_KEY)
    auth.set_access_token(settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth)

    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")

    media = api.media_upload("/tmp/out_image.jpg")
    api.update_status(
       status=f"Corona-Fälle in den Bezirken von {canton.name}\n\nStand: {last_date}\n\n#CoronaInfoCH\n\nGanze Rangliste: https://covidlaws.net/ranking7all/\nKartenansicht: https://covidlaws.net/districts7/",
       media_ids=[media.media_id_string])


def create_image(districts, canton):
    canton_vals = []

    #'#container_2 { -webkit-transform: rotate(90deg); -moz-transform: rotate(90deg); -o-transform: rotate(90deg); -ms-transform: rotate(90deg); transform: rotate(90deg);}' \

    cases_canton = CHCases.objects.filter(canton=canton,
                                   date__range=[date.today() - timedelta(days=25), date.today()]).order_by(
        "-date")

    html = f'<html><head><meta charset="UTF-8" /><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.css"/><script src="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.js"></script>' \
           '<style>table, th, td { padding: 10px; font-size: 14; }' \
            '.columnl { float: left; width: 80px; } .columnr { float: left; width: 1000px; }/* Clear floats after the columns */ .row:after {   content: "";   display: table;   clear: both; }' \
            '#rotate-text { width: 45px; transform: rotate(90deg); }' \
            '.table td, .table th {'\
                'font-size: 25px;'\
            '}'\
            '</style>' \
           f'</head>' \
           '<body style="background-color: #edeeee;"><div style="margin-top: 20px;margin-bottom: 20px;">' \
           '<table style="margin-left: auto;margin-right: auto;">' \
           '<tr style="vertical-align: top;"><td style="vertical-align: top;text-align: right" nowrap>' \
           f'<img src = https://covidlaws.net/static/images/flags_ch/{canton.code}_circle.png><br><br>' \
           f'<div id="rotate-text"><h1>&nbsp;&nbsp;&nbsp;{canton.name} // Inzidenz: {cases_canton[0].incidence_past7days} ({cases_canton[0].date}) </h1></div>' \
            '</td><td>' \
           '<table class="ui celled table" style="width: 950px;table-layout:fixed">' \
            '<colgroup>' \
            '<col style="width: 30px;">' \
            '<col style="width: 150px">' \
            '<col style="width: 45px">' \
            '<col style="width: 65px">' \
            '</colgroup>' \
           '<tr><th>Rang</th>' \
           '<th>Bezirk</th>' \
           '<th>Inzidenz 7T/100k</th>' \
           '<th>Entwicklung<br>Woche/Vorwoche</th>' \
           '</tr>'

    for district in districts:
        date_tocheck = date.today()

        cases = CHCases.objects.filter(canton=district,
                                       date__range=[date_tocheck - timedelta(days=25), date_tocheck]).order_by(
            "-date")

        last_date = cases[0].date
        last_prev7 = cases[0].incidence_past7days
        last_prev14 = cases[0].incidence_past14days
        last_tendency = cases[0].development7to7

        past_date_tocheck = last_date - timedelta(days=7)

        cur_prev = last_prev7

        canton_toadd = {"name": district.name,
                        "date": last_date, "code": district.code, "level": district.level,
                        "cur_prev": cur_prev, "cur_prev14": last_prev14, "tendency": last_tendency,
                        "id": district.swisstopo_id,
                        "level": district.level}
        canton_vals.append(canton_toadd)



    scores = sorted(canton_vals, key=lambda i: i['cur_prev'], reverse=False)
    rank = 1
    for score in scores:
        score["rank"] = rank
        rank += 1

        html += f'<tr>' \
                f'<td>{score["rank"]}</td>' \
                f'<td><b>{score["name"]}</b></td>' \
                f'<td><div class ="centered"> {score["cur_prev"]}</div></td>'

        if score["tendency"] and score["tendency"] < 0:
            html += f'<td class="positive"><div class ="centered">{score["tendency"]} %</div></td>' \
                '</tr>'
        else:
            html += f'<td class="negative"><div class ="centered">{score["tendency"]} %</div></td>' \
                '</tr>'


    html += f'</table><div style="font-size:30px"><b>Stand: {last_date}</b>' \
            "// covidlaws.net // Quelle: @OpenDataZH & der Kanton</div></td></tr></table>" \
            '</div>' \
            '</body></html>'

    print(html)

    options = {'width': '1200', 'height': '1200', 'encoding': "UTF-8", }
    imgkit.from_string(html, "/tmp/out_image.jpg", options=options)

    return last_date
