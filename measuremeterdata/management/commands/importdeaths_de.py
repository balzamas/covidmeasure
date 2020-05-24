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

        country = Country.objects.get(pk=35)

        url = country.source_death

        myfile = requests.get(url)

        print("Read excel")
        read_file = pd.read_excel(myfile.content, sheet_name = "D_2020_Tage")
        print("Convert and write:")
        read_file.to_csv('/tmp/death_de.csv', index=None, header=True)

        workpath = os.path.dirname(os.path.abspath(__file__))  # Returns the Path your .py file is in


        print("Load data into django")
        # Should move to datasources directory
        with open('/tmp/death_de.csv', newline='') as csvfile:
               spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')

               rowcount = 0
               savedate = datetime.date(2020,1,1)
               for row in spamreader:
                    rowcount += 1
                    if (rowcount == 10):
                        cellcount = 0
                        for cell in row:
                            cellcount += 1
                            if (cellcount > 1):
                                try:
                                    cd_existing = CasesDeaths.objects.get(country=country, date=savedate)
                                    cd_existing.deathstotal = cell
                                    cd_existing.save()
                                except CasesDeaths.DoesNotExist:
                                    cd = CasesDeaths(country=country, deathstotal=cell, date=savedate)
                                    cd.save()

                                savedate += timedelta(days=1)

                                print(savedate)
                                print(cell)
                                print("....")
