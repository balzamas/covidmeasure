from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.models.models_ch import CHCanton, CHCases, DoomsdayClock
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

class Command(BaseCommand):



    def handle(self, *args, **options):
        with urllib.request.urlopen("https://www.covid19.admin.ch/api/data/context") as url:
            data = json.loads(url.read().decode())

            resp = urlopen(
                data['sources']['zip']['csv'])

            zf = zipfile.ZipFile(BytesIO(resp.read()), 'r')

            df_occupancy = pd.read_csv(zf.open('data/COVID19HospCapacity_geoRegion.csv'))
            hosp_cov19_patients = df_occupancy.tail(1)['ICU_Covid19Patients'].item()
            hosp_capacity = df_occupancy.tail(1)['ICU_Capacity'].item()
            hosp_date = df_occupancy.tail(1)['date'].item()

            df_positivity = pd.read_csv(zf.open('data/COVID19Test_geoRegion_all.csv'))

            ch_only = df_positivity['geoRegion']=='CH'
            pos_7days = df_positivity[ch_only].tail(7)
            total_pos_sum = 0
            for index_row, row in pos_7days.iterrows():
                total_pos_sum += row['pos_anteil']

            positivity = total_pos_sum / 7
            positivity_date = df_positivity[ch_only].tail(1)['datum'].item()


            df_r = pd.read_csv(zf.open('data/COVID19Re_geoRegion.csv'))
            ch_only_filter = df_r['geoRegion']=='CH'
            ch_only = df_r[ch_only_filter]
            empty_filter = ch_only.median_R_mean.notnull()
            r_final = ch_only[empty_filter].tail(7)

            r_okay = True

            for index_row, row in r_final.iterrows():
                if row['median_R_mean'] > 1:
                    r_okay = False

            df_incidence = pd.read_csv(zf.open('data/COVID19Cases_geoRegion.csv'))
            df_incidence_ch_only = df_incidence['geoRegion']=='CH'

            incidence_mar1 = 163.35
            cases_14d = df_incidence[df_incidence_ch_only].tail(2).iloc[0]['sumTotal_last14d']

            incidence_latest = 100000*cases_14d/8570146
            incidence_latest_date = df_incidence[df_incidence_ch_only].tail(2).iloc[0]['datum']


            try:
                cd_existing = DoomsdayClock.objects.get(name="Master")
                cd_existing.hosp_cov19_patients = hosp_cov19_patients
                cd_existing.hosp_capacity = hosp_capacity
                cd_existing.hosp_date = hosp_date
                cd_existing.positivity = positivity
                cd_existing.positivity_date = positivity_date
                cd_existing.r_okay = r_okay
                cd_existing.r1_value = r_final.iloc[0].median_R_mean
                cd_existing.r1_date = r_final.iloc[0].date
                cd_existing.r2_value = r_final.iloc[1].median_R_mean
                cd_existing.r2_date = r_final.iloc[1].date
                cd_existing.r3_value = r_final.iloc[2].median_R_mean
                cd_existing.r3_date = r_final.iloc[2].date
                cd_existing.r4_value = r_final.iloc[3].median_R_mean
                cd_existing.r4_date = r_final.iloc[3].date
                cd_existing.r5_value = r_final.iloc[4].median_R_mean
                cd_existing.r5_date = r_final.iloc[4].date
                cd_existing.incidence_mar1 = incidence_mar1
                cd_existing.incidence_latest = incidence_latest
                cd_existing.incidence_latest_date = incidence_latest_date
                cd_existing.save()
            except DoomsdayClock.DoesNotExist:
                cd = DoomsdayClock(name="Master",
                            hosp_cov19_patients = hosp_cov19_patients,
                            hosp_capacity=hosp_capacity,
                            hosp_date = hosp_date,
                            positivity = positivity,
                            positivity_date = positivity_date,
                            r_okay = r_okay,
                            r1_value = r_final.iloc[0].median_R_mean,
                            r1_date = r_final.iloc[0].date,
                            r2_value = r_final.iloc[1].median_R_mean,
                            r2_date = r_final.iloc[1].date,
                            r3_value = r_final.iloc[2].median_R_mean,
                            r3_date = r_final.iloc[2].date,
                            r4_value = r_final.iloc[3].median_R_mean,
                            r4_date = r_final.iloc[3].date,
                            r5_value = r_final.iloc[4].median_R_mean,
                            r5_date = r_final.iloc[4].date,
                            incidence_mar1 = incidence_mar1,
                            incidence_latest = incidence_latest,
                            incidence_latest_date = incidence_latest_date)
                cd.save()
