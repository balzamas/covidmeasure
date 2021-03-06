from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.models.models_ch import CHCanton, CHCases
import os
import csv
import datetime
import requests
import pandas as pd
from datetime import date, timedelta
from measuremeterdata.tasks import import_helper
from measuremeterdata.tasks.socialmedia.tweet_district_ranking import tweet

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

        has_new_data = False

        for row in my_list:
            if (count > 0):
                date = import_helper.get_start_end_dates(int(row[5]), int(row[4]))[1]
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
                        has_new_data = True
                        if (ftdays):
                            cd = CHCases(canton=bezirk[0], incidence_past7days=sdays, incidence_past14days=ftdays, development7to7=development7to7, date=date)
                        else:
                            cd = CHCases(canton=bezirk[0], incidence_past7days=sdays, date=date)
                        cd.save()

                    last_days = int(row[8])

            count += 1

        if has_new_data:
            canton_code = "vs"
            canton = CHCanton.objects.filter(level=0, code=canton_code)[0]
            tweet(canton)

