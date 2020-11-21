from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.models.models import Country, CasesDeaths
from measuremeterdata.models.models_ch import CHCanton, CHCases
import os
import csv
import datetime
import requests
import pandas as pd
from datetime import date, timedelta
from measuremeterdata.tasks import import_helper


def LoadR0(country):
    print(f"Loading...{country}")
    url=f"https://raw.githubusercontent.com/covid-19-Re/dailyRe-Data/master/{country.iso_code}-estimates.csv"

    with requests.Session() as s:
        download = s.get(url)

        decoded_content = download.content.decode('utf-8')

        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)

        print("Load data into django")
        if len(my_list) > 1:

            for row in my_list:
                if (country.code == "ch"):
                    if row[1] == "CHE" and row[3] == 'Confirmed cases' and row[4] == 'Cori_slidingWindow':
                        date_tosave = date.fromisoformat(row[5])

                        try:
                            cd_existing = CasesDeaths.objects.get(country=country, date=date_tosave)
                            cd_existing.r0peak = row[7]
                            cd_existing.r0low = row[8]
                            cd_existing.r0median = row[6]
                            cd_existing.save()
                        except CasesDeaths.DoesNotExist:
                            cd = CasesDeaths(country=country, r0median = row[6], r0peak = row[7],
                                         r0low = row[8], date=date_tosave)
                            cd.save()
                    elif row[1] != "CHE" and row[3] == 'Confirmed cases' and row[4] == 'Cori_slidingWindow':
                        date_tosave = date.fromisoformat(row[5])
                        try:
                            canton = CHCanton.objects.get(code=row[1].lower(), level=0)
                            try:
                                cd_existing = CHCases.objects.get(canton=canton, date=date_tosave)
                                cd_existing.r0peak = row[7]
                                cd_existing.r0low = row[8]
                                cd_existing.r0median = row[6]
                                cd_existing.save()
                            except CHCases.DoesNotExist:
                                cd = CHCases(canton=canton, r0median = row[6], r0peak = row[7],
                                             r0low = row[8], date=date_tosave)
                                cd.save()
                        except:
                            print(f"{row[1]} does not exist.")
                else:
                    if (row[3] == 'Confirmed cases' and row[4] == 'Cori_slidingWindow'):
                        date_tosave = date.fromisoformat(row[5])

                        try:
                            cd_existing = CasesDeaths.objects.get(country=country, date=date_tosave)
                            cd_existing.r0peak = row[7]
                            cd_existing.r0low = row[8]
                            cd_existing.r0median = row[6]
                            cd_existing.save()
                        except CasesDeaths.DoesNotExist:
                            cd = CasesDeaths(country=country, r0median = row[6], r0peak = row[7],
                                         r0low = row[8], date=date_tosave)
                            cd.save()

class Command(BaseCommand):
    def handle(self, *args, **options):


        countries = Country.objects.all()
        for country in countries:
            if (country.code != "kp"):
                LoadR0(country)




