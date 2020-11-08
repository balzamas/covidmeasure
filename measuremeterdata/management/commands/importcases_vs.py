from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.models.models_ch import CHCanton, CHCases
import os
import csv
import datetime
import requests
import pandas as pd
from datetime import date, timedelta



#Source: https://data.europa.eu/euodp/en/data/dataset/covid-19-coronavirus-data/resource/55e8f966-d5c8-438e-85bc-c7a5a26f4863

def get_start_end_dates(year, week):
    d = datetime.datetime(year, 1, 1)
    if (d.weekday() <= 3):
        d = d - timedelta(d.weekday())
    else:
        d = d + timedelta(7 - d.weekday())
    dlt = timedelta(days=(week - 1) * 7)
    return d + dlt + timedelta(days=6)

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

class Command(BaseCommand):
    def handle(self, *args, **options):

      url = 'https://raw.githubusercontent.com/openZH/covid_19/master/fallzahlen_bezirke/fallzahlen_kanton_VS_bezirk.csv'

      with requests.Session() as s:
        download = s.get(url)

        decoded_content = download.content.decode('utf-8')

        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)

        print("Load data into django")

        count = 0

        last_days = 0

        for row in my_list:
            if (count > 0):
                date = get_start_end_dates(int(row[5]), int(row[4]))
                bezirk = CHCanton.objects.filter(swisstopo_id=int(row[0]))

                print(f"{date} - {bezirk}")

                if (bezirk):
                    ftdays = None

                    sdays = int(row[8]) / bezirk[0].population * 100000

                    sdays_ago =  CHCases.objects.get(canton=bezirk[0], date=(date - timedelta(days=7)))
                    if (sdays_ago.incidence_past7days):
                        ftdays = sdays + float(sdays_ago.incidence_past7days)


                    development7to7 = 0
                    if last_days > 0:
                        development7to7 = (int(row[8]) * 100 / last_days) - 100

                    try:
                        cd_existing = CHCases.objects.get(canton=bezirk[0], date=date)
                        cd_existing.incidence_past7days = sdays
                        cd_existing.development7to7 = development7to7
                        if (ftdays):
                            cd_existing.incidence_past14days = ftdays
                        cd_existing.save()
                    except CHCases.DoesNotExist:
                        if (ftdays):
                            cd = CHCases(canton=bezirk[0], incidence_past7days=sdays, incidence_past14days=ftdays, development7to7=development7to7, date=date)
                        else:
                            cd = CHCases(canton=bezirk[0], incidence_past7days=sdays, date=date)
                        cd.save()

                    last_days = int(row[8])

            count += 1

