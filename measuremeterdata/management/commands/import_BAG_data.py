from django.core.management.base import BaseCommand, CommandError
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
            'https://www.covid19.admin.ch/api/data/20210218-thfu5buu/downloads/sources-csv.zip')

        zf = zipfile.ZipFile(BytesIO(resp.read()), 'r')

        df_occupancy = pd.read_csv(zf.open('data/COVID19HospCapacity_geoRegion.csv'))
        cov19_patients = df_occupancy.tail(1)['ICU_Covid19Patients'].item()
        capacity = df_occupancy.tail(1)['ICU_Capacity'].item()
        date = df_occupancy.tail(1)['date'].item()

        df_positivity = pd.read_csv(zf.open('data/COVID19Test_geoRegion_all.csv'))

        ch_only = df_positivity['geoRegion']=='CH'
        positivity = df_positivity[ch_only].tail(1)['pos_anteil'].item()
        positivity_date = df_positivity[ch_only].tail(1)['datum'].item()


        df_r = pd.read_csv(zf.open('data/COVID19Re_geoRegion.csv'))
        ch_only_r = df_r['geoRegion']=='CH'
        past7_r = df_r[ch_only_r].median_R_mean.notnull().tail(7)
        for index, value in past7_r.items():
            print(past7_r[index])
        print("....")
        print(past7_r)
        for index_row, row in past7_r.iterrows():
            print(row['median_R_mean'])
            print(row['date'])




