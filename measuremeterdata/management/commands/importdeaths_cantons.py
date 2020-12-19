from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.models.models import Country
from measuremeterdata.models.models_ch import CHCanton, CHDeaths
import os
import csv
import datetime
import requests
import pandas as pd
from datetime import date, timedelta
from django.db.models import Q


#Source: https://data.europa.eu/euodp/en/data/dataset/covid-19-coronavirus-data/resource/55e8f966-d5c8-438e-85bc-c7a5a26f4863

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

class Command(BaseCommand):
    def handle(self, *args, **options):

        country = Country.objects.get(pk=1)

        url = country.source_death

        myfile = requests.get(url)


        cantons = CHCanton.objects.filter(level=0)

        for canton in cantons:
            print("Read excel")
            read_file = pd.read_excel(myfile.content, sheet_name=canton.code.upper())
            print("Convert and write:")
            read_file.to_csv('/tmp/death_ch.csv', index=None, header=True)

            workpath = os.path.dirname(os.path.abspath(__file__))  # Returns the Path your .py file is in

            print("Load data into django")

            with open('/tmp/death_ch.csv', newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
                rowcount = 0
                for row in spamreader:
                    if rowcount > 6 and row[1] != '':
                        avg = (float(row[2]) + float(row[3]) + float(row[4]) + float(row[5]) + float(row[6]))/5
                        try:
                            cd_existing = CHDeaths.objects.get(canton=canton, week=row[0])
                            print(cd_existing)
                            cd_existing.deaths20 = int(row[1])
                            cd_existing.deaths19 = int(float(row[2]))
                            cd_existing.deaths15 = int(float(row[6]))
                            cd_existing.average_deaths_15_19 = avg
                            cd_existing.save()
                        except CHDeaths.DoesNotExist:
                            cd = CHDeaths(canton=canton, deaths=int(row[1]), deaths19=int(float(row[2])), deaths15=int(float(row[6])), average_deaths=avg, week=row[0])
                            cd.save()
                        except:
                            print("Other error")
                    rowcount += 1



