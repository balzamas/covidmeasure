from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.models import Country, MeasureCategory, MeasureType, Measure, Continent, CasesDeaths, CHCanton, CHCases
import os
import csv
import datetime
import requests
import pandas as pd
from datetime import date, timedelta

class Command(BaseCommand):
    def handle(self, *args, **options):

      url = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province.csv'

      with requests.Session() as s:
        download = s.get(url)

        decoded_content = download.content.decode('utf-8')

        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)

        print("Load data into django")

        provinces = ["007", "002","103","012","013","014","021",]

        count = 0
        old_bezirk = -1

        for province in provinces:
            last_numbers = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
            last_day = 0
            for row in my_list:
                if count > 0:
                    if row[4] == province:
                            print(row)

                            bezirk = CHCanton.objects.filter(swisstopo_id="I"+row[4])

                            if (bezirk):

                                this_day = int(row[9])
                                today_only = this_day - last_day
                                last_day = this_day


                                last_numbers.append(today_only)
                                last_numbers.pop(0)

                                tot = 0
                                seven_tot = 0

                                daycount = 0
                                for x in last_numbers:
                                    tot += x

                                    if (daycount > 6):
                                        seven_tot += x

                                    daycount += 1


                                fourteen_avg = tot * 100000 / bezirk[0].population
                                seven_avg = seven_tot * 100000 / bezirk[0].population

                                date_tosave = date.fromisoformat(row[0].split("T")[0])

                                print(bezirk[0])
                                print(today_only)
                                print(f"Average:{fourteen_avg}")

                                try:
                                    cd_existing = CHCases.objects.get(canton=bezirk[0], date=date_tosave)
                                    cd_existing.cases = today_only
                                    cd_existing.incidence_past7days = seven_avg
                                    cd_existing.incidence_past14days = fourteen_avg
                                    cd_existing.date = date_tosave
                                    cd_existing.save()
                                except CHCases.DoesNotExist:
                                    cd = CHCases(canton=bezirk[0], incidence_past7days=seven_avg, incidence_past14days=fourteen_avg, cases=today_only, date=date_tosave)
                                    cd.save()
                count += 1

