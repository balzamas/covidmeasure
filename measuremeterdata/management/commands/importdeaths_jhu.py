from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.models import Country, MeasureCategory, MeasureType, Measure, Continent, CasesDeaths, CHCanton, CHCases
import os
import csv
import datetime
import requests
import pandas as pd
from datetime import date, timedelta, datetime



#Source: https://data.europa.eu/euodp/en/data/dataset/covid-19-coronavirus-data/resource/55e8f966-d5c8-438e-85bc-c7a5a26f4863

def get_start_end_dates(year, week):
    d = datetime.datetime(year, 1, 1)
    if (d.weekday() <= 3):
        d = d - timedelta(d.weekday())
    else:
        d = d + timedelta(7 - d.weekday())
    dlt = timedelta(days=(week - 1) * 7)
    return d + dlt + timedelta(days=6)

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)


def CalcCaesesPerMio(cases, population):
    casespm = int(cases) *1000000 / (int(population))
    return casespm

def CalcCaesesPer100k(cases, population):
    casespm = int(cases) *100000 / (int(population))
    return casespm

class Command(BaseCommand):
    def handle(self, *args, **options):

      url="https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"

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
                                if col != '':
                                    tdy_val = int(float(col)) - last_val
                                    date_object = datetime.strptime(daterow[col_count], '%m/%d/%y')

                                    try:
                                        cd_existing = CasesDeaths.objects.get(country=country, date=date_object)
                                        cd_existing.deaths = tdy_val
                                        cd_existing.deaths_per100k = CalcCaesesPer100k(tdy_val, country.population)
                                        cd_existing.save()
                                    except CasesDeaths.DoesNotExist:
                                        cd = CasesDeaths(country=country, deaths=tdy_val, date=date_object,
                                                         deaths_per100k=CalcCaesesPer100k(tdy_val, country.population))
                                        cd.save()

                                    last_val = int(float(col))
                            col_count += 1

                        # calc running avg
                        last_numbers_death = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]

                        rec_cases = CasesDeaths.objects.filter(country=country).order_by('date')

                        print(country.name)
                        for day in rec_cases:
                            last_numbers_death.append(day.deaths)
                            last_numbers_death.pop(0)
                            tot_death = 0

                            for x in last_numbers_death:
                                tot_death += x

                            fourteen_avg_death = tot_death * 100000 / country.population

                            day.deaths_past14days = fourteen_avg_death

                            day.save()

              count += 1
