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
        url=f"https://datenservice.kof.ethz.ch/api/v1/public/sets/stringency_plus_web?mime=csv&df=Y-m-d"

        with requests.Session() as s:
            download = s.get(url)

            decoded_content = download.content.decode('utf-8')

            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            my_list = list(cr)

            print("Load data into django")
            if len(my_list) > 1:

                count = 0
                cantons = []


                for row in my_list:
                    if count == 0:
                        col_cnt = 0
                        for col in row:
                            if col_cnt > 0:
                                print(col.split(".")[3])
                                if (col.split(".")[3] == 'ch'):
                                    cantons.append(CHCanton.objects.get(code=col.split(".")[3], level=3))
                                else:
                                    cantons.append(CHCanton.objects.get(code=col.split(".")[3], level=0))
                            col_cnt += 1



                    else:
                        date_tosave = date.fromisoformat(row[0])
                        col_cnt = -1
                        for col in row:
                            if col_cnt > -1:
                                print(cantons[col_cnt].code + ":" + col)
                                try:
                                    cd_existing = CHCases.objects.get(canton=cantons[col_cnt], date=date_tosave)
                                    cd_existing.kof_index = col
                                    cd_existing.save()
                                except CHCases.DoesNotExist:
                                    cd = CHCases(canton=cantons[col_cnt], kof_index=col, date=date_tosave)

                            col_cnt += 1

                    count =+ 1
