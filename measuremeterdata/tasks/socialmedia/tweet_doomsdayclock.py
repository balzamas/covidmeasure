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

        text = "Öffnungs-o-meter\n\nhttps://covidlaws.net/doomsdayclock/\n\n #CoronaInfoCH"

        send_telegram(text)
        send_tweet(text)

def send_telegram(message):
    #Telegram

    bot = telepot.Bot(settings.TELEGRAM_TOKEN)
    print(bot.getMe())
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
    doom_clock = DoomsdayClock.objects.get(name="Master")

    quota = doom_clock.hosp_cov19_patients * 100 / doom_clock.hosp_capacity
    quota_str = "{0:.2f}".format(quota)
    value = 0

    if doom_clock.positivity < 5:
        value += 1

    if doom_clock.hosp_cov19_patients < 250:
        value += 1

    if doom_clock.r_okay:
        value += 1

    if doom_clock.incidence_mar1 > doom_clock.incidence_latest:
        value += 1

    #'#container_2 { -webkit-transform: rotate(90deg); -moz-transform: rotate(90deg); -o-transform: rotate(90deg); -ms-transform: rotate(90deg); transform: rotate(90deg);}' \

    html = f'<html><head><meta charset="UTF-8" /><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.css"/><script src="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.js"></script>' \
           '<style>table, th, td { padding: 10px; font-size: 14; }' \
            '.columnl { float: left; width: 80px; } .columnr { float: left; width: 1000px; }/* Clear floats after the columns */ .row:after {   content: "";   display: table;   clear: both; }' \
            '#rotate-text { width: 45px; transform: rotate(90deg); }' \
            '.peak { text-align: center; font-size: 10; } .container { position: relative; text-align: center; color: white; } .centered { position: absolute; color: black;' \
        'font-size: 18; top: 50%; left: 50%; transform: translate(-50%, -50%); } ' \
       '.bottomed { position: absolute; color: black; font-size: 10; bottom: 1px; left: 50%; transform: translate(-50%, -50%); }' \
            '</style>' \
           f'</head>' \
           '<body style="background-color: #edeeee;"><div style="margin-top: 20px;margin-bottom: 20px;margin-left: 30px;margin-right: 30px">'

    html += f'<div align="center"><h2>Öffnungs-o-meter</h2><p><img src="https://covidlaws.net/static/images/clock/{value}.png"></p><table class="ui celled table"><tr  class="center aligned">'
    if doom_clock.hosp_cov19_patients < 250:
        html += '<td class ="positive">'
    else:
        html += '<td class ="negative" >'

    html += f'''
           Anzahl Covid-Patienten in Intensivpflege < 250
         </td>
       </tr>
       <tr  class="center aligned">
         <td>
          Covid-Patienten in IPS: {doom_clock.hosp_cov19_patients} // Gesamtkapazität IPS: {doom_clock.hosp_capacity} // Quote: {quota_str}% // Stand: {doom_clock.hosp_date}
         </td>
       </tr>
     </table>

     <table class="ui celled table">
       <tr  class="center aligned">
    '''

    if doom_clock.positivity < 5:
        html += '<td class ="positive">'
    else:
        html += '<td class ="negative" >'

    html += f'''
               Positivitätsrate < 5%
         </td>
       </tr>
       <tr  class="center aligned">
         <td>
          Positivitätsrate: {doom_clock.positivity}% (Durchschnitt d. letzten 7 Tage) // Stand: {doom_clock.positivity_date}
         </td>
       </tr>
     </table>

          <table class="ui celled table">
       <tr  class="center aligned">

    '''

    if doom_clock.r_okay:
        html += '<td class ="positive" colspan="5">'
    else:
        html += '<td class ="negative" colspan="5">'

    html += f'''
               Letzten 5 R-Werte unter 1
         </td>
       </tr>
       <tr  class="center aligned">
         <td>
        {doom_clock.r1_date}: {doom_clock.r1_value}
           </td>
         <td>
        {doom_clock.r2_date}: {doom_clock.r2_value}
           </td>
         <td>
        {doom_clock.r3_date}: {doom_clock.r3_value}
           </td>
         <td>
        {doom_clock.r4_date}: {doom_clock.r4_value}
           </td>
         <td>
        {doom_clock.r5_date}: {doom_clock.r5_value}
           </td>
         </td>
       </tr>
     </table>

               <table class="ui celled table" width="500px">
       <tr  class="center aligned">
    '''

    if doom_clock.incidence_mar1 >  doom_clock.incidence_latest:
        html += '<td class ="positive">'
    else:
        html += '<td class ="negative" >'


    html += f'''
               14-Tage Inzidenz unter Wert 1. März
         </td>
       </tr>
       <tr  class="center aligned">
         <td>
           Wert 1. März: {doom_clock.incidence_mar1} // Wert Aktuell: {doom_clock.incidence_latest} // Stand: {doom_clock.incidence_latest_date}
           </td>
       </tr>
     </table>
    </body></html>

    '''


    options = {'width': '1200', 'height': '675', 'encoding': "UTF-8", }
    imgkit.from_string(html, "/tmp/out_image.jpg", options=options)

