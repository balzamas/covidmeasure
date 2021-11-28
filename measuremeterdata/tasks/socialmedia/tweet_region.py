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


def tweet(type):

    text = None

    if type == 1:
        region = "Scandinavia"
        countries = Country.objects.filter(pk__in=[8, 22, 23, 24, 44])
        scores = create_list(countries)
        print(scores)
        text = create_image(region, scores, True)
        print(text)

    if type == 2:
        region = "Switzerland and neighbours"
        countries = Country.objects.filter(pk__in=[6, 35, 34, 33, 1])
        scores = create_list(countries)
        text = create_image(region, scores, True)

    if type == 3:
        region = "Central Europe"
        countries = Country.objects.filter(pk__in=[3, 12, 29, 18])
        scores = create_list(countries)
        text = create_image(region, scores, True)

    if type == 4:
        region = "Baltics"
        countries = Country.objects.filter(pk__in=[25,9,26,16])
        scores = create_list(countries)
        text = create_image(region, scores, True)

    if type == 5:
        region = "Eastern Africa"
        countries = Country.objects.filter(pk__in=[5,89,98,88])
        scores = create_list(countries)
        text = create_image(region, scores, False)

    if type == 6:
        region = "Southern Africa"
        countries = Country.objects.filter(pk__in=[90,97,102,103,104])
        scores = create_list(countries)
        text = create_image(region, scores, False)

    if type == 7:
        region = "Western Africa"
        countries = Country.objects.filter(pk__in=[55,91,95,92,96])
        scores = create_list(countries)
        text = create_image(region, scores, False)

    if type == 8:
        region = "Postsoviet space"
        countries = Country.objects.filter(pk__in=[27,50,21,46,47,45])
        scores = create_list(countries)
        text = create_image(region, scores, False)

    if type == 9:
        region = "Eastern Balkans"
        countries = Country.objects.filter(pk__in=[30,32,42,40,39,38])
        scores = create_list(countries)
        text = create_image(region, scores, False)

    if type == 10:
        region = "South America (South)"
        countries = Country.objects.filter(pk__in=[82,83,80,84,81])
        scores = create_list(countries)
        text = create_image(region, scores, False)

    if type == 11:
        region = "South East Asia"
        countries = Country.objects.filter(pk__in=[67,65,66,68,69])
        scores = create_list(countries)
        text = create_image(region, scores, False)

    if type == 12:
        region = "Indian Subcontinent"
        countries = Country.objects.filter(pk__in=[70,85,72,71,73, 109])
        scores = create_list(countries)
        text = create_image(region, scores, False)

    if type == 13:
        region = "Arab Gulf"
        countries = Country.objects.filter(pk__in=[78,79,87,77,110])
        scores = create_list(countries)
        text = create_image(region, scores, False)

#    page_access_token = settings.FACEBOOK_ACCESS_TOKEN
#    graph = facebook.GraphAPI(page_access_token)
#    facebook_page_id = settings.FACEBOOK_PAGE_ID
#    graph.put_object(facebook_page_id, "feed", message='test message')



    if text:
        cntry_list = ""

        for country in countries:
            cntry_list += str(country.pk) + ","

        end_date = datetime.now()
        start_date = end_date - timedelta(days=62)

        text += "\n\nLändervergleich:\n"
        text += f"covidlaws.net/compare/{cntry_list}&1,2,5&{start_date.strftime('%Y-%m-%d')}&{end_date.strftime('%Y-%m-%d')}"

        print(text)
        send_telegram(text)
        send_tweet(text)

def send_telegram(message):
    #Telegram

    bot = telepot.Bot(settings.TELEGRAM_TOKEN)
    print(bot.getMe())
    bot.sendMessage(settings.TELEGRAM_CHATID, f"{message}")
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


