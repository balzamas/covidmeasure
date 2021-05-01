from measuremeterdata.models.models_ch import CHCases, CHCanton
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

def tweet():

    cantons = CHCanton.objects.filter(level=0)
    last_date = create_image(cantons)

#    page_access_token = settings.FACEBOOK_ACCESS_TOKEN
#    graph = facebook.GraphAPI(page_access_token)
#    facebook_page_id = settings.FACEBOOK_PAGE_ID
#    graph.put_object(facebook_page_id, "feed", message='test message')

    send_telegram(last_date)
    send_tweet(last_date)

def send_telegram(last_date):
    #Telegram

    bot = telepot.Bot(settings.TELEGRAM_TOKEN)
    print(bot.getMe())
    bot.sendMessage(settings.TELEGRAM_CHATID, f"Impfgeschwindigkeit in den Kantonen\n\nStand: {last_date}\n\nDetails: https://covidlaws.net/ranking7/")
    bot.sendPhoto(settings.TELEGRAM_CHATID, photo=open("/tmp/out_image.jpg", 'rb'))



def send_tweet(last_date):
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
       status=f"Impfgeschwindigkeit in den Kantonen\n\nStand: {last_date}\n\n#CoronaInfoCH\n\nDetails: https://covidlaws.net/ranking7/",
       media_ids=[media.media_id_string])


def create_image(cantons):
    canton_vals = []

    #ch_incidences = CasesDeaths.objects.filter(country=1, date__range=[date.today() - timedelta(days=5), date.today()]).order_by("-date")
    #ch_incidence = ch_incidences[0].cases_past7days

    vacc_date = None

    for canton in cantons:
        date_tocheck = date.today()

        cases = CHCases.objects.filter(canton=canton, date__range=[date_tocheck - timedelta(days=25), date_tocheck]).order_by("-date")
        vacc = None
        vacc_goal = None
        for case in cases:
                if case.vacc_perpop_7d and not vacc:
                    vacc = case.vacc_perpop_7d
                    vacc_date = case.date


                    to_vacc = ((canton.population /100*60) * 2 - case.vacc_total) - (canton.population / 100 * 6.5)

                    days = date(2021, 7, 31) - case.date

                    vacc_goal_raw =  to_vacc / days.days * 7

                    vacc_goal = 100000 * vacc_goal_raw / canton.population




        canton_toadd = {"name": canton.name,
                         "code": canton.code,
                        "code_up": canton.code.upper(),
                        "id": canton.swisstopo_id,
                        "vacc": int(vacc), "vacc_goal":int(vacc_goal), "vacc_date": vacc_date}

        canton_vals.append(canton_toadd)

    canton_vals_sorted = sorted(canton_vals, key=lambda i: i['vacc'], reverse=True)







    canton_vals = []

    #'#container_2 { -webkit-transform: rotate(90deg); -moz-transform: rotate(90deg); -o-transform: rotate(90deg); -ms-transform: rotate(90deg); transform: rotate(90deg);}' \

    html = f'<html><head><meta charset="UTF-8" /><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.css"/><script src="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.js"></script>' \
           '<style>table, th, td { padding: 10px; font-size: 14; }' \
            '.columnl { float: left; width: 80px; } .columnr { float: left; width: 1000px; }/* Clear floats after the columns */ .row:after {   content: "";   display: table;   clear: both; }' \
            '#rotate-text { width: 45px; transform: rotate(90deg); }' \
            '</style>' \
           f'</head>' \
           '<body style="background-color: #edeeee;"><div style="margin-top: 20px;margin-bottom: 20px;">' \
           '<table style="margin-left: auto;margin-right: auto;">' \
           '<tr style="vertical-align: top;"><td style="vertical-align: top;text-align: right" nowrap>' \
           f'<div id="rotate-text"><h1>&nbsp;&nbsp;&nbsp;Impfgeschwindigkeit</h1></div>' \
            '</td><td>' \
           '<table class="ui celled table" style="width: 300px;table-layout:fixed">' \
            '<colgroup>' \
            '<col style="width: 30px;">' \
            '<col style="width: 30px">' \
            '<col style="width: 30px">' \
            '<col style="width: 30px">' \
            '</colgroup>' \
           '<tr><th></th>' \
           '<th></th>' \
           '<th>Ist</th>' \
           '<th>Soll</th>' \
           '</tr>'

    count = 0
    for canton in canton_vals_sorted:

        html += f'<tr>' \
                f'<td><img src = https://covidlaws.net/static/images/flags_ch/{canton["code"]}_circle.png width="25" height="25"></td>' \
                f'<td>{canton["code_up"]}</td>' \

        if canton["vacc_goal"] < canton["vacc"]:
            html += f'<td class="positive"><div class ="centered">{canton["vacc"]}</div></td>'
        else:
            html += f'<td class="negative"><div class ="centered">{canton["vacc"]}</div></td>'

        html += f'<td>{canton["vacc_goal"]}</td></tr>'

        count += 1
        if count == 9 or count == 18:
            html += "</table></td><td>&nbsp;</td><td>"
            html += '<table class="ui celled table" style="width: 300px;table-layout:fixed">' \
            '<colgroup>' \
            '<col style="width: 30px;">' \
            '<col style="width: 30px">' \
            '<col style="width: 30px">' \
            '<col style="width: 30px">' \
            '</colgroup>' \
           '<tr><th></th>' \
           '<th></th>' \
           '<th>Ist</th>' \
           '<th>Soll</th>' \
           '</tr>'



    html += f'</table></td></tr><tr><td></td><td colspan=3> ' \
            f'<b>Ist:</b> Impfungen pro 100k Einw. in den letzten 7 Tagen</b><br>' \
            f'<b>Soll:</b> Nötige Impfungen (100k/7T) um 60% der Bevölkerung bis Ende Juli zu impfen.</b><br>' \
            f'Details: covidlaws.net/ranking7<br>' \
            f'<b>Stand: {vacc_date}</b> // covidlaws.net // Quelle: BAG' \
            f'</td></tr></table>' \
            '</div>' \
            '</body></html>'

    print(html)

    options = {'width': '1200', 'height': '675', 'encoding': "UTF-8", }
    imgkit.from_string(html, "out_image.jpg", options=options)

    return vacc_date
