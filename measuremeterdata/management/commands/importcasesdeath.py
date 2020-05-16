from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.models import Country, MeasureCategory, MeasureType, Measure, Continent, CasesDeaths
import os
import csv
import datetime

#Source: https://data.europa.eu/euodp/en/data/dataset/covid-19-coronavirus-data/resource/55e8f966-d5c8-438e-85bc-c7a5a26f4863

class Command(BaseCommand):
    def handle(self, *args, **options):
        workpath = os.path.dirname(os.path.abspath(__file__))  # Returns the Path your .py file is in

        cntry = Country.objects.all();

        for cntry in Country.objects.all():
            countrycode = cntry.code;
            print(countrycode)

            # Should move to datasources directory
            with open(os.path.join(workpath, 'covidcasesdeath.csv'), newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=';', quotechar='"')

                country = Country.objects.get(code=countrycode)
                for row in spamreader:
                    if (row[7].lower() == countrycode.lower()):
                        date_field = row[0].split(".")
                        date_object = datetime.date(int(date_field[2]), int(date_field[1]), int(date_field[0]))

                        try:
                            cd_existing = CasesDeaths.objects.get(country=country, date=date_object)
                        except CasesDeaths.DoesNotExist:
                            cd = CasesDeaths(country=country, deaths=row[5], cases=row[4], date=date_object)
                            cd.save()








