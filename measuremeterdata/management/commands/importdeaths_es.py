from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.models import Country, MeasureCategory, MeasureType, Measure, Continent, CasesDeaths
import os
import csv
import requests

import datetime
from datetime import timedelta
import requests
import pandas as pd

class Command(BaseCommand):

    def handle(self, *args, **options):

        country = Country.objects.get(pk=20)

        url = country.source_death

        with requests.Session() as s:
            download = s.get(url)

            decoded_content = download.content.decode('utf-8')

            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            my_list = list(cr)

            rowcount = 0
            savedate = datetime.date(2020, 1, 1)

            for row in my_list:
                if (row[0] == 'nacional' and row[5] == 'todos' and row[7] == 'todos' and row[8].startswith('2020')):
                    rowcount += 1
                    try:
                            cd_existing = CasesDeaths.objects.get(country=country, date=savedate)
                            cd_existing.deathstotal = int(float(row[9]))
                            cd_existing.save()
                    except CasesDeaths.DoesNotExist:
                            cd = CasesDeaths(country=country, deathstotal=int(float(row[9])), date=savedate)
                            cd.save()

                    print(savedate)
                    print(row[9])
                    print("-----")

                    savedate += timedelta(days=1)


