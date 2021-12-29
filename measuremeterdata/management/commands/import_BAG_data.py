from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.models.models_ch import CHCanton, CHCases, DoomsdayClock
from measuremeterdata.tasks.socialmedia.tweet_covidmeter import tweet
from measuremeterdata.tasks.socialmedia.tweet_covidmeter2 import tweet as tweet2
from measuremeterdata.tasks.socialmedia.tweet_vacc_speed import tweet as tweet_vacc
from measuremeterdata.tasks.importer.ch.import_vacc_cantons import import_vacc_cantons
import os
import csv
import datetime
from datetime import date, timedelta
import requests
import pandas as pd
from io import BytesIO
import gzip
import math
from urllib.request import urlopen
from measuremeterdata.tasks import import_helper
import pandas as pd
import zipfile
import urllib.request, json
from decimal import *
class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('date')


    def handle(self, *args, **kwargs):
        arg_date = kwargs['date']

        date_to_load = datetime.datetime.today().strftime('%Y-%m-%d')
        date_to_load_date = datetime.datetime.today()

        if arg_date != 'now':
            date_to_load = arg_date
            date_to_load_date = datetime.datetime.strptime(date_to_load, "%Y-%m-%d")

        print("Importing...:")
        print(date_to_load)
        print(date_to_load_date)

        with urllib.request.urlopen("https://www.covid19.admin.ch/api/data/context") as url:
            data = json.loads(url.read().decode())

            resp = urlopen(
                data['sources']['zip']['csv'])

            zf = zipfile.ZipFile(BytesIO(resp.read()), 'r')

            df_occupancy = pd.read_csv(zf.open('data/COVID19HospCapacity_geoRegion.csv'), on_bad_lines='skip')
            df_occupancy['date'] = pd.to_datetime(df_occupancy['date'])
            df_occupancy = df_occupancy.set_index(['date'])

            ch_only = (df_occupancy['geoRegion'] == 'CH') & (df_occupancy['type_variant'] == 'fp7d')
            datefrom = (date_to_load_date - timedelta(days=15)).strftime('%Y-%m-%d')
            dateto = (date_to_load_date - timedelta(days=1)).strftime('%Y-%m-%d')

            print("Load Hospitalisations")
            hosp_final = 0
            for index_row, row in df_occupancy[ch_only].loc[datefrom:dateto].iterrows():
                hosp_final += row['ICU_Covid19Patients']
            hosp_cov19_patients = hosp_final/15

            hosp_capacity = df_occupancy[ch_only].loc[datefrom:dateto].tail(1)['ICU_Capacity'].item()
            hosp_date = df_occupancy[ch_only].loc[datefrom:dateto].tail(1).index.strftime('%Y-%m-%d')[0]

            datefrom = (date_to_load_date - timedelta(days=22)).strftime('%Y-%m-%d')
            dateto = (date_to_load_date - timedelta(days=8)).strftime('%Y-%m-%d')

            hosp_final = 0
            for index_row, row in df_occupancy[ch_only].loc[datefrom:dateto].iterrows():
                hosp_final += row['ICU_Covid19Patients']
            hosp_cov19_patients_7d = hosp_final/15

            #---------------------------------------------------------------------------

            print("Load Deaths")

            df_death = pd.read_csv(zf.open('data/COVID19Death_geoRegion.csv'), on_bad_lines='skip')
            df_death['datum'] = pd.to_datetime(df_death['datum'])
            df_death = df_death.set_index(['datum'])
            ch_only = df_death['geoRegion'] == 'CH'

            date_death = date_to_load_date.strftime('%Y-%m-%d')
            death_7days = df_death[ch_only].loc[date_death]['sum7d']

            date_death = (date_to_load_date - timedelta(days=7)).strftime('%Y-%m-%d')
            death_7days_7d = df_death[ch_only].loc[date_death]['sum7d']

            #---------------------------------------------------------------------------


            print("Vacc")

            df_vacc = pd.read_csv(zf.open('data/COVID19VaccDosesAdministered.csv'), on_bad_lines='skip')
            df_vacc['date'] = pd.to_datetime(df_vacc['date'])
            df_vacc = df_vacc.set_index(['date'])
            ch_only = df_vacc['geoRegion'] == 'CH'

            try:
                date_vacc = (date_to_load_date - timedelta(days=1)).strftime('%Y-%m-%d')
                now = df_vacc[ch_only].loc[date_vacc]['sumTotal']
                vacc_date = date_to_load_date - timedelta(days=1)
            except:
                print("xxxx")
                now = df_vacc[ch_only].tail(1)['sumTotal'].item()
                vacc_date = df_vacc[ch_only].tail(1).index[0]

            date_vacc = (vacc_date - timedelta(days=8)).strftime('%Y-%m-%d')
            bef7d = df_vacc[ch_only].loc[date_vacc]['sumTotal']

            date_vacc = (vacc_date - timedelta(days=15)).strftime('%Y-%m-%d')
            bef14d = df_vacc[ch_only].loc[date_vacc]['sumTotal']

            vacc_value = (now - bef7d) * 100000 / 8500000
            vacc_value_7d = (bef7d - bef14d) * 100000 / 8500000

            #---------------------------------------------------------------------------
            print("Positivity")

            df_positivity = pd.read_csv(zf.open('data/COVID19Test_geoRegion_all.csv'), on_bad_lines='skip')
            df_positivity['datum'] = pd.to_datetime(df_positivity['datum'])
            df_positivity = df_positivity.set_index(['datum'])
            ch_only = df_positivity['geoRegion'] == 'CH'

            datefrom = (date_to_load_date - timedelta(days=7)).strftime('%Y-%m-%d')
            dateto = (date_to_load_date - timedelta(days=1)).strftime('%Y-%m-%d')
            positivity_date = (date_to_load_date - timedelta(days=1))

            total_pos_sum = 0
            for index_row, row in df_positivity[ch_only].loc[datefrom:dateto].iterrows():
                total_pos_sum += row['pos_anteil']


            datefrom = (date_to_load_date - timedelta(days=14)).strftime('%Y-%m-%d')
            dateto = (date_to_load_date - timedelta(days=8)).strftime('%Y-%m-%d')
            total_pos_sum_7d = 0
            for index_row, row in df_positivity[ch_only].loc[datefrom:dateto].iterrows():
                total_pos_sum_7d += row['pos_anteil']

            positivity = total_pos_sum / 7
            positivity_7d = total_pos_sum_7d / 7

            print(positivity)
            print(positivity_7d)

            #---------------------------------------------------------------------------
            print("R")

            df_r = pd.read_csv(zf.open('data/COVID19Re_geoRegion.csv'), on_bad_lines='skip')
            df_r['date'] = pd.to_datetime(df_r['date'])
            df_r = df_r.set_index(['date'])
            ch_only_filter = df_r['geoRegion']=='CH'

            r_okay = False

            r_sum = 0

            datefrom = (date_to_load_date - timedelta(days=19)).strftime('%Y-%m-%d')
            dateto = (date_to_load_date - timedelta(days=13)).strftime('%Y-%m-%d')

            r_final = df_r[ch_only_filter].loc[datefrom:dateto]
            print(r_final.index[0])
            for index_row, row in df_r[ch_only_filter].loc[datefrom:dateto].iterrows():
                r_sum += row['median_R_mean']

            print("R")

            if math.isnan(r_sum):
                print("Empty")
                datefrom = (date_to_load_date - timedelta(days=20)).strftime('%Y-%m-%d')
                dateto = (date_to_load_date - timedelta(days=14)).strftime('%Y-%m-%d')
                r_sum = 0

                r_final = df_r[ch_only_filter].loc[datefrom:dateto]
                for index_row, row in df_r[ch_only_filter].loc[datefrom:dateto].iterrows():
                    r_sum += row['median_R_mean']
                r_average = r_sum / 7
            else:
                r_average = r_sum / 7


            r_sum_7d = 0
            datefrom = (date_to_load_date - timedelta(days=27)).strftime('%Y-%m-%d')
            dateto = (date_to_load_date - timedelta(days=20)).strftime('%Y-%m-%d')
            for index_row, row in df_r[ch_only_filter].loc[datefrom:dateto].iterrows():
                r_sum_7d += row['median_R_mean']
            r_average_7d = r_sum_7d / 7

            if r_sum < 1:
                r_okay = True

            #---------------------------------------------------------------------------

            print("Hosp")

            df_hosp = pd.read_csv(zf.open('data/COVID19Hosp_geoRegion.csv'), on_bad_lines='skip')
            df_hosp['datum'] = pd.to_datetime(df_hosp['datum'])
            df_hosp = df_hosp.set_index(['datum'])
            ch_only_filter = df_hosp['geoRegion']=='CH'

            ch_only = df_hosp[ch_only_filter]
            empty_filter = ch_only.entries.notnull()

            hosp_sum = 0

            datefrom = (date_to_load_date - timedelta(days=12)).strftime('%Y-%m-%d')
            dateto = (date_to_load_date - timedelta(days=6)).strftime('%Y-%m-%d')

            hosp_final = df_hosp[ch_only_filter].loc[datefrom:dateto]

            for index_row, row in df_hosp[ch_only_filter].loc[datefrom:dateto].iterrows():
                print(row['entries'])
                hosp_sum += row['entries']

            print(hosp_sum)
            hosp_average = hosp_sum / 7

            hosp_final_7d = ch_only[empty_filter].tail(21).head(7)

            hosp_sum_7d = 0

            datefrom = (date_to_load_date - timedelta(days=19)).strftime('%Y-%m-%d')
            dateto = (date_to_load_date - timedelta(days=13)).strftime('%Y-%m-%d')

            for index_row, row in df_hosp[ch_only_filter].loc[datefrom:dateto].iterrows():
                print(row['entries'])
                hosp_sum_7d += row['entries']

            print(hosp_sum_7d)
            hosp_average_7d = hosp_sum_7d / 7

            #---------------------------------------------------------------------------

            print("Inz")

            df_incidence = pd.read_csv(zf.open('data/COVID19Cases_geoRegion.csv'), on_bad_lines='skip')
            df_incidence['datum'] = pd.to_datetime(df_incidence['datum'])
            df_incidence = df_incidence.set_index(['datum'])
            df_incidence_ch_only = df_incidence['geoRegion']=='CH'

            incidence_mar1 = 161
            date_inz = (date_to_load_date - timedelta(days=1)).strftime('%Y-%m-%d')
            cases_14d = df_incidence[df_incidence_ch_only].loc[date_inz]['sum14d']

            incidence_latest = 100000*cases_14d/8570146
            incidence_latest_date = (date_to_load_date - timedelta(days=1))

            date_inz = (date_to_load_date - timedelta(days=8)).strftime('%Y-%m-%d')
            cases_14d_7d = df_incidence[df_incidence_ch_only].loc[date_inz]['sum14d']
            incidence_latest_7d = 100000*cases_14d_7d/8570146
            print(df_incidence[df_incidence_ch_only].tail(9).iloc[0]['sum14d'])
            print("Save...")

            try:
                cd_existing = DoomsdayClock.objects.get(cur_date=date_to_load_date)
                cd_existing.cur_date = date_to_load_date
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
                cd_existing.r1_date = r_final.index[0]
                cd_existing.r2_value = r_final.iloc[1].median_R_mean
                cd_existing.r2_date = r_final.index[1]
                cd_existing.r3_value = r_final.iloc[2].median_R_mean
                cd_existing.r3_date = r_final.index[2]
                cd_existing.r4_value = r_final.iloc[3].median_R_mean
                cd_existing.r4_date = r_final.index[3]
                cd_existing.r5_value = r_final.iloc[4].median_R_mean
                cd_existing.r5_date = r_final.index[4]
                cd_existing.r6_value = r_final.iloc[5].median_R_mean
                cd_existing.r6_date = r_final.index[5]
                cd_existing.r7_value = r_final.iloc[6].median_R_mean
                cd_existing.r7_date = r_final.index[6]
                cd_existing.hosp_average = hosp_average
                cd_existing.hosp_average_7d = hosp_average_7d
                cd_existing.hosp1_value = Decimal(hosp_final.iloc[0].entries.item())
                cd_existing.hosp1_date = hosp_final.index[0]
                cd_existing.hosp2_value = Decimal(hosp_final.iloc[1].entries.item())
                cd_existing.hosp2_date = hosp_final.index[1]
                cd_existing.hosp3_value = Decimal(hosp_final.iloc[2].entries.item())
                cd_existing.hosp3_date = hosp_final.index[2]
                cd_existing.hosp4_value = Decimal(hosp_final.iloc[3].entries.item())
                cd_existing.hosp4_date = hosp_final.index[3]
                cd_existing.hosp5_value = Decimal(hosp_final.iloc[4].entries.item())
                cd_existing.hosp5_date = hosp_final.index[4]
                cd_existing.hosp6_value = Decimal(hosp_final.iloc[5].entries.item())
                cd_existing.hosp6_date = hosp_final.index[5]
                cd_existing.hosp7_value = Decimal(hosp_final.iloc[6].entries.item())
                cd_existing.hosp7_date = hosp_final.index[6]
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
                cd = DoomsdayClock(
                            cur_date = date_to_load_date,
                            hosp_cov19_patients = hosp_cov19_patients,
                            hosp_cov19_patients_7d = hosp_cov19_patients_7d,
                            hosp_capacity=hosp_capacity,
                            hosp_date = hosp_date,
                            positivity = positivity,
                            positivity_7d=positivity_7d,
                            positivity_date = positivity_date,
                            r_okay = r_okay,
                            r_average = r_average,
                            r_average_7d=r_average_7d,
                            r1_value = r_final.iloc[0].median_R_mean,
                            r1_date = r_final.index[0],
                            r2_value = r_final.iloc[1].median_R_mean,
                            r2_date = r_final.index[1],
                            r3_value = r_final.iloc[2].median_R_mean,
                            r3_date = r_final.index[2],
                            r4_value = r_final.iloc[3].median_R_mean,
                            r4_date = r_final.index[3],
                            r5_value = r_final.iloc[4].median_R_mean,
                            r5_date = r_final.index[4],
                            r6_value=r_final.iloc[5].median_R_mean,
                            r6_date=r_final.index[5],
                            r7_value=r_final.iloc[6].median_R_mean,
                            r7_date=r_final.index[6],
                            hosp_average = hosp_average,
                            hosp_average_7d = hosp_average_7d,
                            hosp1_value = Decimal(hosp_final.iloc[0].entries.item()),
                            hosp1_date = hosp_final.index[0],
                            hosp2_value = Decimal(hosp_final.iloc[1].entries.item()),
                            hosp2_date = hosp_final.index[1],
                            hosp3_value = Decimal(hosp_final.iloc[2].entries.item()),
                            hosp3_date = hosp_final.index[2],
                            hosp4_value = Decimal(hosp_final.iloc[3].entries.item()),
                            hosp4_date = hosp_final.index[3],
                            hosp5_value = Decimal(hosp_final.iloc[4].entries.item()),
                            hosp5_date = hosp_final.index[4],
                            hosp6_value = Decimal(hosp_final.iloc[5].entries.item()),
                            hosp6_date = hosp_final.index[5],
                            hosp7_value = Decimal(hosp_final.iloc[6].entries.item()),
                            hosp7_date = hosp_final.index[6],
                            incidence_mar1 = incidence_mar1,
                            incidence_latest = incidence_latest,
                            incidence_latest_7d = incidence_latest_7d,
                            incidence_latest_date = incidence_latest_date,
                            deaths_value = death_7days,
                            deaths_value_7d = death_7days_7d,
                            vacc_value = vacc_value,
                            vacc_value_7d = vacc_value_7d,
                            vacc_date = vacc_date
                )
                cd.save()

                tweet2()
                #import_vacc_cantons()
                #tweet_vacc()
