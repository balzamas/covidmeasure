from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.models.models import Country, Continent, CasesDeaths
import os
import csv
import datetime
import requests
import pandas as pd
from datetime import date, timedelta
from decimal import *

class Command(BaseCommand):
    def handle(self, *args, **options):

      url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'

      with requests.Session() as s:
        download = s.get(url)

        decoded_content = download.content.decode('utf-8')

        cr = csv.reader(decoded_content.splitlines(), delimiter=',')

        print("Load data into django")

        #Load countries
        cntries = []
        cntries.append('usa')
        cntries.append('can')
        cntries.append('aus')

        row_count = 0
        col_count = 0
        col_newcases = -1
        col_newdeaths = -1
        col_tests = -1
        col_tests_per_p = -1

        for row in cr:
            if row_count == 0:
                for col in row:
                    if col == "new_cases":
                        col_newcases = col_count
                    if col == "new_deaths":
                        col_newdeaths = col_count
                    col_count += 1
            row_count += 1


            if (row[0].lower() in cntries):
                if row[col_newcases]:
                    new_cases = Decimal(row[col_newcases])
                else:
                    new_cases = 0

                if row[col_newdeaths]:
                    new_deaths = Decimal(row[col_newdeaths])
                else:
                    new_deaths = 0

                date_tosave = date.fromisoformat(row[3])

                country = Country.objects.get(iso_code = row[0])

                try:
                    cd_existing = CasesDeaths.objects.get(country=country, date=date_tosave)
                    cd_existing.cases = new_cases
                    cd_existing.deaths = new_deaths
                    cd_existing.save()
                except:
                    cd = CasesDeaths(country=country, cases=new_cases, deaths=new_deaths, date=date_tosave)
                    cd.save()

        for cntry in cntries:
            print(cntry)
            country = Country.objects.get(iso_code=cntry.upper())

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
                    cases_past7 = 0.1
                if (cases_past7_before == 0):
                    cases_past7_before = 0.1

                day.development7to7 = (cases_past7 * 100 / cases_past7_before) - 100

                day.save()

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

                day.save()
