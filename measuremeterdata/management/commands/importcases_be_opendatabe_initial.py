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


def load(url):
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
                        cd = CHCases(canton=bezirk[0], incidence_past7days=sdays, incidence_past14days=ftdays,
                                     development7to7=development7to7, date=date_now)
                        cd.save()

            count += 1

class Command(BaseCommand):


    def handle(self, *args, **options):

      load('https://raw.githubusercontent.com/openDataBE/covid19Data/9697d527938f171a5bc4bcd128d364efea2889aa/7_d_inzidenz_verwaltungskreis.csv')
      load('https://raw.githubusercontent.com/openDataBE/covid19Data/22741e426f2574c733641a27d565a6ffb7d4c028/7_d_inzidenz_verwaltungskreis.csv')
      load('https://raw.githubusercontent.com/openDataBE/covid19Data/68cbecd063abb0e76e69b99a4f2557bfc6a4d8b5/7_d_inzidenz_verwaltungskreis.csv')
      load('https://raw.githubusercontent.com/openDataBE/covid19Data/9f5fac6354d3f60bf5e4b2e339c98d8d91faf3ac/7_d_inzidenz_verwaltungskreis.csv')
      load('https://raw.githubusercontent.com/openDataBE/covid19Data/5d7e1611551586d63356990e7c44dc0dd2f08a39/7_d_inzidenz_verwaltungskreis.csv')
      load('https://raw.githubusercontent.com/openDataBE/covid19Data/d3f4d1b8ad976c99932083be59e3e8138e33b1fe/7_d_inzidenz_verwaltungskreis.csv')
      load('https://raw.githubusercontent.com/openDataBE/covid19Data/3b05592160c536ae3d0f5e65abe37f2634917b6e/7_d_inzidenz_verwaltungskreis.csv')
      load('https://raw.githubusercontent.com/openDataBE/covid19Data/4f19a4abb97dd48549a8a652a1e158c8702b797e/7_d_inzidenz_verwaltungskreis.csv')




