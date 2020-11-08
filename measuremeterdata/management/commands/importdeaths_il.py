from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.models.models import Country, MeasureCategory, MeasureType, Measure, Continent, CasesDeaths
import os
import csv
import datetime
from datetime import timedelta
import requests
import pandas as pd

class Command(BaseCommand):

    def handle(self, *args, **options):

        country = Country.objects.get(pk=48)

        print("Load data into django")
        # Should move to datasources directory
        with open('measuremeterdata/datasources/owid_deaths.csv', newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')

                rowcount = 0
                for row in spamreader:
                    rowcount += 1
                    if (row[1] == "ISR" and row[3] != ""):

                        format_str = '%Y-%m-%d'
                        savedate = datetime.datetime.strptime(row[2], format_str)

                        avg = int(row[3])/7
                        avg15 = int(row[5])/7

                        for number in range(1,8):
                            try:
                                cd_existing = CasesDeaths.objects.get(country=country, date=savedate)
                                print(cd_existing)
                                cd_existing.deathstotal = avg
                                cd_existing.deathstotal_peak = avg15
                                cd_existing.save()
                            except CasesDeaths.DoesNotExist:
                                cd = CasesDeaths(country=country, deathstotal=avg, date=savedate, deathstotal_peak = avg15)
                                cd.save()

                            print(savedate)
                            print(avg)
                            print("....")

                            savedate = savedate - timedelta(days=1)








