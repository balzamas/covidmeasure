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

def tweet(type):

    if type > 4:
        countries = Country.objects.filter(isactive=True,population__gte=500000)
    else:
        countries = Country.objects.filter(continent=1,isactive=True)
    scores = create_list(countries)

    message = create_messages(scores, type)
    print("Tweet:")
    print(message)
    send_tweet(message)
    send_telegram(message)

def create_messages(scores, type):

    message_twitter = ""

    if type == 1:
        #Tendency bad
        scores = sorted(scores, key=lambda i: i['tendency'],reverse=True)
        message_twitter = "Euro Stats\nHöchste Zunahme Fälle im Vergleich zur Vorwoche in %\n\n"
        gen_message, countries = generate_list(scores, "tendency", 7, False)
        message_twitter += gen_message

    if type == 2:
        #Tendency good
        scores = sorted(scores, key=lambda i: i['tendency'],reverse=False)
        message_twitter = "Euro Stats\nHöchste Rückgänge Fälle im Vergleich zur Vorwoche in %\n"
        gen_message, countries = generate_list(scores, "tendency", 7, False)
        message_twitter += gen_message

    if type == 3:
        #deaths bad
        scores = sorted(scores, key=lambda i: i['deaths'],reverse=True)
        message_twitter = emoji.emojize('Euro Stats\nCovid-Tote/100k Einwohner in den verg. 2 Wochen (worst)\n')
        gen_message, countries = generate_list(scores, "deaths", 7, False)
        message_twitter += gen_message

    if type == 4:
        #Tendency good
        scores = sorted(scores, key=lambda i: i['deaths'],reverse=False)
        message_twitter = emoji.emojize("Euro Stats\nCovid-Tote/100k Einwohner in den verg. 2 Wochen (best)\n")
        gen_message, countries = generate_list(scores, "deaths", 7, False)
        message_twitter += gen_message

    if type == 5:
        #Tendency bad
        scores = sorted(scores, key=lambda i: i['tendency'],reverse=True)
        message_twitter = "World Stats\nHöchste Zunahme Fälle im Vergleich zur Vorwoche in %\n\n"
        gen_message, countries = generate_list(scores, "tendency", 11, False)
        message_twitter += gen_message

    if type == 6:
        #Tendency good
        scores = sorted(scores, key=lambda i: i['tendency'],reverse=False)
        message_twitter = "World Stats\nHöchste Rückgänge Fälle im Vergleich zur Vorwoche in %\n"
        gen_message, countries = generate_list(scores, "tendency", 11, False)
        message_twitter += gen_message

    if type == 7:
        #deaths bad
        scores = sorted(scores, key=lambda i: i['deaths'],reverse=True)
        message_twitter = emoji.emojize('World Stats\nCovid-Tote/100k Einwohner in den verg. 2 Wochen (worst)\n')
        gen_message, countries = generate_list(scores, "deaths", 11, False)
        message_twitter += gen_message

    if type == 8:
        #Tendency good
        scores = sorted(scores, key=lambda i: i['deaths'],reverse=False)
        message_twitter = emoji.emojize("World Stats\nCovid-Tote/100k Einwohner in den verg. 2 Wochen (best)\n")
        gen_message, countries = generate_list(scores, "deaths", 11, False)
        message_twitter += gen_message

    if type == 9:
        scores = sorted(scores, key=lambda i: i['cur_prev14'],reverse=True)
        message_twitter = emoji.emojize("World Stats\nFall-Inzidenz (14 Tage/100k Einwohner)\n")
        gen_message, countries = generate_list(scores, "cur_prev14", 11, True)
        message_twitter += gen_message

    if type == 10:
        scores = sorted(scores, key=lambda i: i['cur_prev14'],reverse=False)
        message_twitter = emoji.emojize("World Stats\nFall-Inzidenz (14 Tage/100k Einwohner) (tiefste)\n")
        gen_message, countries = generate_list(scores, "cur_prev14", 11, True)
        message_twitter += gen_message

    cntry_list = ""
    for country in countries:
       cntry_list+=str(country)+","

    end_date = datetime.now()
    start_date =  end_date - timedelta(days=62)

    if type > 4:
        message_twitter += "\n\ncovidlaws.net/ranking_world\n"
    else:
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
            last_stringency_date = None
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


            try:
                score = float(cases[0].cases_past14days) + float(cases[0].cases_past7days) + (float(cases[0].development7to7) * float(cases[0].cases_past7days) /100) + (float(last_positivity_calc) * float(cases[0].cases_past7days) / 50) + float((cases[0].deaths_past14days * 20))
                score_7days_before = float(case_14days_7daysago.cases_past14days) + float(case_14days_7daysago.cases_past7days) + (float(case_14days_7daysago.development7to7) * float(case_14days_7daysago.cases_past7days) /100) + (float(positivity_before7) * float(case_14days_7daysago.cases_past7days) / 50) + float((case_14days_7daysago.deaths_past14days * 20))
            except:
                print(f"{country} failed...")
                score = None

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
                                "has_measures": country.has_measures, "continent": country.continent.pk, "icon": arrow,
                                "peak_cases": peak_cases, "peak_cases_date": peak_cases_date,
                                "peak_deaths": peak_deaths, "peak_deaths_date": peak_deaths_date,
                                "peak_positivity": peak_positivity, "peak_positivity_date": peak_positivity_date,
                                "R": last_R, "R_date": last_R_date, "stringency": last_stringency, "stringency_date": last_stringency_date
                                }

                if last_prev14 > 2:
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




def generate_list(scores, field, max, show_tend):
    count = 0
    countries = []

    list = ""

    for score in scores:
        if (count < max):
            if max > 7:
                tend_icon = ""
                if show_tend:
                    if (score["tendency"]> 5):
                        tend_icon = "\U0001F4C8"
                    elif (score["tendency"]> -5):
                        tend_icon = "\U0001F4C9"
                    else:
                        tend_icon = "\U0001F538"

                list += tend_icon + " " + str(score[field]).split(".")[0] + " " + flag.flag(score["code"]) + " " + score["code"] + "\n"
            else:
                list += str(score[field]) + " " + flag.flag(score["code"]) + " " + score["name"] +"\n"
            countries.append(score["pk"])
        count += 1

    return list, countries
