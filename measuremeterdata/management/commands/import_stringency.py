from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.models.models import Country, MeasureCategory, MeasureType, Measure, Continent, CasesDeaths, OxfordMeasure, OxfordMeasureType
import os
import csv
import datetime
import requests
import pandas as pd
from datetime import date, datetime, timedelta
from decimal import *

class Command(BaseCommand):
    def handle(self, *args, **options):

        url = 'https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/timeseries/stringency_index.csv'
        with requests.Session() as s:
            download = s.get(url)

            decoded_content = download.content.decode('utf-8')

            cr = csv.reader(decoded_content.splitlines(), delimiter=',')

            # Load countries
            cntries = []
            for cntry in Country.objects.all():
                if (cntry.iso_code):
                    cntries.append(cntry.iso_code.lower())

            row_count = 0

            for row in cr:
                if row_count == 0:
                    firstrow = row
                row_count += 1

                if len(row) > 1 and row[1].lower() in cntries:
                    print(row[1])
                    country = Country.objects.get(iso_code=row[1])

                    col_num = 0
                    for col in row:
                        if (col_num > 2):

                            if col != "":

                                date = datetime.strptime(firstrow[col_num], '%d%b%Y')

                                stringency_index = float(col)
                                try:
                                    measure = CasesDeaths.objects.get(country=country, date=date)
                                    measure.stringency_index = stringency_index
                                    measure.save()
                                except:
                                    measure = CasesDeaths(country=country, date=date, stringency_index=stringency_index)
                                    measure.save()
                        col_num += 1
