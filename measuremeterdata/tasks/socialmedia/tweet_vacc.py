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
import os
import csv
import datetime
from datetime import date, timedelta
import requests
import pandas as pd
from io import BytesIO
import gzip
from urllib.request import urlopen
from measuremeterdata.tasks import import_helper
import pandas as pd
import zipfile
import urllib.request, json
from decimal import *

def tweet(week):
    create_image(week)

#    page_access_token = settings.FACEBOOK_ACCESS_TOKEN
#    graph = facebook.GraphAPI(page_access_token)
#    facebook_page_id = settings.FACEBOOK_PAGE_ID
#    graph.put_object(facebook_page_id, "feed", message='test message')

    send_telegram(week)
    send_tweet(week)

def send_telegram(week):
    #Telegram

    bot = telepot.Bot(settings.TELEGRAM_TOKEN)
    print(bot.getMe())
    bot.sendMessage(settings.TELEGRAM_CHATID, f'Vollständig Geimpfte vs. Unvollständig Geimpfte/Ungeimpfte\nStand: Woche {week - 4} bis {week}\n28-Tage-Inzidenzen Fälle/Hospitalisierte/Tote\nDaten sind im BAG-File als "limited" markiert, d.h. noch sehr inkomplett.\nDie Tabelle dient als Demo bis die Zahlen zuverlässiger werden.Geimpfte vs. Ungeimpfte')
    bot.sendPhoto(settings.TELEGRAM_CHATID, photo=open("/tmp/out_image.jpg", 'rb'))



def send_tweet(week):
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
       status=f'Vollständig Geimpfte vs. Unvollständig Geimpfte/Ungeimpfte\nStand: Woche {week - 4} bis {week}\n28-Tage-Inzidenzen Fälle/Hospitalisierte/Tote\nDaten sind im BAG-File als "limited" markiert, d.h. noch sehr inkomplett.\nDie Tabelle dient als Demo bis die Zahlen zuverlässiger werden.Geimpfte vs. Ungeimpfte',
       media_ids=[media.media_id_string])

def get_vacced_by_agegroup(age_group, date_week, zf):
        df_tot_vacc = pd.read_csv(zf.open('data/COVID19VaccPersons_AKL10_w_v2.csv'), error_bad_lines=False)

        rslt_df = df_tot_vacc[(df_tot_vacc['geoRegion'] == "CHFL") &
                            (df_tot_vacc['altersklasse_covid19'] == age_group) &
                             (df_tot_vacc['date'] == date_week) &
                            (df_tot_vacc['type'] == "COVID19FullyVaccPersons") ]

        return rslt_df['sumTotal'].item()


def get_cases_tot_by_agegroup(age_group, week, zf):
    df_tot_vacc = pd.read_csv(zf.open('data/COVID19Cases_geoRegion_AKL10_w.csv'), error_bad_lines=False)

    tot = 0

    for x in range(4):
        date_week = (202100 + week - x)
        rslt_df = df_tot_vacc[(df_tot_vacc['geoRegion'] == "CHFL") &
                              (df_tot_vacc['altersklasse_covid19'] == age_group) &
                              (df_tot_vacc['datum'] == date_week)]

        tot += rslt_df['entries'].item()

    return tot


def get_vacccases_tot_by_agegroup(age_group, week, zf):
    df_tot_vacc = pd.read_csv(zf.open('data/COVID19Cases_vaccpersons_AKL10_w.csv'), error_bad_lines=False)

    tot = 0

    for x in range(4):
        date_week = (202100 + week - x)
        rslt_df = df_tot_vacc[(df_tot_vacc['geoRegion'] == "CHFL") &
                              (df_tot_vacc['altersklasse_covid19'] == age_group) &
                              (df_tot_vacc['date'] == date_week)]

        tot += rslt_df['entries'].item()

    return tot

def get_hosp_tot_by_agegroup(age_group, week, zf):
    df_tot_vacc = pd.read_csv(zf.open('data/COVID19Hosp_geoRegion_AKL10_w.csv'), error_bad_lines=False)

    tot = 0

    for x in range(4):
        date_week = (202100 + week - x)
        rslt_df = df_tot_vacc[(df_tot_vacc['geoRegion'] == "CHFL") &
                              (df_tot_vacc['altersklasse_covid19'] == age_group) &
                              (df_tot_vacc['datum'] == date_week)]

        tot += rslt_df['entries'].item()

    return tot


