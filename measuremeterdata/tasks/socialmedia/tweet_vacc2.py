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

def tweet(week, geo):
    create_image(week, geo)

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
    bot.sendMessage(settings.TELEGRAM_CHATID, f'Vollständig Geimpfte vs. Unvollständig Geimpfte/Ungeimpfte\nStand: Woche {week} \n7-Tage-Inzidenzen Fälle/Hospitalisierte/Tote\nDaten sind im BAG-File als "intermediate" markiert.\nGeimpfte vs. Ungeimpfte')
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
    status_gen = {week}

    api.update_status(
        status = f'Vollständig Geimpfte vs. Unvollständig Geimpfte/Ungeimpfte\nWoche {status_gen}\nInzidenzen Fälle/Hospitalisierte/Tote\nDaten sind im BAG-File als "intermediate" markiert!',
        media_ids=[media.media_id_string])




def get_vacced_by_agegroup(filename, age_group, date_week, zf, geo):
        df_tot_vacc = pd.read_csv(zf.open(f'data/{filename}'), error_bad_lines=False)

        rslt_df = df_tot_vacc[(df_tot_vacc['geoRegion'] == geo) &
                            (df_tot_vacc['altersklasse_covid19'] == age_group) &
                             (df_tot_vacc['date'] == date_week) &
                            (df_tot_vacc['vaccination_status'] == "fully_vaccinated") ]

        return rslt_df['pop'].item()


def get_unvacced_by_agegroup(filename, age_group, date_week, zf, geo):
    tot = 0

    df_tot_vacc = pd.read_csv(zf.open(f'data/{filename}'), error_bad_lines=False)

    rslt_df = df_tot_vacc[(df_tot_vacc['geoRegion'] == geo) &
                          (df_tot_vacc['altersklasse_covid19'] == age_group) &
                          (df_tot_vacc['date'] == date_week) &
                          (df_tot_vacc['vaccination_status'] == "not_vaccinated")]

    tot += rslt_df['pop'].item()

    rslt_df = df_tot_vacc[(df_tot_vacc['geoRegion'] == geo) &
                          (df_tot_vacc['altersklasse_covid19'] == age_group) &
                          (df_tot_vacc['date'] == date_week) &
                          (df_tot_vacc['vaccination_status'] == "partially_vaccinated")]

    tot += rslt_df['pop'].item()

    return tot

def get_numbers_tot_by_agegroup(filename, date_str, age_group, week_from, week_to, zf, geo, is_vacc_file):
    df_tot_vacc = pd.read_csv(zf.open(f'data/{filename}'), error_bad_lines=False)

    tot = 0

    for x in range(week_from, (week_to + 1)):
        date_week = (202100 +  x)

        if is_vacc_file:
            rslt_df = df_tot_vacc[(df_tot_vacc['geoRegion'] == geo) &
                                  (df_tot_vacc['altersklasse_covid19'] == age_group) &
                                  (df_tot_vacc[date_str] == date_week) &
                                  (df_tot_vacc['vaccination_status'] == 'fully_vaccinated') ]
        else:
            rslt_df = df_tot_vacc[(df_tot_vacc['geoRegion'] == geo) &
                                  (df_tot_vacc['altersklasse_covid19'] == age_group) &
                                  (df_tot_vacc[date_str] == date_week)]

        tot += rslt_df['entries'].item()

    return tot


