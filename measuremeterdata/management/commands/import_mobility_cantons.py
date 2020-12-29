from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.models.models import Country, MeasureCategory, MeasureType, Measure, Continent, CasesDeaths
from measuremeterdata.models.models_ch import CHCanton, CHCases
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

class Command(BaseCommand):



    def handle(self, *args, **options):
        resp = urlopen(
            'https://www.gstatic.com/covid19/mobility/Region_Mobility_Report_CSVs.zip')

        zf = zipfile.ZipFile(BytesIO(resp.read()), 'r')
        df = pd.read_csv(zf.open('2020_CH_Region_Mobility_Report.csv'))

        for i, j in df.iterrows():

            if j.notnull()[5]:
                print(j[5])
                canton_code = j[5].split("-")[1].lower()
                try:
                    canton = CHCanton.objects.get(code=canton_code, level=0)
                except:
                    print("Does not exist")
                if canton:
                    date_tosave = date.fromisoformat(j[7])

                    try:
                        cd_existing = CHCases.objects.get(canton=canton, date=date_tosave)
                        cd_existing.mobility_recreation = j[8]
                        cd_existing.mobility_workplace = j[12]
                        cd_existing.mobility_transit = j[11]
                        cd_existing.save()
                    except CHCases.DoesNotExist:
                        cd = CHCases(canton=canton, mobility_recreation=j[8], mobility_workplace=j[12],
                                     mobility_transit=j[11], date=date_tosave)
                        cd.save()

                    print(canton_code)


