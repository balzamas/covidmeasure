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

def tweet(weekfrom, weekto, weekvacc, geo):
    create_image(weekfrom, weekto, weekvacc, geo)

#    page_access_token = settings.FACEBOOK_ACCESS_TOKEN
#    graph = facebook.GraphAPI(page_access_token)
#    facebook_page_id = settings.FACEBOOK_PAGE_ID
#    graph.put_object(facebook_page_id, "feed", message='test message')

    send_telegram(weekfrom, weekto)
    send_tweet(weekfrom, weekto)

def send_telegram(weekfrom, weekto):
    #Telegram

    bot = telepot.Bot(settings.TELEGRAM_TOKEN)
    print(bot.getMe())
    bot.sendMessage(settings.TELEGRAM_CHATID, f'Vollständig Geimpfte vs. Unvollständig Geimpfte/Ungeimpfte\nStand: Woche {weekfrom} bis {weekto}\n28-Tage-Inzidenzen Fälle/Hospitalisierte/Tote\nDaten sind im BAG-File als "limited" markiert, d.h. noch sehr inkomplett.\nDie Tabelle dient als Demo bis die Zahlen zuverlässiger werden.Geimpfte vs. Ungeimpfte')
    bot.sendPhoto(settings.TELEGRAM_CHATID, photo=open("/tmp/out_image.jpg", 'rb'))



def send_tweet(weekfrom, weekto):
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
    if weekto == weekfrom:
        status_gen = {weekto}
    else:
        status_gen = f'{weekfrom} bis {weekto}'

    api.update_status(
        status = f'Vollständig Geimpfte vs. Unvollständig Geimpfte/Ungeimpfte\nWoche {status_gen}\nInzidenzen Fälle/Hospitalisierte/Tote\nDaten sind im BAG-File als "limited" markiert!\nDie Tabelle dient als Demo bis die Zahlen zuverlässiger werden.',
        media_ids=[media.media_id_string])




def get_vacced_by_agegroup(age_group, date_week, zf, geo):
        df_tot_vacc = pd.read_csv(zf.open('data/COVID19VaccPersons_AKL10_w_v2.csv'), error_bad_lines=False)

        rslt_df = df_tot_vacc[(df_tot_vacc['geoRegion'] == geo) &
                            (df_tot_vacc['altersklasse_covid19'] == age_group) &
                             (df_tot_vacc['date'] == date_week) &
                            (df_tot_vacc['type'] == "COVID19FullyVaccPersons") ]

        return rslt_df['sumTotal'].item()


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

