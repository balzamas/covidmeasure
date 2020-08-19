from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.models import Country, MeasureCategory, MeasureType, Measure, Continent, CasesDeaths
import os
import csv
import datetime
from datetime import timedelta
import requests
import pandas as pd
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen

def CalcCaesesPer100k(cases, population):
    casespm = int(cases) *100000 / (int(population))
    return casespm

class Command(BaseCommand):

    def handle(self, *args, **options):

        country = Country.objects.get(pk=34)

        url = country.source_death

        resp = urlopen(url)
        myfile = ZipFile(BytesIO(resp.read()))

        print(myfile.namelist())

        print("Read excel")
        read_file = pd.read_excel(myfile.open('2020-06-12_deces_quotidiens_departement.xlsx'), sheet_name = "France")
        print("Convert and write:")
        read_file.to_csv('/tmp/death_fr.csv', index=None, header=True)

        print("Load data into django")
        # Should move to datasources directory
        with open('/tmp/death_fr.csv', newline='') as csvfile:
               spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')

               rowcount = 0
               savedate = datetime.date(2020,3,1)
               deaths_yesterday = 0
               for row in spamreader:
                    rowcount += 1
                    if (rowcount > 4 and row[2] != ''):

                        tdy_temp=int(row[2])

                        deaths_today = tdy_temp - deaths_yesterday
                        deaths_yesterday = tdy_temp

                        print(savedate)
                        print(deaths_today)
                        print("-----")

                        try:
                            cd_existing = CasesDeaths.objects.get(country=country, date=savedate)
                            print(cd_existing)
                            cd_existing.deathstotal = deaths_today
                            cd_existing.deaths_total_per100k = CalcCaesesPer100k(deaths_today, country.population)
                            cd_existing.save()
                        except CasesDeaths.DoesNotExist:
                            cd = CasesDeaths(country=country, deathstotal=deaths_today, date=savedate, deaths_total_per100k = CalcCaesesPer100k(deaths_today, country.population))
                            cd.save()

                        savedate += timedelta(days=1)
