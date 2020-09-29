from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.models import Country, MeasureCategory, MeasureType, Measure, Continent, CasesDeaths, CHCanton, CHCases
import os
import csv
import datetime
import requests
import pandas as pd
from datetime import date, timedelta
import urllib.request, json

class Command(BaseCommand):
    def handle(self, *args, **options):

      url_toload = 'https://vis.csh.ac.at/riskpatients/disease_rate.json'

      bezirke = ["801", "802", "803", "804", "706"]

      with urllib.request.urlopen(url_toload) as url:
          data = json.loads(url.read().decode())
          for row in data["features"]:

                if (row['properties']['iso'] in bezirke):

                    bezirk = CHCanton.objects.filter(swisstopo_id="A" + row['properties']['iso'])

                    if (bezirk):

                        last_numbers = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]

                        for day in row['properties']["deltaDisease"]:

                            val_today = row['properties']["deltaDisease"][day]


                            last_numbers.append(val_today)
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

                            date_tosave = date.fromisoformat(day)

                            print(row['properties']["name"])
                            print(date_tosave)
                            print(fourteen_avg)


                            try:
                                cd_existing = CHCases.objects.get(canton=bezirk[0], date=date_tosave)
                                cd_existing.cases = val_today
                                cd_existing.cases_past7days = seven_avg
                                cd_existing.cases_past14days = fourteen_avg
                                cd_existing.date = date_tosave
                                cd_existing.save()
                            except CHCases.DoesNotExist:
                                cd = CHCases(canton=bezirk[0], cases_past7days=seven_avg, cases_past14days=fourteen_avg,
                                             cases=val_today, date=date_tosave)
                                cd.save()


