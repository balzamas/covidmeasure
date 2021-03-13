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
        for cntry in Country.objects.all():
            if (cntry.iso_code):
                cntries.append(cntry.iso_code.lower())

        row_count = 0
        col_count = 0
        col_positivity = -1
        col_tests = -1
        col_tests_per_p = -1
        col_people_vaccinated_per_hundred = -1

        for row in cr:
            if row_count == 0:
                for col in row:
                    if col == "positive_rate":
                        col_positivity = col_count
                    if col == "new_tests_smoothed_per_thousand":
                        col_tests_per_p = col_count
                    if col == "new_tests":
                        col_tests = col_count
                    if col == "people_vaccinated_per_hundred":
                        col_people_vaccinated_per_hundred = col_count
                    col_count += 1
            row_count += 1

            if (row[0].lower() in cntries):
                if row[col_positivity]:
                    pos = Decimal(row[col_positivity]) * 100
                else:
                    pos = None

                if row[col_tests_per_p]:
                    tests_per_p = Decimal(row[col_tests_per_p])
                else:
                    tests_per_p = None

                if row[col_tests]:
                    tests = Decimal(row[col_tests])
                else:
                    tests = None

                if row[col_people_vaccinated_per_hundred]:
                    people_vaccinated_per_hundred = Decimal(row[col_people_vaccinated_per_hundred])
                else:
                    people_vaccinated_per_hundred = None

                date_tosave = date.fromisoformat(row[3])

                country = Country.objects.get(iso_code = row[0])

                try:
                    cd_existing = CasesDeaths.objects.get(country=country, date=date_tosave)
                    cd_existing.positivity = pos
                    cd_existing.tests_smoothed_per_thousand = tests_per_p
                    cd_existing.tests = tests
                    cd_existing.people_vaccinated_per_hundred = people_vaccinated_per_hundred
                    cd_existing.save()
                except:
                    print("Day record does not exist yet")