def get_vacchosp_tot_by_agegroup(age_group, week, zf):
    df_tot_vacc = pd.read_csv(zf.open('data/COVID19Hosp_vaccpersons_AKL10_w.csv'), error_bad_lines=False)

    tot = 0

    for x in range(4):
        date_week = (202100 + week - x)
        rslt_df = df_tot_vacc[(df_tot_vacc['geoRegion'] == "CHFL") &
                              (df_tot_vacc['altersklasse_covid19'] == age_group) &
                              (df_tot_vacc['date'] == date_week)]

        tot += rslt_df['entries'].item()

    return tot

def get_death_tot_by_agegroup(age_group, week, zf):
    df_tot_vacc = pd.read_csv(zf.open('data/COVID19Death_geoRegion_AKL10_w.csv'), error_bad_lines=False)

    tot = 0

    for x in range(4):
        date_week = (202100 + week - x)
        rslt_df = df_tot_vacc[(df_tot_vacc['geoRegion'] == "CHFL") &
                              (df_tot_vacc['altersklasse_covid19'] == age_group) &
                              (df_tot_vacc['datum'] == date_week)]

        tot += rslt_df['entries'].item()

    return tot


def get_vaccdeath_tot_by_agegroup(age_group, week, zf):
    df_tot_vacc = pd.read_csv(zf.open('data/COVID19Death_vaccpersons_AKL10_w.csv'), error_bad_lines=False)

    tot = 0

    for x in range(4):
        date_week = (202100 + week - x)
        rslt_df = df_tot_vacc[(df_tot_vacc['geoRegion'] == "CHFL") &
                              (df_tot_vacc['altersklasse_covid19'] == age_group) &
                              (df_tot_vacc['date'] == date_week)]

        tot += rslt_df['entries'].item()

    return tot


