from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.models.models_ch import CHCanton, CHCases
import os
import csv
import io

import datetime
import requests
import pandas as pd
from datetime import date, timedelta
import measuremeterdata.tasks
from measuremeterdata.tasks.tweet_district_ranking import tweet

class Command(BaseCommand):
    def handle(self, *args, **options):

        has_new_data = False

        districts = CHCanton.objects.filter(code="so", level=1)

        url = "https://raw.githubusercontent.com/openZH/covid_19/master/fallzahlen_bezirke/fallzahlen_kanton_SO_bezirk.csv"
        s = requests.get(url).content
        df = pd.read_csv(io.StringIO(s.decode('utf-8')))

        for district in districts:
          has_new_data = load_district(df, district)

        if has_new_data:
            canton_code = "so"
            canton = CHCanton.objects.filter(level=0, code=canton_code)[0]
            tweet(canton)

def load_district(df, district):
    df_filtered = df[df['DistrictId'] == int(district.swisstopo_id)]
    df_filtered.set_index('Date')

    has_new_dataX = False

    for index, row in df_filtered.iterrows():

        cases_7days = None
        cases_14days = None
        date_now = date.fromisoformat(row['Date'])

        #7 days
        date7 = date_now - timedelta(days=7)
        try:
            cases_7days_ago = int(df[(df.DistrictId == int(district.swisstopo_id)) & (df.Date == date7.isoformat())]['TotalConfCases'])
            print(int(row['TotalConfCases']))
            print(cases_7days_ago)
            cases_7days = int(row['TotalConfCases']) - cases_7days_ago
        except:
            pass

        #14 days
        date14 = date_now - timedelta(days=14)
        try:
            cases_14days_ago = int(df[(df.DistrictId == int(district.swisstopo_id)) & (df.Date == date14.isoformat())]['TotalConfCases'])
            print(int(row['TotalConfCases']))
            print(cases_14days_ago)
            cases_14days = int(row['TotalConfCases']) - cases_14days_ago
        except:
            pass

        sdays = None
        ftdays=None

        if cases_7days:
            sdays = cases_7days / district.population * 100000

        if cases_14days:
            ftdays = cases_14days / district.population * 100000

        development7to7 = 0
        if cases_7days and cases_14days and ((cases_14days - cases_7days) > 0):
            development7to7 = (cases_7days * 100 / (cases_14days- cases_7days)) - 100

        try:
            cd_existing = CHCases.objects.get(canton=district, date=date_now)
            cd_existing.incidence_past14days = ftdays
            cd_existing.incidence_past7days = sdays
            cd_existing.development7to7 = development7to7
            cd_existing.save()
        except CHCases.DoesNotExist:
            has_new_dataX = True
            cd = CHCases(canton=district, incidence_past14days=ftdays, incidence_past7days=sdays, development7to7=development7to7, date=date_now)
            cd.save()

    return has_new_dataX