def get_vals_by_agegroup(filename, date_str, age_group, date_week, zf, geo):
    try:
        df_tot_vacc = pd.read_csv(zf.open(f'data/{filename}'), error_bad_lines=False)

        rslt_df = df_tot_vacc[(df_tot_vacc['geoRegion'] == geo) &
                              (df_tot_vacc['altersklasse_covid19'] == age_group) &
                              (df_tot_vacc[date_str] == date_week) &
                              (df_tot_vacc['vaccination_status'] == 'fully_vaccinated')]

        cases_vacc = rslt_df['entries'].item()
        total_vacc = rslt_df['pop'].item()

        cases_unvacc = 0
        total_unvacc = 0

        rslt_df = df_tot_vacc[(df_tot_vacc['geoRegion'] == geo) &
                              (df_tot_vacc['altersklasse_covid19'] == age_group) &
                              (df_tot_vacc[date_str] == date_week) &
                              (df_tot_vacc['vaccination_status'] == 'not_vaccinated')]

        cases_unvacc += rslt_df['entries'].item()
        total_unvacc += rslt_df['pop'].item()

        rslt_df = df_tot_vacc[(df_tot_vacc['geoRegion'] == geo) &
                              (df_tot_vacc['altersklasse_covid19'] == age_group) &
                              (df_tot_vacc[date_str] == date_week) &
                              (df_tot_vacc['vaccination_status'] == 'partially_vaccinated')]

        cases_unvacc += rslt_df['entries'].item()
        total_unvacc += rslt_df['pop'].item()

        rslt_df = df_tot_vacc[(df_tot_vacc['geoRegion'] == geo) &
                              (df_tot_vacc['altersklasse_covid19'] == age_group) &
                              (df_tot_vacc[date_str] == date_week) &
                              (df_tot_vacc['vaccination_status'] == 'unknown')]

        cases_unknown = rslt_df['entries'].item()

        return cases_vacc, total_vacc, cases_unvacc, total_unvacc, cases_unknown
    except:
        return None, None, None, None, None