def create_image(week):
    date_week = 202100 + week

    pop_0_9 = 873043
    pop_10_19 = 844155
    pop_20_29 = 1045350
    pop_30_39 = 1229176
    pop_40_49 = 1198325
    pop_50_59 = 1292837
    pop_60_69 = 947959
    pop_70_79 = 721518
    pop_80plus = 453670

    with urllib.request.urlopen("https://www.covid19.admin.ch/api/data/context") as url:
        data = json.loads(url.read().decode())

        resp = urlopen(
            data['sources']['zip']['csv'])

        zf = zipfile.ZipFile(BytesIO(resp.read()), 'r')


        tot_vacc_0_9 = get_vacced_by_agegroup("0 - 9", date_week,zf)
        tot_vacc_10_19 = get_vacced_by_agegroup("10 - 19", date_week,zf)
        tot_vacc_20_29 = get_vacced_by_agegroup("20 - 29", date_week,zf)
        tot_vacc_30_39 = get_vacced_by_agegroup("30 - 39", date_week,zf)
        tot_vacc_40_49 = get_vacced_by_agegroup("40 - 49", date_week,zf)
        tot_vacc_50_59 = get_vacced_by_agegroup("50 - 59", date_week,zf)
        tot_vacc_60_69 = get_vacced_by_agegroup("60 - 69", date_week,zf)
        tot_vacc_70_79 = get_vacced_by_agegroup("70 - 79", date_week,zf)
        tot_vacc_80plus = get_vacced_by_agegroup("80+", date_week,zf)

        tot_nonvacc_0_9 = pop_0_9 - tot_vacc_0_9
        tot_nonvacc_10_19 = pop_10_19 - tot_vacc_10_19
        tot_nonvacc_20_29 = pop_20_29 - tot_vacc_20_29
        tot_nonvacc_30_39 = pop_30_39 - tot_vacc_30_39
        tot_nonvacc_40_49 = pop_40_49 - tot_vacc_40_49
        tot_nonvacc_50_59 = pop_50_59 - tot_vacc_50_59
        tot_nonvacc_60_69 = pop_60_69 - tot_vacc_60_69
        tot_nonvacc_70_79 = pop_70_79 - tot_vacc_70_79
        tot_nonvacc_80plus = pop_80plus - tot_vacc_80plus


        #Cases ------------------------------------------------------------------------

        cases_tot_0_9 = get_cases_tot_by_agegroup("0 - 9",week,zf)
        cases_tot_10_19 = get_cases_tot_by_agegroup("10 - 19", week,zf)
        cases_tot_20_29 = get_cases_tot_by_agegroup("20 - 29", week,zf)
        cases_tot_30_39 = get_cases_tot_by_agegroup("30 - 39", week,zf)
        cases_tot_40_49 = get_cases_tot_by_agegroup("40 - 49", week,zf)
        cases_tot_50_59 = get_cases_tot_by_agegroup("50 - 59", week,zf)
        cases_tot_60_69 = get_cases_tot_by_agegroup("60 - 69", week,zf)
        cases_tot_70_79 = get_cases_tot_by_agegroup("70 - 79", week,zf)
        cases_tot_80plus = get_cases_tot_by_agegroup("80+", week,zf)

        vacccases_tot_0_9 = get_vacccases_tot_by_agegroup("0 - 9",week,zf)
        vacccases_tot_10_19 = get_vacccases_tot_by_agegroup("10 - 19", week,zf)
        vacccases_tot_20_29 = get_vacccases_tot_by_agegroup("20 - 29", week,zf)
        vacccases_tot_30_39 = get_vacccases_tot_by_agegroup("30 - 39", week,zf)
        vacccases_tot_40_49 = get_vacccases_tot_by_agegroup("40 - 49", week,zf)
        vacccases_tot_50_59 = get_vacccases_tot_by_agegroup("50 - 59", week,zf)
        vacccases_tot_60_69 = get_vacccases_tot_by_agegroup("60 - 69", week,zf)
        vacccases_tot_70_79 = get_vacccases_tot_by_agegroup("70 - 79", week,zf)
        vacccases_tot_80plus = get_vacccases_tot_by_agegroup("80+", week,zf)

        nonvacccases_tot_0_9 = cases_tot_0_9 - vacccases_tot_0_9
        nonvacccases_tot_10_19 = cases_tot_10_19 - vacccases_tot_10_19
        nonvacccases_tot_20_29 = cases_tot_20_29 - vacccases_tot_20_29
        nonvacccases_tot_30_39 = cases_tot_30_39 - vacccases_tot_30_39
        nonvacccases_tot_40_49 = cases_tot_40_49 - vacccases_tot_40_49
        nonvacccases_tot_50_59 = cases_tot_50_59 - vacccases_tot_50_59
        nonvacccases_tot_60_69 = cases_tot_60_69 - vacccases_tot_60_69
        nonvacccases_tot_70_79 = cases_tot_70_79 - vacccases_tot_70_79
        nonvacccases_tot_80plus = cases_tot_80plus - vacccases_tot_80plus

        inz_vacccases_0_9 = 100000 * vacccases_tot_0_9 / tot_vacc_0_9
        inz_vacccases_10_19 = 100000 * vacccases_tot_10_19 / tot_vacc_10_19
        inz_vacccases_20_29 = 100000 * vacccases_tot_20_29 / tot_vacc_20_29
        inz_vacccases_30_39 = 100000 * vacccases_tot_30_39 / tot_vacc_30_39
        inz_vacccases_40_49 = 100000 * vacccases_tot_40_49 / tot_vacc_40_49
        inz_vacccases_50_59 = 100000 * vacccases_tot_50_59 / tot_vacc_50_59
        inz_vacccases_60_69 = 100000 * vacccases_tot_60_69 / tot_vacc_60_69
        inz_vacccases_70_79 = 100000 * vacccases_tot_70_79 / tot_vacc_70_79
        inz_vacccases_80plus = 100000 * vacccases_tot_80plus / tot_vacc_80plus

        inz_nonvacccases_0_9 = 100000 * nonvacccases_tot_0_9 / tot_nonvacc_0_9
        inz_nonvacccases_10_19 = 100000 * nonvacccases_tot_10_19 / tot_nonvacc_10_19
        inz_nonvacccases_20_29 = 100000 * nonvacccases_tot_20_29 / tot_nonvacc_20_29
        inz_nonvacccases_30_39 = 100000 * nonvacccases_tot_30_39 / tot_nonvacc_30_39
        inz_nonvacccases_40_49 = 100000 * nonvacccases_tot_40_49 / tot_nonvacc_40_49
        inz_nonvacccases_50_59 = 100000 * nonvacccases_tot_50_59 / tot_nonvacc_50_59
        inz_nonvacccases_60_69 = 100000 * nonvacccases_tot_60_69 / tot_nonvacc_60_69
        inz_nonvacccases_70_79 = 100000 * nonvacccases_tot_70_79 / tot_nonvacc_70_79
        inz_nonvacccases_80plus = 100000 * nonvacccases_tot_80plus / tot_nonvacc_80plus

        rel_cases_0_9 = None
        try:
            rel_cases_0_9 = inz_nonvacccases_0_9 / inz_vacccases_0_9
        except:
            pass

        rel_cases_10_19 = None
        try:
            rel_cases_10_19 = inz_nonvacccases_10_19 / inz_vacccases_10_19
        except:
            pass

        rel_cases_20_29 = None
        try:
            rel_cases_20_29 = inz_nonvacccases_20_29 / inz_vacccases_20_29
        except:
            pass

        rel_cases_30_39 = None
        try:
            rel_cases_30_39 = inz_nonvacccases_30_39 / inz_vacccases_30_39
        except:
            pass

        rel_cases_40_49 = None
        try:
            rel_cases_40_49 = inz_nonvacccases_40_49 / inz_vacccases_40_49
        except:
            pass

        rel_cases_50_59 = None
        try:
            rel_cases_50_59 = inz_nonvacccases_50_59 / inz_vacccases_50_59
        except:
            pass

        rel_cases_60_69 = None
        try:
            rel_cases_60_69 = inz_nonvacccases_60_69 / inz_vacccases_60_69
        except:
            pass

        rel_cases_70_79 = None
        try:
            rel_cases_70_79 = inz_nonvacccases_70_79 / inz_vacccases_70_79
        except:
            pass

        rel_cases_80plus = None
        try:
            rel_cases_80plus = inz_nonvacccases_80plus / inz_vacccases_80plus
        except:
            pass



        #Hosp ------------------------------------------------------------------------

        hosp_tot_0_9 = get_hosp_tot_by_agegroup("0 - 9",week,zf)
        hosp_tot_10_19 = get_hosp_tot_by_agegroup("10 - 19", week,zf)
        hosp_tot_20_29 = get_hosp_tot_by_agegroup("20 - 29", week,zf)
        hosp_tot_30_39 = get_hosp_tot_by_agegroup("30 - 39", week,zf)
        hosp_tot_40_49 = get_hosp_tot_by_agegroup("40 - 49", week,zf)
        hosp_tot_50_59 = get_hosp_tot_by_agegroup("50 - 59", week,zf)
        hosp_tot_60_69 = get_hosp_tot_by_agegroup("60 - 69", week,zf)
        hosp_tot_70_79 = get_hosp_tot_by_agegroup("70 - 79", week,zf)
        hosp_tot_80plus = get_hosp_tot_by_agegroup("80+", week,zf)

        vacchosp_tot_0_9 = get_vacchosp_tot_by_agegroup("0 - 9",week,zf)
        vacchosp_tot_10_19 = get_vacchosp_tot_by_agegroup("10 - 19", week,zf)
        vacchosp_tot_20_29 = get_vacchosp_tot_by_agegroup("20 - 29", week,zf)
        vacchosp_tot_30_39 = get_vacchosp_tot_by_agegroup("30 - 39", week,zf)
        vacchosp_tot_40_49 = get_vacchosp_tot_by_agegroup("40 - 49", week,zf)
        vacchosp_tot_50_59 = get_vacchosp_tot_by_agegroup("50 - 59", week,zf)
        vacchosp_tot_60_69 = get_vacchosp_tot_by_agegroup("60 - 69", week,zf)
        vacchosp_tot_70_79 = get_vacchosp_tot_by_agegroup("70 - 79", week,zf)
        vacchosp_tot_80plus = get_vacchosp_tot_by_agegroup("80+", week,zf)

        nonvacchosp_tot_0_9 = hosp_tot_0_9 - vacchosp_tot_0_9
        nonvacchosp_tot_10_19 = hosp_tot_10_19 - vacchosp_tot_10_19
        nonvacchosp_tot_20_29 = hosp_tot_20_29 - vacchosp_tot_20_29
        nonvacchosp_tot_30_39 = hosp_tot_30_39 - vacchosp_tot_30_39
        nonvacchosp_tot_40_49 = hosp_tot_40_49 - vacchosp_tot_40_49
        nonvacchosp_tot_50_59 = hosp_tot_50_59 - vacchosp_tot_50_59
        nonvacchosp_tot_60_69 = hosp_tot_60_69 - vacchosp_tot_60_69
        nonvacchosp_tot_70_79 = hosp_tot_70_79 - vacchosp_tot_70_79
        nonvacchosp_tot_80plus = hosp_tot_80plus - vacchosp_tot_80plus

        inz_vacchosp_0_9 = 100000 * vacchosp_tot_0_9 / tot_vacc_0_9
        inz_vacchosp_10_19 = 100000 * vacchosp_tot_10_19 / tot_vacc_10_19
        inz_vacchosp_20_29 = 100000 * vacchosp_tot_20_29 / tot_vacc_20_29
        inz_vacchosp_30_39 = 100000 * vacchosp_tot_30_39 / tot_vacc_30_39
        inz_vacchosp_40_49 = 100000 * vacchosp_tot_40_49 / tot_vacc_40_49
        inz_vacchosp_50_59 = 100000 * vacchosp_tot_50_59 / tot_vacc_50_59
        inz_vacchosp_60_69 = 100000 * vacchosp_tot_60_69 / tot_vacc_60_69
        inz_vacchosp_70_79 = 100000 * vacchosp_tot_70_79 / tot_vacc_70_79
        inz_vacchosp_80plus = 100000 * vacchosp_tot_80plus / tot_vacc_80plus

        inz_nonvacchosp_0_9 = 100000 * nonvacchosp_tot_0_9 / tot_nonvacc_0_9
        inz_nonvacchosp_10_19 = 100000 * nonvacchosp_tot_10_19 / tot_nonvacc_10_19
        inz_nonvacchosp_20_29 = 100000 * nonvacchosp_tot_20_29 / tot_nonvacc_20_29
        inz_nonvacchosp_30_39 = 100000 * nonvacchosp_tot_30_39 / tot_nonvacc_30_39
        inz_nonvacchosp_40_49 = 100000 * nonvacchosp_tot_40_49 / tot_nonvacc_40_49
        inz_nonvacchosp_50_59 = 100000 * nonvacchosp_tot_50_59 / tot_nonvacc_50_59
        inz_nonvacchosp_60_69 = 100000 * nonvacchosp_tot_60_69 / tot_nonvacc_60_69
        inz_nonvacchosp_70_79 = 100000 * nonvacchosp_tot_70_79 / tot_nonvacc_70_79
        inz_nonvacchosp_80plus = 100000 * nonvacchosp_tot_80plus / tot_nonvacc_80plus

        #Death ------------------------------------------------------------------------

        death_tot_0_9 = get_death_tot_by_agegroup("0 - 9",week,zf)
        death_tot_10_19 = get_death_tot_by_agegroup("10 - 19", week,zf)
        death_tot_20_29 = get_death_tot_by_agegroup("20 - 29", week,zf)
        death_tot_30_39 = get_death_tot_by_agegroup("30 - 39", week,zf)
        death_tot_40_49 = get_death_tot_by_agegroup("40 - 49", week,zf)
        death_tot_50_59 = get_death_tot_by_agegroup("50 - 59", week,zf)
        death_tot_60_69 = get_death_tot_by_agegroup("60 - 69", week,zf)
        death_tot_70_79 = get_death_tot_by_agegroup("70 - 79", week,zf)
        death_tot_80plus = get_death_tot_by_agegroup("80+", week,zf)

        vaccdeath_tot_0_9 = get_vaccdeath_tot_by_agegroup("0 - 9",week,zf)
        vaccdeath_tot_10_19 = get_vaccdeath_tot_by_agegroup("10 - 19", week,zf)
        vaccdeath_tot_20_29 = get_vaccdeath_tot_by_agegroup("20 - 29", week,zf)
        vaccdeath_tot_30_39 = get_vaccdeath_tot_by_agegroup("30 - 39", week,zf)
        vaccdeath_tot_40_49 = get_vaccdeath_tot_by_agegroup("40 - 49", week,zf)
        vaccdeath_tot_50_59 = get_vaccdeath_tot_by_agegroup("50 - 59", week,zf)
        vaccdeath_tot_60_69 = get_vaccdeath_tot_by_agegroup("60 - 69", week,zf)
        vaccdeath_tot_70_79 = get_vaccdeath_tot_by_agegroup("70 - 79", week,zf)
        vaccdeath_tot_80plus = get_vaccdeath_tot_by_agegroup("80+", week,zf)

        nonvaccdeath_tot_0_9 = death_tot_0_9 - vaccdeath_tot_0_9
        nonvaccdeath_tot_10_19 = death_tot_10_19 - vaccdeath_tot_10_19
        nonvaccdeath_tot_20_29 = death_tot_20_29 - vaccdeath_tot_20_29
        nonvaccdeath_tot_30_39 = death_tot_30_39 - vaccdeath_tot_30_39
        nonvaccdeath_tot_40_49 = death_tot_40_49 - vaccdeath_tot_40_49
        nonvaccdeath_tot_50_59 = death_tot_50_59 - vaccdeath_tot_50_59
        nonvaccdeath_tot_60_69 = death_tot_60_69 - vaccdeath_tot_60_69
        nonvaccdeath_tot_70_79 = death_tot_70_79 - vaccdeath_tot_70_79
        nonvaccdeath_tot_80plus = death_tot_80plus - vaccdeath_tot_80plus

        inz_vaccdeath_0_9 = 100000 * vaccdeath_tot_0_9 / tot_vacc_0_9
        inz_vaccdeath_10_19 = 100000 * vaccdeath_tot_10_19 / tot_vacc_10_19
        inz_vaccdeath_20_29 = 100000 * vaccdeath_tot_20_29 / tot_vacc_20_29
        inz_vaccdeath_30_39 = 100000 * vaccdeath_tot_30_39 / tot_vacc_30_39
        inz_vaccdeath_40_49 = 100000 * vaccdeath_tot_40_49 / tot_vacc_40_49
        inz_vaccdeath_50_59 = 100000 * vaccdeath_tot_50_59 / tot_vacc_50_59
        inz_vaccdeath_60_69 = 100000 * vaccdeath_tot_60_69 / tot_vacc_60_69
        inz_vaccdeath_70_79 = 100000 * vaccdeath_tot_70_79 / tot_vacc_70_79
        inz_vaccdeath_80plus = 100000 * vaccdeath_tot_80plus / tot_vacc_80plus

        inz_nonvaccdeath_0_9 = 100000 * nonvaccdeath_tot_0_9 / tot_nonvacc_0_9
        inz_nonvaccdeath_10_19 = 100000 * nonvaccdeath_tot_10_19 / tot_nonvacc_10_19
        inz_nonvaccdeath_20_29 = 100000 * nonvaccdeath_tot_20_29 / tot_nonvacc_20_29
        inz_nonvaccdeath_30_39 = 100000 * nonvaccdeath_tot_30_39 / tot_nonvacc_30_39
        inz_nonvaccdeath_40_49 = 100000 * nonvaccdeath_tot_40_49 / tot_nonvacc_40_49
        inz_nonvaccdeath_50_59 = 100000 * nonvaccdeath_tot_50_59 / tot_nonvacc_50_59
        inz_nonvaccdeath_60_69 = 100000 * nonvaccdeath_tot_60_69 / tot_nonvacc_60_69
        inz_nonvaccdeath_70_79 = 100000 * nonvaccdeath_tot_70_79 / tot_nonvacc_70_79
        inz_nonvaccdeath_80plus = 100000 * nonvaccdeath_tot_80plus / tot_nonvacc_80plus

    html = f'<html><head><meta charset="UTF-8" /><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.css"/><script src="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.js"></script>' \
           '<style>table, th, td { padding: 10px; font-size: 14; }' \
            '.columnl { float: left; width: 80px; } .columnr { float: left; width: 1400px; }/* Clear floats after the columns */ .row:after {   content: "";   display: table;   clear: both; }' \
            '#rotate-text { width: 45px; transform: rotate(90deg); }' \
    '.table td, .table th {'\
        'font-size: 30px;'\
    '}'\
            '</style>' \
           f'</head>' \
           '<body style="background-color: #edeeee;"><div style="margin-top: 20px;margin-bottom: 20px;">' \
           '<table style="margin-left: auto;margin-right: auto;">' \
           '<tr style="vertical-align: top;"><td>' \
           f'<h1>Fully vaccinated vs. Not fully vaccinated/Unvaccinated // Week {week - 4} to {week} // !!DRAFT!!</h1>' \
           f'<h2>28 day incidences per 100k</h2>' \
           '<h3>All data about the vaccinated cases, hosp. and deaths is still very LIMITED! Source: BAG/FOPH Switzerland</h3>' \
           '<table class="ui celled table" style="width: 1400px;table-layout:fixed">' \
           '<colgroup>' \
           '<col style="width: 100px;">' \
           '<col style="width: 20px">' \
           '<col style="width: 100px">' \
           '<col style="width: 100px">' \
           '<col style="width: 30px">' \
           '<col style="width: 100px">' \
           '<col style="width: 100px">' \
           '<col style="width: 30px">' \
           '<col style="width: 100px">' \
           '<col style="width: 100px">' \
           '</colgroup>' \
           '<tr><th>Age group</th>' \
           '<th></th>' \
           '<th class="right aligned">Vacc. Cases</th>' \
           '<th class="right aligned">Unvacc. Cases</th>' \
           '<th></th>' \
           '<th class="right aligned">Vacc. Hosp.</th>' \
           '<th class="right aligned">Unvacc. Hosp.</th>' \
           '<th></th>' \
           '<th class="right aligned">Vacc. Deaths</th>' \
           '<th class="right aligned">Unvacc. Deaths</th>' \
           '</tr>' \
           f'<tr><td>0-9</td><td></td><td class="right aligned">{"{:10.2f}".format(inz_vacccases_0_9)}</td><td class="right aligned">{"{:10.2f}".format(inz_nonvacccases_0_9)}</td><td></td><td class="right aligned">{"{:10.2f}".format(inz_vacchosp_0_9)}</td><td class="right aligned">{"{:10.2f}".format(inz_nonvacchosp_0_9)}</td><td></td><td class="right aligned">{"{:10.2f}".format(inz_vaccdeath_0_9)}</td><td class="right aligned">{"{:10.2f}".format(inz_nonvaccdeath_0_9)}</td></tr>' \
           f'<tr><td>10-19</td><td></td><td class="right aligned">{"{:10.2f}".format(inz_vacccases_10_19)}</td><td class="right aligned">{"{:10.2f}".format(inz_nonvacccases_10_19)}</td><td></td><td class="right aligned">{"{:10.2f}".format(inz_vacchosp_10_19)}</td><td class="right aligned">{"{:10.2f}".format(inz_nonvacchosp_10_19)}</td><td></td><td class="right aligned">{"{:10.2f}".format(inz_vaccdeath_10_19)}</td><td class="right aligned">{"{:10.2f}".format(inz_nonvaccdeath_10_19)}</td></tr>' \
           f'<tr><td>20-29</td><td></td><td class="right aligned">{"{:10.2f}".format(inz_vacccases_20_29)}</td><td class="right aligned">{"{:10.2f}".format(inz_nonvacccases_20_29)}</td><td></td><td class="right aligned">{"{:10.2f}".format(inz_vacchosp_20_29)}</td><td class="right aligned">{"{:10.2f}".format(inz_nonvacchosp_20_29)}</td><td></td><td class="right aligned">{"{:10.2f}".format(inz_vaccdeath_20_29)}</td><td class="right aligned">{"{:10.2f}".format(inz_nonvaccdeath_20_29)}</td></tr>' \
           f'<tr><td>30-39</td><td></td><td class="right aligned">{"{:10.2f}".format(inz_vacccases_30_39)}</td><td class="right aligned">{"{:10.2f}".format(inz_nonvacccases_30_39)}</td><td></td><td class="right aligned">{"{:10.2f}".format(inz_vacchosp_30_39)}</td><td class="right aligned">{"{:10.2f}".format(inz_nonvacchosp_30_39)}</td><td></td><td class="right aligned">{"{:10.2f}".format(inz_vaccdeath_30_39)}</td><td class="right aligned">{"{:10.2f}".format(inz_nonvaccdeath_30_39)}</td></tr>' \
           f'<tr><td>40-49</td><td></td><td class="right aligned">{"{:10.2f}".format(inz_vacccases_40_49)}</td><td class="right aligned">{"{:10.2f}".format(inz_nonvacccases_40_49)}</td><td></td><td class="right aligned">{"{:10.2f}".format(inz_vacchosp_40_49)}</td><td class="right aligned">{"{:10.2f}".format(inz_nonvacchosp_40_49)}</td><td></td><td class="right aligned">{"{:10.2f}".format(inz_vaccdeath_40_49)}</td><td class="right aligned">{"{:10.2f}".format(inz_nonvaccdeath_40_49)}</td></tr>' \
           f'<tr><td>50-59</td><td></td><td class="right aligned">{"{:10.2f}".format(inz_vacccases_50_59)}</td><td class="right aligned">{"{:10.2f}".format(inz_nonvacccases_50_59)}</td><td></td><td class="right aligned">{"{:10.2f}".format(inz_vacchosp_50_59)}</td><td class="right aligned">{"{:10.2f}".format(inz_nonvacchosp_50_59)}</td><td></td><td class="right aligned">{"{:10.2f}".format(inz_vaccdeath_50_59)}</td><td class="right aligned">{"{:10.2f}".format(inz_nonvaccdeath_50_59)}</td></tr>' \
           f'<tr><td>60-69</td><td></td><td class="right aligned">{"{:10.2f}".format(inz_vacccases_60_69)}</td><td class="right aligned">{"{:10.2f}".format(inz_nonvacccases_60_69)}</td><td></td><td class="right aligned">{"{:10.2f}".format(inz_vacchosp_60_69)}</td><td class="right aligned">{"{:10.2f}".format(inz_nonvacchosp_60_69)}</td><td></td><td class="right aligned">{"{:10.2f}".format(inz_vaccdeath_60_69)}</td><td class="right aligned">{"{:10.2f}".format(inz_nonvaccdeath_60_69)}</td></tr>' \
           f'<tr><td>70-79</td><td></td><td class="right aligned">{"{:10.2f}".format(inz_vacccases_70_79)}</td><td class="right aligned">{"{:10.2f}".format(inz_nonvacccases_70_79)}</td><td></td><td class="right aligned">{"{:10.2f}".format(inz_vacchosp_70_79)}</td><td class="right aligned">{"{:10.2f}".format(inz_nonvacchosp_70_79)}</td><td></td><td class="right aligned">{"{:10.2f}".format(inz_vaccdeath_70_79)}</td><td class="right aligned">{"{:10.2f}".format(inz_nonvaccdeath_70_79)}</td></tr>' \
           f'<tr><td>80+</td><td></td><td class="right aligned">{"{:10.2f}".format(inz_vacccases_80plus)}</td><td class="right aligned">{"{:10.2f}".format(inz_nonvacccases_80plus)}</td><td></td><td class="right aligned">{"{:10.2f}".format(inz_vacchosp_80plus)}</td><td class="right aligned">{"{:10.2f}".format(inz_nonvacchosp_80plus)}</td><td></td><td class="right aligned">{"{:10.2f}".format(inz_vaccdeath_80plus)}</td><td class="right aligned">{"{:10.2f}".format(inz_nonvaccdeath_80plus)}</td></tr>' \


    html += f'</table><h3>Web: covidlaws.net // Twitter: @CovidLawsStats</h3></td></tr></table> </body></html>'

    print(html)

    options = {'width': '1500', 'height': '1200', 'encoding': "UTF-8", }
    imgkit.from_string(html, "out_image.jpg", options=options)

