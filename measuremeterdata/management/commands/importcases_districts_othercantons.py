from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.models import Country, MeasureCategory, MeasureType, Measure, Continent, CasesDeaths, CHCanton, CHCases
import os
import csv
import datetime
import requests
import pandas as pd
from datetime import date, timedelta



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

class Command(BaseCommand):
    def handle(self, *args, **options):

      print("Read excel")
      read_file = pd.read_excel('/app/measuremeterdata/datasources/cases_bezirke.xlsx', sheet_name="Cases per Week")
      print("Convert and write:")
      read_file.to_csv('/tmp/cases_cantons.csv', index=None, header=True)

      with open('/tmp/cases_cantons.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')

            print("Load data into django")

            count = 0
            old_bezirk = -1
            last_7days = -1



            for row in spamreader:
                if (count == 1):
                    print(row)
                    weeks_row = row

                if (count > 1):
                    cell_count = 0
                    beznum = -1
                    for cell in row:
                        if (cell is not ''):
                            if (cell_count == 2):
                                print(cell)
                                beznum = cell
                            if (cell_count > 2):

                                date = get_start_end_dates(2020, int(float(weeks_row[cell_count])))

                                bezirk = CHCanton.objects.filter(swisstopo_id=int(float(beznum)))

                                print("-----")
                                print(bezirk)

                                if (bezirk):
                                    ftdays = (int(float(cell)) + last_7days) / bezirk[0].population * 100000

                                    sdays = int(float(cell)) / bezirk[0].population * 100000

                                    print(".....")
                                    print(date)
                                    print(ftdays)

                                    try:
                                        cd_existing = CHCases.objects.get(canton=bezirk[0], date=date)
                                        cd_existing.cases_past7days = sdays
                                        cd_existing.cases_past14days = ftdays
                                        cd_existing.save()
                                    except CHCases.DoesNotExist:
                                        cd = CHCases(canton=bezirk[0], cases_past7days=sdays, cases_past14days=ftdays, date=date)
                                        cd.save()

                                    last_7days = int(float(cell))
                        cell_count += 1

                count += 1

