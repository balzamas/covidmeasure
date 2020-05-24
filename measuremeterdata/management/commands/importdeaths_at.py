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

        country = Country.objects.get(pk=6)

        url = country.source_death

        myfile = requests.get(url)

        print("Read excel")
        read_file = pd.read_excel(myfile.content)
        print("Convert and write:")
        read_file.to_csv('/tmp/death_at.csv', index=None, header=True)

        workpath = os.path.dirname(os.path.abspath(__file__))  # Returns the Path your .py file is in


        print("Load data into django")
        # Should move to datasources directory
        with open('/tmp/death_at.csv', newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')

                #I failed to sort the xls with pandas, so we reverse it here
                weeks=[]
                for row_rev in spamreader:
                    if (row_rev[0].startswith('2020')):
                        weeks.append(row_rev)

                weeks.reverse()

                rowcount = 0
                savedate = datetime.date(2020,1,1)
                for row in weeks:
                        print(row)
                        rowcount += 1

                        if (rowcount == 1):
                            avg = int(int(row[2]) / 5)
                            max_day=6
                        else:
                            avg = int(int(row[2])/7)
                            max_day=8

                        for number in range(1,max_day):
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








