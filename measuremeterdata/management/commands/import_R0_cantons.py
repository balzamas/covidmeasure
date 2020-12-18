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


class Command(BaseCommand):
    def handle(self, *args, **options):
        url=f"https://raw.githubusercontent.com/covid-19-Re/dailyRe-Data/master/CHE-confCasesSWestimates.csv"

        with requests.Session() as s:
            download = s.get(url)

            decoded_content = download.content.decode('utf-8')

            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            my_list = list(cr)

            print("Load data into django")
            if len(my_list) > 1:

                count = 0

                for row in my_list:
                    if count > 0:
                        date_tosave = date.fromisoformat(row[1])
                        try:
                            canton = CHCanton.objects.get(code=row[0].lower(), level=0)
                            try:
                                cd_existing = CHCases.objects.get(canton=canton, date=date_tosave)
                                cd_existing.r0peak = row[3]
                                cd_existing.r0low = row[4]
                                cd_existing.r0median = row[2]
                                cd_existing.save()
                            except CHCases.DoesNotExist:
                                cd = CHCases(canton=canton, r0median=row[2], r0peak=row[3],
                                             r0low=row[4], date=date_tosave)
                                cd.save()
                        except:
                            print(f"{row[0]} does not exist.")
                    count += 1
