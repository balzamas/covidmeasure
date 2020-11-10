from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.models.models import Country, MeasureCategory, MeasureType, Measure, Continent, CasesDeaths
import os
import csv
import datetime
import requests
import pandas as pd
from datetime import date, timedelta, datetime
import measuremeterdata.tasks

def set_incidence(last_numbers, bezirk, date, cases_today):
    total = 0
    total7 = 0
    count = 0
    for cases in last_numbers:
        total += cases
        if (count > 6):
            total7 += cases
        count += 1

    ftdays = total / bezirk.population * 100000
    sdays = total7 / bezirk.population * 100000

    print(ftdays)

    try:
        cd_existing = CHCases.objects.get(canton=bezirk, date=date)
        cd_existing.incidence_past14days = ftdays
        cd_existing.incidence_past7days = sdays
        cd_existing.cases = cases_today
        cd_existing.save()
    except CHCases.DoesNotExist:
        cd = CHCases(canton=bezirk, incidence_past14days=ftdays, incidence_past7days=sdays, cases=cases_today, date=date)
        cd.save()
    return 0

class Command(BaseCommand):
    def handle(self, *args, **options):

      url="https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"

      with requests.Session() as s:

          download = s.get(url)

          decoded_content = download.content.decode('latin-1')

          cr = csv.reader(decoded_content.splitlines(), delimiter=',')
          my_list = list(cr)


          count = 0
          for row in my_list:
              if (count == 0):
                  daterow = row
                  print("xxx")
              else:
                  if (row[0]==""):
                      print(".........")
                      print(row[1])
                      country = None
                      try:
                        country = Country.objects.get(name=row[1])
                      except:
                        print("Does not exist")
                      if country:
                        print(country)
                        last_val = 0
                        col_count=0
                        for col in row:
                            if col_count > 3:
                                tdy_val = int(float(col)) - last_val
                                date_object = datetime.strptime(daterow[col_count], '%m/%d/%y')

                                try:
                                    cd_existing = CasesDeaths.objects.get(country=country, date=date_object)
                                    cd_existing.cases = tdy_val
                                    cd_existing.save()
                                except CasesDeaths.DoesNotExist:
                                    cd = CasesDeaths(country=country, cases=tdy_val, date=date_object)
                                    cd.save()

                                last_val = int(float(col))
                            col_count += 1

                        # calc running avg
                        last_numbers = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]

                        rec_cases = CasesDeaths.objects.filter(country=country).order_by('date')

                        print(country.name)
                        for day in rec_cases:
                            last_numbers.append(day.cases)
                            last_numbers.pop(0)
                            tot = 0
                            seven_tot = 0

                            daycount = 0
                            for x in last_numbers:
                                tot += x

                                if (daycount > 6):
                                    seven_tot += x

                                daycount += 1

                            fourteen_avg = tot * 100000 / country.population
                            seven_avg = seven_tot * 100000 / country.population

                            day.cases_past14days = fourteen_avg
                            day.cases_past7days = seven_avg

                            cases_past7 = sum(last_numbers[7:])
                            cases_past7_before = sum(last_numbers[:7])

                            if (cases_past7 == 0):
                                cases_past7 = 1
                            if (cases_past7_before == 0):
                                cases_past7_before = 1

                            day.development7to7 = (cases_past7 * 100 / cases_past7_before) - 100

                            day.save()

              count += 1
