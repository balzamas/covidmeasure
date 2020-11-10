from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.models.models import Country, MeasureCategory, MeasureType, Measure, Continent, CasesDeaths
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

        for row in cr:
            if (row[0].lower() in cntries):
                if row[31]:
                    date_tosave = date.fromisoformat(row[3])

                    country = Country.objects.get(iso_code = row[0])

                    print(country)

                    try:
                        cd_existing = CasesDeaths.objects.get(country=country, date=date_tosave)
                        cd_existing.positivity = Decimal(row[31]) * 100
                        cd_existing.save()
                    except:
                        print("Day record does not exist yet")
