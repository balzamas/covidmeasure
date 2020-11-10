from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.models.models_ch import CHCanton, CHCases
import os
import csv
import datetime
import requests
import pandas as pd
from datetime import date, timedelta
from measuremeterdata.tasks import import_helper



#Source: https://data.europa.eu/euodp/en/data/dataset/covid-19-coronavirus-data/resource/55e8f966-d5c8-438e-85bc-c7a5a26f4863

class Command(BaseCommand):
    def handle(self, *args, **options):

      url = 'https://raw.githubusercontent.com/openZH/covid_19/master/fallzahlen_bezirke/fallzahlen_kanton_FR_bezirk.csv'

      with requests.Session() as s:
        download = s.get(url)

        decoded_content = download.content.decode('utf-8')

        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)

        print("Load data into django")

        count = 0

        for row in my_list:
            if (count > 0):
                if row[5] != '' and row[4] != '':
                    date = import_helper.get_start_end_dates(int(row[5]), int(row[4]))[1]
                    bezirk = CHCanton.objects.filter(swisstopo_id=int(row[0]))

                    print(f"{date} - {bezirk}")

                    if (bezirk):
                        ftdays = None

                        sdays = int(row[8]) / bezirk[0].population * 100000

                        sdays_ago =  CHCases.objects.get(canton=bezirk[0], date=(date - timedelta(days=7)))
                        if (sdays_ago.incidence_past7days):
                            ftdays = sdays + float(sdays_ago.incidence_past7days)

                        try:
                            cd_existing = CHCases.objects.get(canton=bezirk[0], date=date)
                            cd_existing.incidence_past7days = sdays
                            if (ftdays):
                                cd_existing.incidence_past14days = ftdays
                            cd_existing.save()
                        except CHCases.DoesNotExist:
                            if (ftdays):
                                cd = CHCases(canton=bezirk[0], incidence_past7days=sdays, incidence_past14days=ftdays, date=date)
                            else:
                                cd = CHCases(canton=bezirk[0], incidence_past7days=sdays, date=date)
                            cd.save()

            count += 1

