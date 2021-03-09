from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.models.models import Country, MeasureCategory, Continent, CasesDeaths
import os
import csv
import datetime
import requests
import pandas as pd
from datetime import date, timedelta, datetime

#Source: https://data.europa.eu/euodp/en/data/dataset/covid-19-coronavirus-data/resource/55e8f966-d5c8-438e-85bc-c7a5a26f4863

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
                                        cd_existing.save()
                                    except CasesDeaths.DoesNotExist:
                                        cd = CasesDeaths(country=country, deaths=tdy_val, date=date_object)
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
                            seven_tot = 0
                            daycount = 0

                            for x in last_numbers_death:
                                tot_death += x

                                if (daycount > 6):
                                    seven_tot += x

                                daycount += 1


                            fourteen_avg_death = tot_death * 100000 / country.population
                            seven_avg = seven_tot * 100000 / country.population


                            day.deaths_past14days = fourteen_avg_death
                            day.deaths_past7days = seven_avg

                            past_date = date(2020, 6, 1)
                            if day.date > past_date:
                                cases = CasesDeaths.objects.get(country=country, date=(day.date-timedelta(21)))
                                if seven_avg > 0:
                                    day.death_to_cases = float(cases.cases_past7days) / float(seven_avg)
                                else:
                                    day.death_to_cases = 0
                            day.save()

              count += 1
