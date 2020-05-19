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

        url = 'https://www.bfs.admin.ch/bfsstatic/dam/assets/12987231/master'

        myfile = requests.get(url)

        print("Read excel")
        read_file = pd.read_excel(myfile.content, sheet_name = "CH")
        print("Convert and write:")
        read_file.to_csv('/tmp/death_ch.csv', index=None, header=True)

        workpath = os.path.dirname(os.path.abspath(__file__))  # Returns the Path your .py file is in

        country = Country.objects.get(pk=1)

        print("Load data into django")
        # Should move to datasources directory
        with open('/tmp/death_ch.csv', newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')

                rowcount = 0
                savedate = datetime.date(2012,12,30)
                for row in spamreader:
                    rowcount += 1
                    if (rowcount > 7 and rowcount < 61 and row[1] is not ''):

                        avg = int(int(row[1])/7)

                        for number in range(1,8):
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








