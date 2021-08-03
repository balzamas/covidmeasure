from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.models.models_ch import CHCanton, CHCases, DoomsdayClock
from measuremeterdata.tasks.socialmedia.tweet_closeometer import tweet
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
class Command(BaseCommand):



    def handle(self, *args, **options):
        with urllib.request.urlopen("https://www.covid19.admin.ch/api/data/context") as url:
            data = json.loads(url.read().decode())

            resp = urlopen(
                data['sources']['zip']['csv'])

            zf = zipfile.ZipFile(BytesIO(resp.read()), 'r')

            for canton in CHCanton.objects.filter(level=0):

                print(canton)

                vacc = pd.read_csv(zf.open('data/COVID19VaccDosesAdministered.csv'), error_bad_lines=False)
                canton_filter = vacc['geoRegion'] == canton.code.upper()
                last14days = vacc[canton_filter].tail(15)
                now = last14days.tail(1)["sumTotal"].item()
                seven_daysago = last14days.head(8).tail(1)["sumTotal"].item()
                ft_daysago = last14days.head(1)["sumTotal"].item()

                print(canton.code)
                vacc_perpop_7d = round((100000 * (now - seven_daysago) / canton.population),2)
                print(vacc_perpop_7d)

                vacc_perpop = round((vacc_perpop_7d / 7),2)

                try:
                    print("cccccc")
                    date = datetime.datetime.fromisoformat(last14days.tail(1)["date"].item())
                    print(date)
                    cd_existing = CHCases.objects.get(canton=canton, date=date)
                    cd_existing.vacc_perpop_7d = vacc_perpop_7d
                    cd_existing.vacc_perpop = vacc_perpop
                    cd_existing.vacc_total = int(now)

                    cd_existing.save()
                except CHCases.DoesNotExist:
                    print("....")
                    print(date)
                    cd = CHCases(canton=canton,
                                 vacc_perpop_7d=vacc_perpop_7d,
                                 vacc_perpop=vacc_perpop,
                                 vacc_total=int(now),
                                 date=date)
                    cd.save()
