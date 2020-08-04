from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.models import Country, MeasureCategory, MeasureType, Measure, Continent, CasesDeaths, CHCanton, CHCases
import os
import csv
import datetime
import requests
import pandas as pd
from datetime import date, timedelta



#Source: https://data.europa.eu/euodp/en/data/dataset/covid-19-coronavirus-data/resource/55e8f966-d5c8-438e-85bc-c7a5a26f4863

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)


def CalcCaesesPerMio(cases, population):
    casespm = int(cases) *1000000 / (int(population))
    return casespm

class Command(BaseCommand):
    def handle(self, *args, **options):

      url = 'https://raw.githubusercontent.com/openZH/covid_19/master/COVID19_Fallzahlen_CH_total_v2.csv'

      with requests.Session() as s:
        download = s.get(url)

        decoded_content = download.content.decode('utf-8')

        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)

        print("Load data into django")
        for canton in CHCanton.objects.all():
            cantoncode = canton.code
            print(cantoncode)

            old_value = 0
            last_numbers = [0, 0, 0, 0, 0, 0, 0]

            #Well...we overwrite everything with 0
            end_date = date.today()
            start_date = date.fromisoformat('2020-02-20')
            day_count = (end_date - start_date).days + 1
            for single_date in [d for d in (start_date + timedelta(n) for n in range(day_count)) if d <= end_date]:
                try:
                    cd_existing = CHCases.objects.get(canton=canton, date=single_date)
                    cd_existing.cases = 0
                    cd_existing.save()
                except CHCases.DoesNotExist:
                    cd = CHCases(canton=canton, cases=0, date=single_date)
                    cd.save()

            # Should move to datasources directory
            for row in my_list:

                if row[2].lower() == cantoncode.lower():
                    try:
                        print(row[2])
                        print(row[0])
                        if row[4] is '':
                                cases_today = 0
                        else:
                                cases_today = int(row[4]) - old_value
                                old_value = int(row[4])

                        print(cases_today)

                        format_str = '%Y-%m-%d'
                        date_object = datetime.datetime.strptime(row[0], format_str)


                        try:
                            cd_existing = CHCases.objects.get(canton=canton, date=date_object)
                            cd_existing.cases = cases_today
                            cd_existing.save()
                        except CHCases.DoesNotExist:
                            cd = CHCases(canton=canton, cases=cases_today, date=date_object)
                            cd.save()
                    except:
                        print("Wrong format")

            #calc running avg
            last_numbers = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,]
            rec_cases = CHCases.objects.filter(canton=canton).order_by('date')

            print(canton.name)
            for day in rec_cases:
                last_numbers.append(day.cases)
                last_numbers.pop(0)
                tot = 0
                for x in last_numbers:
                    tot += x

                fourteen_avg = tot * 100000 / canton.population
                print(day)
                print(fourteen_avg)
                day.cases_past14days = fourteen_avg
                day.save()