def create_image(region, scores, show_hosp):
    canton_vals = []

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
           '<body style="background-color: #edeeee;"><div style="margin-top: 20px;margin-bottom: 20px;">' \
           '<table style="margin-left: auto;margin-right: auto;">' \
           '<tr style="vertical-align: top;"><td style="vertical-align: top;text-align: right" nowrap>' \
           f'<div id="rotate-text"><h1>&nbsp;&nbsp;&nbsp;{region}</h1></div>' \
            '</td><td>' \
           '<table class="ui celled table" style="width: 930px;table-layout:fixed">' \
            '<colgroup>' \
            '<col style="width: 150px;">' \
            '<col style="width: 150px">' \
            '<col style="width: 150px">'
    if show_hosp:
             html +=  '<col style="width: 150px">'
    html += '<col style="width: 150px">' \
            '<col style="width: 130px">' \
           '<col style="width: 90px">'\
           '<col style="width: 90px">' \
           '<col style="width: 150px">'\
           '</colgroup>' \
           '<tr><th></th>' \
           '<th>Pos. Tests per 100k<br>Last 14 days</th>' \
           '<th>Deaths per 100k<br>Last 14 days</th>'
    if show_hosp:
           '<th>Hospitalisations<br>per 1 Mill.</th>'
    html += '<th>Positive rate<br>7 days avg. @ Date</th>' \
           '<th>Development<br>Week over week</th>' \
           '<th>Vacc. per<br>100 pop.*</th>' \
           '<th>Tests per<br>1000 pop.</th>' \
           '<th>Stringency index</th>' \
           '</tr>'



    for score in scores:
        html += f'<tr>' \
                f'<td nowrap><b style="font-size: 18">{score["name"]}</b></td>'

        html += f'<td nowrap>'
        html += f'<div class="container"> \
          <img src=https://covidlaws.net/static/images/graphs_world/{score["code"]}_cases.png height="70px"> \
          <div class="centered">{score["cur_prev14"]}</div> \
        </div> \
        </td>'

        html += '<td nowrap>'
        html += f'<div class="container"> \
          <img src=https://covidlaws.net/static/images/graphs_world/{score["code"]}_deaths.png height="70px"> \
          <div class="centered">{score["deaths"]}</div> \
        </div> '
        html += '</td>'

        if show_hosp:
            html += '<td nowrap>'
            html += f'<div class="container"> \
              <img src=https://covidlaws.net/static/images/graphs_world/{score["code"]}_hosp.png height="70px"> \
              <div class="centered">{score["hosp"]}</div> \
              <div class="bottomed">{score["hosp_date"]}</div> \
            </div> '
            html += '</td>'

        html += "<td nowrap>"
        if score["positivity"] != None:
          html += f'<div class="container">' \
            f'<img src=https://covidlaws.net/static/images/graphs_world/{score["code"]}_positivity.png height="70px">' \
            f'<div class="centered">{"{:10.2f}".format(score["positivity"])}%</div>' \
            f'<div class="bottomed">{score["positivity_date"]}</div>' \
            '</div>'
        html += "</td>"



        if score["tendency"] < 0:
            html += f'<td class="positive" nowrap><div class="container"><div class ="centered">{score["tendency"]} %</div></div></td>'
        else:
            html += f'<td class="negative" nowrap><div class="container"><div class ="centered">{score["tendency"]} %</div></div></td>'


        html += "<td nowrap>"
        if score["vaccination"] != None:
            html += f'<div class="container">' \
                    f'<div class="centered">{"{:10.2f}".format(score["vaccination"])}</div>' \
                    f'<div class="bottomed">{score["vaccination_date"]}</div>' \
                    '</div>'
        html += "</td>"

        html += "<td nowrap>"
        if score["tests"] != None:
            html += f'<div class="container">' \
                    f'<div class="centered">{"{:10.2f}".format(score["tests"])}</div>' \
                    f'<div class="bottomed">{score["tests_date"]}</div>' \
                    '</div>'
        html += "</td>"



        html += "<td nowrap>"
        if score["stringency"] != None:
          html += f'<div class="container">' \
                  f'<img src=https://covidlaws.net/static/images/graphs_world/{score["code"]}_stringency.png height="70px">' \
                  f'<div class="centered">{"{:10.2f}".format(score["stringency"])}</div>' \
                  f'<div class="bottomed">{score["stringency_date"]}</div>' \
                  '</div>'
        html += "</td>"

        html += '</tr>'


    html += f'</table>' \
            "* Vaccination: People who received at least one shot per 100.<br>" \
            "covidlaws.net // Quellen: JHU/Our world in data/Oxford University/ETH Zürich</td></tr></table>" \
            '</div>' \
            '</body></html>'

    if show_hosp:
        options = {'width': '1360', 'height': '675', 'encoding': "UTF-8", }
    else:
        options = {'width': '1200', 'height': '675', 'encoding': "UTF-8", }
    imgkit.from_string(html, "out_image.jpg", options=options)

    return f"Regionalvergleich\n\n{region}"


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
            last_hosp = None
            last_hosp_date = None
            last_R = None
            last_R_date = None
            positivity_before7 = None
            last_stringency = None
            last_tests = None
            last_tests_date = None
            last_vaccination = None
            last_vaccination_date = None

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

                if (case.tests_smoothed_per_thousand and last_tests == None):
                    last_tests = case.tests_smoothed_per_thousand
                    last_tests_date = case.date

                if (case.people_vaccinated_per_hundred and last_vaccination == None):
                    last_vaccination = case.people_vaccinated_per_hundred
                    last_vaccination_date = case.date

                if (case.hosp_per_million != None and last_hosp == None):
                    last_hosp = case.hosp_per_million
                    last_hosp_date = case.date

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

                canton_toadd = {"name": country.name, "pk": country.pk, "score": int(score), "score_before": int(score_7days_before),
                                "date": last_date, "code": country.code,
                                "cur_prev14": last_prev14, "tendency": last_tendency,
                                "cur_prev7": case_14days_14daysago.cases_past7days,
                                "positivity": last_positivity, "positivity_date":last_positivity_date, "deaths": last_deaths14,
                                "hosp": last_hosp, "hosp_date": last_hosp_date,
                                "has_measures": country.has_measures, "continent": country.continent.pk, "icon": arrow,
                                "peak_cases": peak_cases, "peak_cases_date": peak_cases_date,
                                "peak_deaths": peak_deaths, "peak_deaths_date": peak_deaths_date,
                                "peak_positivity": peak_positivity, "peak_positivity_date": peak_positivity_date,
                                "R": last_R, "R_date": last_R_date, "stringency": last_stringency, "stringency_date": last_stringency_date,
                                "tests": last_tests, "tests_date": last_tests_date,
                                "vaccination": last_vaccination, "vaccination_date": last_vaccination_date
                                }

                country_vals.append(canton_toadd)

    scores = sorted(country_vals, key=lambda i: i['cur_prev14'],reverse=False)

    return scores