def calc_week(week, geo, age_categories):
    date_week = 202100 + week

    response = {}

    with urllib.request.urlopen("https://www.covid19.admin.ch/api/data/context") as url:
        data = json.loads(url.read().decode())

        resp = urlopen(
            data['sources']['zip']['csv'])

        zf = zipfile.ZipFile(BytesIO(resp.read()), 'r')

        #Cases ------------------------------------------------------------------------
        cases_vacc = {}
        tot_vacc = {}
        cases_unvacc = {}
        tot_nonvacc = {}
        inz_vacccases = {}
        inz_nonvacccases = {}
        cases_unknown = {}

        for ac in age_categories:
            cases_vacc[ac], tot_vacc[ac], cases_unvacc[ac], tot_nonvacc[ac], cases_unknown[ac] = get_vals_by_agegroup("COVID19Cases_vaccpersons_AKL10_w.csv", "date", ac, date_week ,zf, geo)

        if (cases_vacc["all"]):
            for ac in age_categories:
                inz_vacccases[ac] = 100000 * cases_vacc[ac] / tot_vacc[ac]
                inz_nonvacccases[ac] = 100000 * cases_unvacc[ac] / tot_nonvacc[ac]

            rel_cases = {}
            rel_cases_str = {}
            for ac in age_categories:
                rel_cases[ac] = None
                try:
                    rel_cases[ac] = inz_nonvacccases[ac] / inz_vacccases[ac]
                except:
                    pass
                if rel_cases[ac]:
                    rel_cases_str[ac] = "{0:.0f}".format(rel_cases[ac]) + "x"
                else:
                    rel_cases_str[ac] = "-"

            try:
                rel_cases_alle = inz_nonvacccases_alle / inz_vacccases_alle
            except:
                rel_cases_alle = None
                pass
            if rel_cases_alle:
                rel_cases_alle_str = "{0:.0f}".format(rel_cases_alle) + "x"
            else:
                rel_cases_alle_str = "-"
        else:
            rel_cases_str = {}

            for ac in age_categories:
                inz_vacccases[ac] = 0
                inz_nonvacccases[ac] = 0
                rel_cases_str[ac] = "-"
        #Hosp ------------------------------------------------------------------------
        hosp_vacc = {}
        tot_vacc = {}
        hosp_unvacc = {}
        tot_nonvacc = {}
        inz_vacchosp = {}
        inz_nonvacchosp = {}
        hosp_unknown = {}

        for ac in age_categories:
            hosp_vacc[ac], tot_vacc[ac], hosp_unvacc[ac], tot_nonvacc[ac], hosp_unknown[ac] = get_vals_by_agegroup(
                "COVID19Hosp_vaccpersons_AKL10_w.csv", "date", ac, date_week, zf, geo)

        for ac in age_categories:
            inz_vacchosp[ac] = 100000 * hosp_vacc[ac] / tot_vacc[ac]
            inz_nonvacchosp[ac] = 100000 * hosp_unvacc[ac] / tot_nonvacc[ac]

        rel_hosp = {}
        eff_hosp = {}
        rel_hosp_str = {}
        eff_hosp_str = {}
        for ac in age_categories:
            rel_hosp[ac] = None
            eff_hosp[ac] = None
            try:
                rel_hosp[ac] = inz_nonvacchosp[ac] / inz_vacchosp[ac]
                eff_hosp[ac] = (inz_nonvacchosp[ac] - inz_vacchosp[ac]) / inz_nonvacchosp[ac] * 100
            except:
                pass
            if rel_hosp[ac]:
                rel_hosp_str[ac] = "{0:.0f}".format(rel_hosp[ac]) + "x"
                eff_hosp_str[ac] = "{0:.1f}".format(eff_hosp[ac]) + "%"
            else:
                rel_hosp_str[ac] = "-"
                eff_hosp_str[ac] = "-"

        rel_hosp_alle = None
        try:
            rel_hosp_alle = inz_nonvacchosp_alle / inz_vacchosp_alle
            eff_hosp_alle = (inz_nonvacchosp_alle - inz_vacchosp_alle) / inz_nonvacchosp_alle * 100
        except:
            pass
        if rel_hosp_alle:
            rel_hosp_alle_str = "{0:.0f}".format(rel_hosp_alle) + "x"
            eff_hosp_alle_str = "{0:.1f}".format(eff_hosp_alle) + "%"
        else:
            rel_hosp_alle_str = "-"
            eff_hosp_alle_str = "-"

        #Death ------------------------------------------------------------------------
        death_vacc = {}
        tot_vacc = {}
        death_nonvacc = {}
        tot_nonvacc = {}
        inz_vaccdeath = {}
        inz_nonvaccdeath = {}
        death_unknown = {}

        for ac in age_categories:
            death_vacc[ac], tot_vacc[ac], death_nonvacc[ac], tot_nonvacc[ac], death_unknown[ac] = get_vals_by_agegroup(
                "COVID19Death_vaccpersons_AKL10_w.csv", "date", ac, date_week, zf, geo)

        for ac in age_categories:
            inz_vaccdeath[ac] = 100000 * death_vacc[ac] / tot_vacc[ac]
            inz_nonvaccdeath[ac] = 100000 * death_nonvacc[ac] / tot_nonvacc[ac]

        rel_death = {}
        eff_death = {}
        rel_death_str = {}
        eff_death_str = {}
        for ac in age_categories:
            rel_death[ac] = None
            eff_death[ac] = None
            try:
                rel_death[ac] = inz_nonvaccdeath[ac] / inz_vaccdeath[ac]
                eff_death[ac] = (inz_nonvaccdeath[ac] - inz_vaccdeath[ac]) / inz_nonvaccdeath[ac] * 100
            except:
                pass
            if rel_death[ac]:
                rel_death_str[ac] = "{0:.0f}".format(rel_death[ac]) + "x"
                eff_death_str[ac] = "{0:.1f}".format(eff_death[ac]) + "%"
            else:
                rel_death_str[ac] = "-"
                eff_death_str[ac] = "-"

        rel_death_alle = None
        try:
            rel_death_alle = inz_nonvaccdeath_alle / inz_vaccdeath_alle
            eff_death_alle = (inz_nonvaccdeath_alle - inz_vaccdeath_alle) / inz_nonvaccdeath_alle * 100
        except:
            pass
        if rel_death_alle:
            rel_death_alle_str = "{0:.0f}".format(rel_death_alle) + "x"
            eff_death_alle_str = "{0:.1f}".format(eff_death_alle) + "%"
        else:
            rel_death_alle_str = "-"
            eff_death_alle_str = "-"


    response["tot_vacc"] = tot_vacc
    response["tot_nonvacc"] = tot_nonvacc
    response["cases_vacc"] = cases_vacc
    response["cases_unvacc"] = cases_unvacc
    response["inz_vacccases"] = inz_vacccases
    response["inz_nonvacccases"] = inz_nonvacccases
    response["rel_cases_str"] = rel_cases_str
    response["hosp_vacc"] = hosp_vacc
    response["hosp_unvacc"] = hosp_unvacc
    response["inz_vacchosp"] = inz_vacchosp
    response["inz_nonvacchosp"] = inz_nonvacchosp
    response["rel_hosp_str"] = rel_hosp_str
    response["eff_hosp_str"] = eff_hosp_str
    response["death_vacc"] = death_vacc
    response["death_nonvacc"] = death_nonvacc
    response["inz_vaccdeath"] = inz_vaccdeath
    response["inz_nonvaccdeath"] = inz_nonvaccdeath
    response["rel_death_str"] = rel_death_str
    response["eff_death_str"] = eff_death_str
    response["cases_unknown"] = cases_unknown
    response["hosp_unknown"] = hosp_unknown
    response["death_unknown"] = death_unknown

    return response