def create_image(weekfrom, weekto, weekvacc, geo):
    date_week_to = 202100 + weekto
    date_week_from = 202100 + weekfrom
    date_week_vacc = 202100 + weekvacc

    age_categories = ["0 - 9","10 - 19","20 - 29","30 - 39","40 - 49","50 - 59","60 - 69","70 - 79","80+"]

    pop = {}
    pop_alle = 0
    pop["0 - 9"] = 873043
    pop["10 - 19"] = 844155
    pop["20 - 29"] = 1045350
    pop["30 - 39"] = 1229176
    pop["40 - 49"] = 1198325
    pop["50 - 59"] = 1292837
    pop["60 - 69"] = 947959
    pop["70 - 79"] = 721518
    pop["80+"] = 453670

    for ac in age_categories:
        pop_alle += pop[ac]

    with urllib.request.urlopen("https://www.covid19.admin.ch/api/data/context") as url:
        data = json.loads(url.read().decode())

        resp = urlopen(
            data['sources']['zip']['csv'])

        zf = zipfile.ZipFile(BytesIO(resp.read()), 'r')

        tot_vacc = {}
        tot_vacc_alle = 0
        for ac in age_categories:
            tot_vacc[ac] = get_vacced_by_agegroup(ac, date_week_vacc, zf, geo)
            tot_vacc_alle += tot_vacc[ac]

        tot_nonvacc = {}
        tot_nonvacc_alle = 0
        for ac in age_categories:
            tot_nonvacc[ac] = pop[ac] - tot_vacc[ac]
            tot_nonvacc_alle += tot_nonvacc[ac]

        #Cases ------------------------------------------------------------------------

        cases_tot = {}
        cases_tot_alle = 0
        for ac in age_categories:
            cases_tot[ac] = get_numbers_tot_by_agegroup("COVID19Cases_geoRegion_AKL10_w.csv", "datum", ac, weekfrom, weekto ,zf, geo, False)
            cases_tot_alle += cases_tot[ac]

        vacccases_tot = {}
        vacccases_tot_alle = 0
        for ac in age_categories:
            vacccases_tot[ac] = get_numbers_tot_by_agegroup("COVID19Cases_vaccpersons_AKL10_w.csv", "date", ac, weekfrom, weekto, zf, geo, True)
            vacccases_tot_alle += vacccases_tot[ac]

        nonvacccases_tot = {}
        nonvacccases_tot_alle = 0
        for ac in age_categories:
            nonvacccases_tot[ac] = cases_tot[ac] - vacccases_tot[ac]
            nonvacccases_tot_alle += nonvacccases_tot[ac]

        inz_vacccases = {}
        for ac in age_categories:
            inz_vacccases[ac] = 100000 * vacccases_tot[ac] / tot_vacc[ac]
        inz_vacccases_alle = 100000 * vacccases_tot_alle / tot_vacc_alle

        inz_nonvacccases = {}
        for ac in age_categories:
            inz_nonvacccases[ac] = 100000 * nonvacccases_tot[ac] / tot_nonvacc[ac]
        inz_nonvacccases_alle = 100000 * nonvacccases_tot_alle / tot_nonvacc_alle

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

        #Hosp ------------------------------------------------------------------------

        hosp_tot = {}
        hosp_tot_alle = 0
        for ac in age_categories:
            hosp_tot[ac] = get_numbers_tot_by_agegroup("COVID19Hosp_geoRegion_AKL10_w.csv", "datum", ac, weekfrom, weekto, zf, geo, False)
            hosp_tot_alle += hosp_tot[ac]

        vacchosp_tot = {}
        vacchosp_tot_alle = 0
        for ac in age_categories:
            vacchosp_tot[ac] = get_numbers_tot_by_agegroup("COVID19Hosp_vaccpersons_AKL10_w.csv", "date", ac, weekfrom, weekto, zf, geo, True)
            vacchosp_tot_alle += vacchosp_tot[ac]

        nonvacchosp_tot = {}
        nonvacchosp_tot_alle = 0
        for ac in age_categories:
            nonvacchosp_tot[ac] = hosp_tot[ac] - vacchosp_tot[ac]
            nonvacchosp_tot_alle += nonvacchosp_tot[ac]

        inz_vacchosp = {}
        for ac in age_categories:
            inz_vacchosp[ac] = 100000 * vacchosp_tot[ac] / tot_vacc[ac]
        inz_vacchosp_alle = 100000 * vacchosp_tot_alle / tot_vacc_alle

        inz_nonvacchosp = {}
        for ac in age_categories:
            inz_nonvacchosp[ac] = 100000 * nonvacchosp_tot[ac] / tot_nonvacc[ac]

        inz_nonvacchosp_alle = 100000 * nonvacchosp_tot_alle / tot_nonvacc_alle

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

        death_tot = {}
        death_tot_alle = 0
        for ac in age_categories:
            death_tot[ac] = get_numbers_tot_by_agegroup("COVID19Death_geoRegion_AKL10_w.csv", "datum", ac, weekfrom, weekto, zf, geo, False)
            death_tot_alle += death_tot[ac]

        vaccdeath_tot = {}
        vaccdeath_tot_alle = 0
        for ac in age_categories:
            vaccdeath_tot[ac] = get_numbers_tot_by_agegroup("COVID19Death_vaccpersons_AKL10_w.csv", "date", ac, weekfrom, weekto, zf, geo, True)
            vaccdeath_tot_alle += vaccdeath_tot[ac]

        nonvaccdeath_tot = {}
        nonvaccdeath_tot_alle = 0
        for ac in age_categories:
           nonvaccdeath_tot[ac] = death_tot[ac] - vaccdeath_tot[ac]
           nonvaccdeath_tot_alle += nonvaccdeath_tot[ac]

        inz_vaccdeath = {}
        for ac in age_categories:
           inz_vaccdeath[ac] = 100000 * vaccdeath_tot[ac] / tot_vacc[ac]

        inz_vaccdeath_alle = 100000 * vaccdeath_tot_alle / tot_vacc_alle

        inz_nonvaccdeath = {}
        for ac in age_categories:
            inz_nonvaccdeath[ac] = 100000 * nonvaccdeath_tot[ac] / tot_nonvacc[ac]
        inz_nonvaccdeath_alle = 100000 * nonvaccdeath_tot_alle / tot_nonvacc_alle

        rel_death = {}
        rel_death_str = {}
        eff_death = {}
        eff_death_str = {}
        for ac in age_categories:
            rel_death[ac] = None
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

        print("CSV:")
        print(f"Week {weekfrom} to {weekto}")
        print(f"Numbers: Incidence 24 days per 100k")
        print("Age Group;Vacc ppl;Unvacc ppl;Perc. Vacc;Vacc Cases;Unvacc Cases;Ratio Cases;Vacc Hosp.;Unvacc Hosp; Ratio Hosp;Eff Hosp;Vacc Death;Unvacc Death;Ratio Death; Eff Death")
        for ac in age_categories:
            print(f"{ac};{tot_vacc[ac]};{tot_nonvacc[ac]};{tot_vacc[ac] * 100 / pop[ac]};{inz_vacccases[ac]};{inz_nonvacccases[ac]};{rel_cases_str[ac]};{inz_vacchosp[ac]};{inz_nonvacchosp[ac]};{rel_hosp_str[ac]};{eff_hosp_str[ac]};{inz_vaccdeath[ac]};{inz_nonvaccdeath[ac]};{rel_death_str[ac]};{eff_death_str[ac]}")
        print(f"Alle;{tot_vacc_alle};{tot_nonvacc_alle};{tot_vacc_alle * 100 / pop_alle};{inz_vacccases_alle};{inz_nonvacccases_alle};{rel_cases_alle_str};{inz_vacchosp_alle};{inz_nonvacchosp_alle};{rel_hosp_alle_str};{eff_hosp_alle_str};{inz_vaccdeath_alle};{inz_nonvaccdeath_alle};{rel_death_alle_str};{eff_death_alle_str}")

        print("--------------------------------")

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
    if weekfrom == weekto:
        html += f'<h1>Vollständig Geimpfte vs. Unvollständig/nicht Geimpfte // Woche {weekto} // V2</h1>'
    else:
        html += f'<h1>Vollständig Geimpfte vs. Unvollständig/nicht Geimpfte // Woche {weekfrom} bis {weekto} // V2</h1>'

    html +=    f'<h2>Inzidenz auf 100k</h2>' \
           '<h3>Die Daten für die geimpften Fälle/Hospitalisierungen/Todesfälle sind noch stark LIMITIERT (Stufe:intermediate)! Quelle: BAG Schweiz</h3>' \
           f'<h3>Die Anzahl vollständig geimpfter Personen bezieht sich auf Woche {weekvacc}.</h3>' \
           '<table class="ui celled table striped" style="width: 1700px;table-layout:fixed">' \
           '<colgroup>' \
           '<col style="width: 80px;">' \
           '<col style="width: 10px">' \
           '<col style="width: 60px">' \
           '<col style="width: 80px">' \
           '<col style="width: 50px">' \
           '<col style="width: 10px">' \
           '<col style="width: 60px">' \
           '<col style="width: 80px">' \
           '<col style="width: 50px">' \
           '<col style="width: 60px">' \
           '<col style="width: 10px">' \
           '<col style="width: 60px">' \
           '<col style="width: 80px">' \
           '<col style="width: 50px">' \
           '<col style="width: 60px">' \
           '</colgroup>' \
           '<tr><th>Alters- gruppe</th>' \
           '<th  style="background-color:#edefee;"></th>' \
           '<th class="right aligned">Geimp. Fälle</th>' \
           '<th class="right aligned">Ungeimp. Fälle</th>' \
           '<th class="right aligned">Rate</th>' \
           '<th style="background-color:#edefee;"></th>' \
           '<th class="right aligned">Geimp. Hosp.</th>' \
           '<th class="right aligned">Ungeimp. Hosp.</th>' \
           '<th class="right aligned">Rate</th>' \
           '<th class="right aligned">Effekt.</th>' \
           '<th style="background-color:#edefee;"></th>' \
           '<th class="right aligned">Geimpt. Tote</th>' \
           '<th class="right aligned">Ungeimp. Tote</th>' \
           '<th class="right aligned">Rate</th>' \
           '<th class="right aligned">Effekt.</th>' \
           '</tr>'

    for ac in age_categories:
        html += f'<tr><td>{ac}</td><td style="background-color:#edefee;"></td><td class="right aligned">{"{:10.1f}".format(inz_vacccases[ac])}</td><td class="right aligned">{"{:10.1f}".format(inz_nonvacccases[ac])}</td><td class="right aligned">{rel_cases_str[ac]}</td><td style="background-color:#edefee;"></td><td class="right aligned">{"{:10.1f}".format(inz_vacchosp[ac])}</td><td class="right aligned">{"{:10.1f}".format(inz_nonvacchosp[ac])}</td><td>{rel_hosp_str[ac]}</td><td>{eff_hosp_str[ac]}</td><td style="background-color:#edefee;"></td><td class="right aligned">{"{:10.1f}".format(inz_vaccdeath[ac])}</td><td class="right aligned">{"{:10.1f}".format(inz_nonvaccdeath[ac])}</td><td>{rel_death_str[ac]}</td><td>{eff_death_str[ac]}</td></tr>'
    html += f'<tr><td>Alle</td><td style="background-color:#edefee;"></td><td class="right aligned">{"{:10.1f}".format(inz_vacccases_alle)}</td><td class="right aligned">{"{:10.1f}".format(inz_nonvacccases_alle)}</td><td class="right aligned">{rel_cases_alle_str}</td><td style="background-color:#edefee;"></td><td class="right aligned">{"{:10.1f}".format(inz_vacchosp_alle)}</td><td class="right aligned">{"{:10.1f}".format(inz_nonvacchosp_alle)}</td><td>{rel_hosp_alle_str}</td><td>{eff_hosp_alle_str}</td><td style="background-color:#edefee;"></td><td class="right aligned">{"{:10.1f}".format(inz_vaccdeath_alle)}</td><td class="right aligned">{"{:10.1f}".format(inz_nonvaccdeath_alle)}</td><td>{rel_death_alle_str}</td><td>{eff_death_alle_str}</td></tr>'

    html += f'</table><h3>Ungeimp. = Noch nicht vollständig geimpfte und ungeimpfte Personen</h3><h3>Web: covidlaws.net // Twitter: @CovidLawsStats</h3></td></tr></table> </body></html>'

    options = {'width': '1750', 'height': '1350', 'encoding': "UTF-8", }
    imgkit.from_string(html, "out_image.jpg", options=options)

