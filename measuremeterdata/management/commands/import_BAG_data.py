from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.models.models_ch import CHCanton, CHCases, DoomsdayClock
from measuremeterdata.tasks.socialmedia.tweet_covidmeter import tweet
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

            df_occupancy = pd.read_csv(zf.open('data/COVID19HospCapacity_geoRegion.csv'), error_bad_lines=False)
            ch_only = df_occupancy['geoRegion'] == 'CH'

            hosp_final = 0
            for index_row, row in df_occupancy[ch_only].tail(15).iterrows():
                hosp_final += row['ICU_Covid19Patients']
            hosp_cov19_patients = hosp_final/15

            hosp_final = 0
            for index_row, row in df_occupancy[ch_only].tail(22).head(15).iterrows():
                hosp_final += row['ICU_Covid19Patients']
            hosp_cov19_patients_7d = hosp_final/15

            hosp_capacity = df_occupancy[ch_only].tail(1)['ICU_Capacity'].item()
            hosp_date = df_occupancy[ch_only].tail(1)['date'].item()

            df_death = pd.read_csv(zf.open('data/COVID19Death_geoRegion.csv'), error_bad_lines=False)
            ch_only = df_death['geoRegion'] == 'CH'
            death_7days = df_death[ch_only].tail(2).head(1)['sum7d'].item()
            death_7days_7d = df_death[ch_only].tail(9).head(1)['sum7d'].item()

            df_vacc = pd.read_csv(zf.open('data/COVID19VaccDosesAdministered.csv'), error_bad_lines=False)
            ch_only = df_vacc['geoRegion'] == 'CH'
            now = df_vacc[ch_only].tail(1)['sumTotal'].item()
            bef7d = df_vacc[ch_only].tail(8).head(1)['sumTotal'].item()
            bef14d = df_vacc[ch_only].tail(15).head(1)['sumTotal'].item()

            vacc_value = (now - bef7d) * 100000 / 8500000
            vacc_value_7d = (bef7d - bef14d) * 100000 / 8500000
            vacc_date = df_vacc[ch_only].tail(1)['date'].item()

            df_positivity = pd.read_csv(zf.open('data/COVID19Test_geoRegion_all.csv'), error_bad_lines=False)

            ch_only = df_positivity['geoRegion']=='CH'
            pos_7days = df_positivity[ch_only].tail(7)
            total_pos_sum = 0
            for index_row, row in pos_7days.iterrows():
                total_pos_sum += row['pos_anteil']

            pos_7days_7d = df_positivity[ch_only].tail(14).head(7)
            total_pos_sum_7d = 0
            for index_row, row in pos_7days_7d.iterrows():
                total_pos_sum_7d += row['pos_anteil']

            positivity = total_pos_sum / 7
            positivity_7d = total_pos_sum_7d / 7

            positivity_date = df_positivity[ch_only].tail(1)['datum'].item()


            df_r = pd.read_csv(zf.open('data/COVID19Re_geoRegion.csv'), error_bad_lines=False)
            ch_only_filter = df_r['geoRegion']=='CH'
            ch_only = df_r[ch_only_filter]
            empty_filter = ch_only.median_R_mean.notnull()
            r_final = ch_only[empty_filter].tail(7)

            r_okay = False

            r_sum = 0

            for index_row, row in r_final.iterrows():
                r_sum += row['median_R_mean']

            r_average = r_sum / 7

            r_sum_7d = 0
            r_final_7d = ch_only[empty_filter].tail(14).head(7)
            for index_row, row in r_final_7d.iterrows():
                r_sum_7d += row['median_R_mean']
            r_average_7d = r_sum_7d / 7

            if r_sum < 1:
                r_okay = True


            df_hosp = pd.read_csv(zf.open('data/COVID19Hosp_geoRegion.csv'), error_bad_lines=False)
            ch_only_filter = df_hosp['geoRegion']=='CH'
            ch_only = df_hosp[ch_only_filter]
            empty_filter = ch_only.entries.notnull()
            hosp_final = ch_only[empty_filter].tail(14).head(7)

            hosp_sum = 0

            for index_row, row in hosp_final.iterrows():
                hosp_sum += row['entries']

            print(hosp_sum)
            hosp_average = hosp_sum / 7

            hosp_final_7d = ch_only[empty_filter].tail(21).head(7)

            hosp_sum_7d = 0

            for index_row, row in hosp_final_7d.iterrows():
                print(row['entries'])
                hosp_sum_7d += row['entries']

            print(hosp_sum_7d)
            hosp_average_7d = hosp_sum_7d / 7

            df_incidence = pd.read_csv(zf.open('data/COVID19Cases_geoRegion.csv'), error_bad_lines=False)
            df_incidence_ch_only = df_incidence['geoRegion']=='CH'

            incidence_mar1 = 161
            cases_14d = df_incidence[df_incidence_ch_only].tail(2).iloc[0]['sumTotal_last14d']

            incidence_latest = 100000*cases_14d/8570146
            incidence_latest_date = df_incidence[df_incidence_ch_only].tail(2).iloc[0]['datum']

            cases_14d_7d = df_incidence[df_incidence_ch_only].tail(9).iloc[0]['sum14d']
            incidence_latest_7d = 100000*cases_14d_7d/8570146

            print(df_incidence[df_incidence_ch_only].tail(2).iloc[0]['sumTotal_last14d'])
            print( df_incidence[df_incidence_ch_only].tail(2).iloc[0]['datum'])

            print(df_incidence[df_incidence_ch_only].tail(9).iloc[0]['sum14d'])
            print( df_incidence[df_incidence_ch_only].tail(9).iloc[0]['datum'])

            try:
                cd_existing = DoomsdayClock.objects.get(name="Master")
                old_date = cd_existing.incidence_latest_date
                cd_existing.hosp_cov19_patients = hosp_cov19_patients
                cd_existing.hosp_cov19_patients_7d = hosp_cov19_patients_7d
                cd_existing.hosp_capacity = hosp_capacity
                cd_existing.hosp_date = hosp_date
                cd_existing.positivity = positivity
                cd_existing.positivity_7d = positivity_7d
                cd_existing.positivity_date = positivity_date
                cd_existing.r_okay = r_okay
                cd_existing.r_average = r_average
                cd_existing.r_average_7d = r_average_7d
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
                cd_existing.r6_value = r_final.iloc[5].median_R_mean
                cd_existing.r6_date = r_final.iloc[5].date
                cd_existing.r7_value = r_final.iloc[6].median_R_mean
                cd_existing.r7_date = r_final.iloc[6].date
                cd_existing.hosp_average = hosp_average
                cd_existing.hosp_average_7d = hosp_average_7d
                cd_existing.hosp1_value = Decimal(hosp_final.iloc[0].entries.item())
                cd_existing.hosp1_date = hosp_final.iloc[0].datum
                cd_existing.hosp2_value = Decimal(hosp_final.iloc[1].entries.item())
                cd_existing.hosp2_date = hosp_final.iloc[1].datum
                cd_existing.hosp3_value = Decimal(hosp_final.iloc[2].entries.item())
                cd_existing.hosp3_date = hosp_final.iloc[2].datum
                cd_existing.hosp4_value = Decimal(hosp_final.iloc[3].entries.item())
                cd_existing.hosp4_date = hosp_final.iloc[3].datum
                cd_existing.hosp5_value = Decimal(hosp_final.iloc[4].entries.item())
                cd_existing.hosp5_date = hosp_final.iloc[4].datum
                cd_existing.hosp6_value = Decimal(hosp_final.iloc[5].entries.item())
                cd_existing.hosp6_date = hosp_final.iloc[5].datum
                cd_existing.hosp7_value = Decimal(hosp_final.iloc[6].entries.item())
                cd_existing.hosp7_date = hosp_final.iloc[6].datum
                cd_existing.incidence_mar1 = incidence_mar1
                cd_existing.incidence_latest = incidence_latest
                cd_existing.incidence_latest_7d = incidence_latest_7d
                cd_existing.incidence_latest_date = incidence_latest_date
                cd_existing.deaths_value = death_7days
                cd_existing.deaths_value_7d = death_7days_7d
                cd_existing.vacc_value = vacc_value
                cd_existing.vacc_value_7d = vacc_value_7d
                cd_existing.vacc_date = vacc_date
                cd_existing.save()
            except DoomsdayClock.DoesNotExist:
                cd = DoomsdayClock(name="Master",
                            hosp_cov19_patients = hosp_cov19_patients,
                            hosp_capacity=hosp_capacity,
                            hosp_date = hosp_date,
                            positivity = positivity,
                            positivity_date = positivity_date,
                            r_okay = r_okay,
                            r_average = r_average,
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
                            r6_value=r_final.iloc[5].median_R_mean,
                            r6_date=r_final.iloc[5].date,
                            r7_value=r_final.iloc[6].median_R_mean,
                            r7_date=r_final.iloc[6].date,
                            incidence_mar1 = incidence_mar1,
                            incidence_latest = incidence_latest,
                            incidence_latest_date = incidence_latest_date)
                cd.save()

            if old_date.isoformat() != cd_existing.incidence_latest_date:
                tweet()