def create_csv(week, geo, age_categories):
    print("CSV:")
    print("Week;Category;Age Group;Vacc Num;Unvacc Num;Unknown Num;Vacc Incidence;Unvacc Incidence;Ratio;Eff")
    for week_to_load in range (30, (week+1)):
        response = calc_week(week_to_load, geo, age_categories)

        for ac in age_categories:
            print(f"{week_to_load};Cases;{ac};{response['cases_vacc'][ac]};{response['cases_unvacc'][ac]};{response['cases_unknown'][ac]};{response['inz_vacccases'][ac]};{response['inz_nonvacccases'][ac]};{response['rel_cases_str'][ac]};;")
            print(f"{week_to_load};Hosp;{ac};{response['hosp_vacc'][ac]};{response['hosp_unvacc'][ac]};{response['hosp_unknown'][ac]};{response['inz_vacchosp'][ac]};{response['inz_nonvacchosp'][ac]};{response['rel_hosp_str'][ac]};{response['eff_hosp_str'][ac]};")
            print(f"{week_to_load};Death;{ac};{response['death_vacc'][ac]};{response['death_nonvacc'][ac]};{response['death_unknown'][ac]};{response['inz_vaccdeath'][ac]};{response['inz_nonvaccdeath'][ac]};{response['rel_death_str'][ac]};{response['eff_hosp_str'][ac]};")


    print("--------------------------------")
