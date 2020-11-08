from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.models.models_ch import CHCanton, CHCases
import os
import csv
import datetime
import requests
import pandas as pd
from datetime import date, timedelta

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


def CalcCaesesPerMio(cases, population):
    casespm = int(cases) *1000000 / (int(population))
    return casespm

class Command(BaseCommand):
    def handle(self, *args, **options):

      url = 'https://raw.githubusercontent.com/openZH/covid_19/master/fallzahlen_bezirke/fallzahlen_kanton_ZH_bezirk.csv'

      with requests.Session() as s:
        download = s.get(url)

        decoded_content = download.content.decode('utf-8')

        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)

        print("Load data into django")

        count = 0
        old_bezirk = -1
        last_7days = -1

        for row in my_list:
            if (count > 1):
                date = get_start_end_dates(int(row[4]), int(row[3]))

                bezirk = CHCanton.objects.filter(swisstopo_id=int(row[0]))

                if (bezirk):
                    ftdays = 0

                    print(".....")
                    print(row[5])

                    if (old_bezirk == int(row[0])):
                        ftdays = (int(row[5]) + last_7days) / bezirk[0].population * 100000

                    sdays = int(row[5]) / bezirk[0].population * 100000

                    development7to7 = 0
                    if (last_7days > 0):
                        development7to7 = (int(row[5]) * 100 / last_7days) - 100

                    try:
                        cd_existing = CHCases.objects.get(canton=bezirk[0], date=date)
                        cd_existing.incidence_past7days = sdays
                        cd_existing.incidence_past14days = ftdays
                        cd_existing.development7to7 = development7to7
                        cd_existing.save()
                    except CHCases.DoesNotExist:
                        cd = CHCases(canton=bezirk[0], incidence_past7days=sdays, incidence_past14days=ftdays, development7to7=development7to7, date=date)
                        cd.save()

                    old_bezirk = int(row[0])
                    last_7days = int(row[5])

            count += 1

