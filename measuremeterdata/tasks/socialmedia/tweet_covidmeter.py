from measuremeterdata.models.models_ch import DoomsdayClock
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


def tweet():
        create_image()

        text = "Covidmeter-Index\n\nhttps://covidlaws.net/covidmeter/\n\n #CoronaInfoCH"

        send_telegram(text)
        send_tweet(text)

def send_telegram(message):
    #Telegram

    bot = telepot.Bot(settings.TELEGRAM_TOKEN)
    print(bot.getMe())
    bot.sendMessage(settings.TELEGRAM_CHATID, f"Covidmeter\n\nDetails: https://covidlaws.net/covidmeter/")
    bot.sendPhoto(settings.TELEGRAM_CHATID, photo=open("/tmp/out_image.jpg", 'rb'))



def send_tweet(message):
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
       status=f"{message}",
       media_ids=[media.media_id_string])


def create_image():
    doom_clock = DoomsdayClock.objects.get(cur_date=datetime.today())

    quota = doom_clock.hosp_cov19_patients * 100 / doom_clock.hosp_capacity
    quota_str = "{0:.2f}".format(quota)
    value = 0

    if doom_clock.vacc_value > 6000:
        value += 3
    elif doom_clock.vacc_value > 3000:
        value += 2
    elif doom_clock.vacc_value > 1600:
        value += 1
    else:
        value += 0

    if doom_clock.deaths_value > 100:
        value += 0
    elif doom_clock.deaths_value > 50:
        value += 1
    elif doom_clock.deaths_value > 20:
        value += 2
    else:
        value += 3

    if doom_clock.positivity > 5:
        value += 0
    elif doom_clock.positivity > 2:
        value += 1
    else:
        value += 2

    if doom_clock.hosp_average > 80:
        value += 0
    elif doom_clock.hosp_average > 50:
        value += 1
    elif doom_clock.hosp_average > 20:
        value += 2
    else:
        value += 3

    if doom_clock.hosp_cov19_patients > 300:
        value += 0
    elif doom_clock.hosp_cov19_patients > 180:
        value += 1
    elif doom_clock.hosp_cov19_patients > 50:
        value += 2
    else:
        value += 3

    if doom_clock.r_average > 1.15:
        value += 0
    elif doom_clock.r_average > 1:
        value += 1
    elif doom_clock.r_average > 0.9:
        value += 2
    else:
        value += 3

    if doom_clock.incidence_latest > 450:
        value += 0
    elif doom_clock.incidence_latest > 250:
        value += 1
    elif doom_clock.incidence_latest > 100:
        value += 2
    elif doom_clock.incidence_latest > 40:
        value += 3
    else:
        value += 4

    #'#container_2 { -webkit-transform: rotate(90deg); -moz-transform: rotate(90deg); -o-transform: rotate(90deg); -ms-transform: rotate(90deg); transform: rotate(90deg);}' \

    html = f'<html><head><meta charset="UTF-8" /><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.css"/><script src="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.js"></script>' \
           '<style>table, th, td { padding: 10px; font-size: 14; }' \
            '.columnl { float: left; width: 80px; } .columnr { float: left; width: 1000px; }/* Clear floats after the columns */ .row:after {   content: "";   display: table;   clear: both; }' \
            '#rotate-text { width: 45px; transform: rotate(90deg); }' \
            '.peak { text-align: center; font-size: 10; } .container { position: relative; text-align: center; color: white; } .centered { position: absolute; color: black;' \
        'font-size: 18; top: 50%; left: 50%; transform: translate(-50%, -50%); } ' \
       '.bottomed { position: absolute; color: black; font-size: 10; bottom: 1px; left: 50%; transform: translate(-50%, -50%); }'
    html += '.table td, .table th {'\
                'font-size: 25px;'\
            '}'
    html += '''
    		#circle-red {
            width: 140px;
            height: 140px;
            -webkit-border-radius: 70px;
            -moz-border-radius: 70px;
            border-radius: 70px;
            background: red;
         }
		#circle-orange {
            width: 140px;
            height: 140px;
            -webkit-border-radius: 70px;
            -moz-border-radius: 70px;
            border-radius: 70px;
            background: orange;
         }
		#circle-yellow {
            width: 140px;
            height: 140px;
            -webkit-border-radius: 70px;
            -moz-border-radius: 70px;
            border-radius: 70px;
            background: #fbbd08;
         }
		#circle-green {
            width: 140px;
            height: 140px;
            -webkit-border-radius: 70px;
            -moz-border-radius: 70px;
            border-radius: 70px;
            background: green;
         }
        '''
    html += '</style>' \
           f'</head>' \
           '<body style="background-color: #edeeee;"><div style="margin-top: 20px;margin-bottom: 20px;margin-left: 30px;margin-right: 30px">'

    html += f'<div align="center"><h2>Covidmeter-Index</h2>'
    if value < 8:
        html += '<div id="circle-red">'
    elif value < 15:
        html += '<div id="circle-orange">'
    elif value < 19:
        html += '<div id="circle-yellow">'
    else:
        html += '<div id="circle-green">'

    html += f'''
                <div style="padding: 20px 20px 0 20px;"><h1 style="color:White;font-size: 70px;">{value}</h1></div></div>
                <br>
    '''
    html += f'''
             <table class="ui celled table" style="width: 1140px;">
                     <thead>

       <tr  class="left aligned">
          <th>
    '''
    if doom_clock.hosp_cov19_patients > 300:
        html += '<i class="red circular inverted large heartbeat icon"></i>'
    elif doom_clock.hosp_cov19_patients > 180:
        html += '<i class="orange circular inverted large heartbeat icon"></i>'
    elif doom_clock.hosp_cov19_patients > 50:
        html += '<i class="yellow circular inverted large heartbeat icon"></i>'
    else:
        html += '<i class="green circular inverted large heartbeat icon"></i>'

    html += f'''
               Covid-Patienten in der IPS: {doom_clock.hosp_cov19_patients} ({doom_clock.hosp_cov19_patients_7d})
               '''

    if doom_clock.hosp_cov19_patients_7d > doom_clock.hosp_cov19_patients:
        html += '<i class="green arrow circle down icon"></i>'
    else:
        html += '<i class="red arrow circle up icon"></i>'

    html += '''
        </th>
        <th>
        '''
    if doom_clock.hosp_average > 80:
        html += '<i class="red circular inverted large hospital icon"></i>'
    elif doom_clock.hosp_average > 50:
        html += '<i class="orange circular inverted large hospital icon"></i>'
    elif doom_clock.hosp_average > 20:
        html += '<i class="yellow circular inverted large hospital icon"></i>'
    else:
        html += '<i class="green circular inverted large hospital icon"></i>'

    html += f'''
               Neue Spitaleintritte: {doom_clock.hosp_average} ({doom_clock.hosp_average_7d})
               '''

    if doom_clock.hosp_average_7d > doom_clock.hosp_average:
        html += '<i class="green arrow circle down icon"></i>'
    else:
        html += '<i class="red arrow circle up icon"></i>'


    html += '''
        </th>
       </tr>
       <tr class="left aligned">
       <th>
      '''

    if doom_clock.r7_value > 1.15:
        html += '<i class="red circular inverted large chart line icon"></i>'
    elif doom_clock.r7_value > 1:
        html += '<i class="orange circular inverted large chart line icon"></i>'
    elif doom_clock.r7_value > 0.9:
        html += '<i class="yellow circular inverted large chart line icon"></i>'
    else:
        html += '<i class="green circular inverted large chart line icon"></i>'

    html += f'''
               Aktueller R-Wert: {doom_clock.r7_value} ({doom_clock.r1_value})
               '''

    if doom_clock.r1_value > doom_clock.r7_value:
        html += '<i class="green arrow circle down icon"></i>'
    else:
        html += '<i class="red arrow circle up icon"></i>'



    html += '</th><th>'

    if doom_clock.incidence_latest > 450:
        html += '<i class="red circular inverted large chart bar icon"></i>'
    elif doom_clock.incidence_latest > 250:
        html += '<i class="orange circular inverted large chart bar icon"></i>'
    elif doom_clock.incidence_latest > 100:
        html += '<i class="yellow circular inverted large chart bar icon"></i>'
    elif doom_clock.incidence_latest > 40:
        html += '<i class="yellow circular inverted large chart bar icon"></i>'
    else:
        html += '<i class="green circular inverted large chart bar icon"></i>'

    html += f'''
               Fallinzidenz: {doom_clock.incidence_latest} ({doom_clock.incidence_latest_7d})
               '''

    if doom_clock.incidence_latest_7d > doom_clock.incidence_latest:
        html += '<i class="green arrow circle down icon"></i>'
    else:
        html += '<i class="red arrow circle up icon"></i>'

    html += '''
        </th>
       </tr>
       <tr class="left aligned">
       <th>
      '''

    if doom_clock.deaths_value > 100:
        html += '<i class="red circular inverted large times circle icon"></i>'
    elif doom_clock.deaths_value > 50:
        html += '<i class="orange circular inverted large times circle icon"></i>'
    elif doom_clock.deaths_value > 20:
        html += '<i class="yellow circular inverted large times circle icon"></i>'
    else:
        html += '<i class="green circular inverted large times circle icon"></i>'

    html += f'''
               Todesfälle: {round(doom_clock.deaths_value,0)} ({round(doom_clock.deaths_value_7d,0)})
               '''

    if doom_clock.deaths_value_7d > doom_clock.deaths_value:
        html += '<i class="green arrow circle down icon"></i>'
    else:
        html += '<i class="red arrow circle up icon"></i>'

    html += '</th><th>'


    if doom_clock.positivity > 5:
        html += '<i class="red circular inverted large plus icon"></i>'
    elif doom_clock.positivity > 2:
        html += '<i class="orange circular inverted large plus icon"></i>'
    else:
        html += '<i class="green circular inverted large plus icon"></i>'

    html += f'''
               Positivität: {doom_clock.positivity} ({doom_clock.positivity_7d})
               '''

    if doom_clock.positivity_7d > doom_clock.positivity:
        html += '<i class="green arrow circle down icon"></i>'
    else:
        html += '<i class="red arrow circle up icon"></i>'

    html += '''
        </th>
       </tr>
       <tr class="left aligned">
       <th>
      '''

    if doom_clock.vacc_value > 6000:
        html += '<i class="green circular inverted large syringe icon"></i>'
    elif doom_clock.vacc_value > 3000:
        html += '<i class="yellow circular inverted large syringe icon"></i>'
    elif doom_clock.vacc_value > 1600:
        html += '<i class="orange circular inverted large syringe icon"></i>'
    else:
        html += '<i class="red circular inverted large syringe icon"></i>'

    html += f'''
               Impfinzidenz: {round(doom_clock.vacc_value,0)} ({round(doom_clock.vacc_value_7d,0)})
               '''

    if doom_clock.vacc_value_7d < doom_clock.vacc_value:
        html += '<i class="green arrow circle up icon"></i>'
    else:
        html += '<i class="red arrow circle down icon"></i>'

    html += '''
    </th>
       </tr>
        </thead>
        </table>
    '''

    html += '''
    <p>Für Beschreibung der Indikatoren und Details:<br>www.covidlaws.net/covidmeter</p>
        Zahlen in Klammern: Wert eine Woche vor aktuellem Wert.<br>
     Aktuelle und vergangene Zahlen können ändern aufgrund von Nachmeldungen.<br>

     Quelle Daten: BAG
    </body></html>

    '''


    options = {'width': '1200', 'height': '875', 'encoding': "UTF-8", }
    imgkit.from_string(html, "/tmp/out_image.jpg", options=options)