def create_image(week, geo):
    age_categories = ["0 - 9","10 - 19","20 - 29","30 - 39","40 - 49","50 - 59","60 - 69","70 - 79","80+","all"]

    #create_csv(week, geo, age_categories)

    response = calc_week(week, geo, age_categories)
    print(response)

    html = f'<html><head><meta charset="UTF-8" /><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.css"/><script src="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.js"></script>' \
           '<style>table, th, td { padding: 10px; font-size: 14; }' \
            '.columnl { float: left; width: 80px; } .columnr { float: left; width: 1600px; }/* Clear floats after the columns */ .row:after {   content: "";   display: table;   clear: both; }' \
            '#rotate-text { width: 45px; transform: rotate(90deg); }' \
    '.table td, .table th {'\
        'font-size: 30px;'\
    '}'\
            '</style>' \
           f'</head>' \
           '<body style="background-color: #edeeee;"><div style="margin-top: 20px;margin-bottom: 20px;">' \
           '<table style="margin-left: auto;margin-right: auto;">' \
           '<tr style="vertical-align: top;"><td>'
    html += f'<h1>Vollständig Geimpfte vs. Unvollständig/nicht Geimpfte // Woche {week} // V3</h1>'\
    '<h1>Hospitalisierungen und Todesfälle</h1><br>'\
    '<pre>'\
    '                                           <img src="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/282/hospital_1f3e5.png" width="70">'\
    '                                                   <img src="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/282/hospital_1f3e5.png" width="70">'\
    '                                                        <img src="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/282/coffin_26b0-fe0f.png" width="70">'\
    '</pre>'\
    '<table class="ui celled table striped" style="width: 1700px;table-layout:fixed">' \
           '<colgroup>' \
           '<col style="width: 80px;">' \
           '<col style="width: 10px">' \
           '<col style="width: 60px">' \
           '<col style="width: 60px">' \
           '<col style="width: 50px">' \
           '<col style="width: 10px">' \
           '<col style="width: 60px">' \
           '<col style="width: 60px">' \
           '<col style="width: 50px">' \
           '<col style="width: 60px">' \
           '<col style="width: 10px">' \
           '<col style="width: 60px">' \
           '<col style="width: 60px">' \
           '<col style="width: 50px">' \
           '<col style="width: 60px">' \
           '</colgroup>' \
           '<tr><th>Alters- gruppe</th>' \
           '<th  style="background-color:#edefee;"></th>' \
           '<th>Fälle <img src="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/282/syringe_1f489.png" width="50"><img src="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/282/syringe_1f489.png" width="50"></th>' \
           '<th>Fälle <img src="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/282/syringe_1f489.png" width="50"><img src="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/282/woman-gesturing-no_1f645-200d-2640-fe0f.png" width="50"></th>' \
            '<th>Fälle <img src="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/282/question-mark_2753.png" width="50"></th>' \
               '<th style="background-color:#edefee;"></th>' \
               '<th class="right aligned">Inzidenz <img src="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/282/syringe_1f489.png" width="50"><img src="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/282/syringe_1f489.png" width="50"></th>' \
           '<th class="right aligned">Inzidenz <img src="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/282/syringe_1f489.png" width="50"><img src="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/282/woman-gesturing-no_1f645-200d-2640-fe0f.png" width="50"></th>' \
           '<th class="right aligned">Rate</th>' \
           '<th class="right aligned">Effekt.</th>' \
           '<th style="background-color:#edefee;"></th>' \
           '<th class="right aligned">Inzidenz <img src="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/282/syringe_1f489.png" width="50"><img src="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/282/syringe_1f489.png" width="50"></th>' \
           '<th class="right aligned">Inzidenz <img src="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/282/syringe_1f489.png" width="50"><img src="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/282/woman-gesturing-no_1f645-200d-2640-fe0f.png" width="50"></th>' \
           '<th class="right aligned">Rate</th>' \
           '<th class="right aligned">Effekt.</th>' \
           '</tr>'

    for ac in age_categories:
        html += f'<tr><td>{ac}</td><td style="background-color:#edefee;"></td>' \
                f'<td class="right aligned">{response["hosp_vacc"][ac]}</td>' \
                f'<td class="right aligned">{response["hosp_unvacc"][ac]}</td>' \
                f'<td class="right aligned">{response["hosp_unknown"][ac]}</td>' \
                f'<td style="background-color:#edefee;"></td>'\
                f'<td class="right aligned">{"{:10.1f}".format(response["inz_vacchosp"][ac])}</td>' \
                f'<td class="right aligned">{"{:10.1f}".format(response["inz_nonvacchosp"][ac])}</td>' \
                f'<td class="right aligned">{response["rel_hosp_str"][ac]}</td>' \
                f'<td class="right aligned">{response["eff_hosp_str"][ac]}</td>' \
                f'<td style="background-color:#edefee;"></td>' \
                f'<td class="right aligned">{"{:10.1f}".format(response["inz_vaccdeath"][ac])}</td>' \
                f'<td class="right aligned">{"{:10.1f}".format(response["inz_nonvaccdeath"][ac])}</td>' \
                f'<td class="right aligned">{response["rel_death_str"][ac]}</td><td>{response["eff_death_str"][ac]}</td>' \
                f'</tr>'

    html += f'</table>'
    html +=    '<p style="font-size:25px;">'\
            '<img src="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/282/syringe_1f489.png" width="30"><img src="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/282/syringe_1f489.png" width="30"> = Vollständig geimpft' \
               ' // <img src="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/282/syringe_1f489.png" width="30"><img src="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/282/woman-gesturing-no_1f645-200d-2640-fe0f.png" width="30"> = Noch nicht vollständig geimpft und ungeimpft' \
             ' // <img src="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/282/question-mark_2753.png" width="30"> = Status unbekannt'\
            '</p>'\
            f'<h3>Web: covidlaws.net // Twitter: @CovidLawsStats // Quelle: BAG Schweiz, Status Daten: Intermediate</h3></td></tr></table> </body></html>'

    options = {'width': '1750', 'height': '1350', 'encoding': "UTF-8", }
    imgkit.from_string(html, "/tmp/out_image.jpg", options=options)

