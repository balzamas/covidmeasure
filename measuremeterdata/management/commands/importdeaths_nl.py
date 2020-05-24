from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.models import Country, MeasureCategory, MeasureType, Measure, Continent, CasesDeaths
import os
import csv
import datetime
from datetime import timedelta
import requests
import pandas as pd

class Command(BaseCommand):

    def handle(self, *args, **options):

        country = Country.objects.get(pk=13)
        with open('/app/measuremeterdata/datasources/netherlands.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')

            rowcount = 0
            savedate = datetime.date(2019, 12, 30)
            for row in spamreader:
                rowcount += 1
                if (rowcount > 1 and row[4] is not ''):

                    avg = int(int(row[4]) / 7)

                    for number in range(1, 8):
                        try:
                            cd_existing = CasesDeaths.objects.get(country=country, date=savedate)
                            print(cd_existing)
                            cd_existing.deathstotal = avg
                            cd_existing.save()
                        except CasesDeaths.DoesNotExist:
                            cd = CasesDeaths(country=country, deathstotal=avg, date=savedate)
                            cd.save()

                        print(savedate)
                        print(avg)
                        print("....")

                        savedate += timedelta(days=1)
