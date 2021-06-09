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
from decimal import Decimal

class Command(BaseCommand):
    def handle(self, *args, **options):

      url = 'https://raw.githubusercontent.com/openDataBE/covid19Data/develop/7_d_inzidenz_verwaltungskreis.csv'

      with requests.Session() as s:
        download = s.get(url)

        decoded_content = download.content.decode('utf-8')

        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)

        print("Load data into django")

        count = 0
        last_7days = -1

        has_new_data = False

        for row in my_list:
            if (count > 0):
                    format_str = '%d.%m.%Y'
                    date_now = datetime.datetime.strptime(row[0], format_str)
                    bezirk = CHCanton.objects.filter(swisstopo_id=int(row[2]))

                    print(bezirk[0])

                    if (bezirk):

                        sdays = Decimal(row[4])

                        date_7dago = date_now - timedelta(days=7)
                        print(type(date_7dago))
                        print(date_7dago)
                        print(date_now)

                        ftdays = None
                        development7to7 = None

                        print("Load...")
                        try:
                            cd_7dago = CHCases.objects.get(canton=bezirk[0], date=date_7dago)
                            ftdays = sdays + cd_7dago.incidence_past7days
                            development7to7 = (sdays * 100 / cd_7dago.incidence_past7days) - 100
                        except:
                            pass

                        try:
                            cd_existing = CHCases.objects.get(canton=bezirk[0], date=date_now)
                            cd_existing.incidence_past7days = sdays
                            cd_existing.incidence_past14days = ftdays
                            cd_existing.development7to7 = development7to7
                            cd_existing.save()
                        except CHCases.DoesNotExist:
                            has_new_data = True
                            cd = CHCases(canton=bezirk[0], incidence_past7days=sdays, incidence_past14days=ftdays, development7to7=development7to7, date=date_now)
                            cd.save()

            count += 1

        if has_new_data:
            canton_code = "be"
            canton = CHCanton.objects.filter(level=0, code=canton_code)[0]
            tweet(canton)
