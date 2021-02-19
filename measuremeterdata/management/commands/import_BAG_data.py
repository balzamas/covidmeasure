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
            'https://www.covid19.admin.ch/api/data/20210219-4389xau5/downloads/sources-csv.zip')

        zf = zipfile.ZipFile(BytesIO(resp.read()), 'r')

        df_occupancy = pd.read_csv(zf.open('data/COVID19HospCapacity_geoRegion.csv'))
        hosp_cov19_patients = df_occupancy.tail(1)['ICU_Covid19Patients'].item()
        hosp_capacity = df_occupancy.tail(1)['ICU_Capacity'].item()
        hosp_date = df_occupancy.tail(1)['date'].item()

        df_positivity = pd.read_csv(zf.open('data/COVID19Test_geoRegion_all.csv'))

        ch_only = df_positivity['geoRegion']=='CH'
        positivity = df_positivity[ch_only].tail(1)['pos_anteil'].item()
        positivity_date = df_positivity[ch_only].tail(1)['datum'].item()


        df_r = pd.read_csv(zf.open('data/COVID19Re_geoRegion.csv'))
        ch_only_filter = df_r['geoRegion']=='CH'
        ch_only = df_r[ch_only_filter]
        empty_filter = ch_only.median_R_mean.notnull()
        r_final = ch_only[empty_filter].tail(7)

        for index_row, row in r_final.iterrows():
            print(row['median_R_mean'])
            print(row['date'])

        df_incidence = pd.read_csv(zf.open('data/COVID19Cases_geoRegion.csv'))
        df_incidence_ch_only = df_incidence['geoRegion']=='CH'

        incidence_mar1 = 200
        incidence_now = df_incidence[df_incidence_ch_only].tail(1)['inzsum14d'].item()
        incidence_date = df_incidence[df_incidence_ch_only].tail(1)['datum'].item()

        print(".....")
        print(incidence_now)
        print(incidence_date)
