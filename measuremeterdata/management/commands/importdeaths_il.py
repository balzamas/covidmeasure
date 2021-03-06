from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.models.models import Country, Continent, CasesDeaths
import os
import csv
import datetime
from datetime import timedelta
import requests
import pandas as pd


def load_data(pk, iso):

    # https://ourworldindata.org/excess-mortality-covid#excess-mortality-statistics-will-only-be-available-for-a-minority-of-countries
    country = Country.objects.get(pk=pk)

    print("Load data into django")
    # Should move to datasources directory
    with open('measuremeterdata/datasources/owid_deaths.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')

        rowcount = 0
        for row in spamreader:
            rowcount += 1
            if (row[1] == iso and row[3] != ""):

                format_str = '%Y-%m-%d'
                savedate = datetime.datetime.strptime(row[2], format_str)

                avg = int(row[3]) / 7
                avg15 = int(row[5]) / 7

                for number in range(1, 8):
                    try:
                        cd_existing = CasesDeaths.objects.get(country=country, date=savedate)
                        print(cd_existing)
                        cd_existing.deathstotal = avg
                        cd_existing.deathstotal_peak = avg15
                        cd_existing.save()
                    except CasesDeaths.DoesNotExist:
                        cd = CasesDeaths(country=country, deathstotal=avg, date=savedate, deathstotal_peak=avg15)
                        cd.save()

                    print(savedate)
                    print(avg)
                    print("....")

                    savedate = savedate - timedelta(days=1)


class Command(BaseCommand):
    def handle(self, *args, **options):
        load_data(48, "ISR")

