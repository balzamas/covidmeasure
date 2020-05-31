from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.models import Country, MeasureCategory, MeasureType, Measure, Continent, CasesDeaths
import os
import csv
import datetime
import requests
import pandas as pd

#Source: https://data.europa.eu/euodp/en/data/dataset/covid-19-coronavirus-data/resource/55e8f966-d5c8-438e-85bc-c7a5a26f4863

def CalcCaesesPerMio(cases, population):
    casespm = int(cases) *1000000 / (int(population))
    return casespm

class Command(BaseCommand):
    def handle(self, *args, **options):

        url = 'https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide.xlsx'

        myfile = requests.get(url)

        print("Read excel")
        read_file = pd.read_excel(myfile.content)
        print("Convert and write:")
        read_file.to_csv('/tmp/casedeath_source.csv', index=None, header=True)



        workpath = os.path.dirname(os.path.abspath(__file__))  # Returns the Path your .py file is in

        print("Load data into django")
        for cntry in Country.objects.all():
            countrycode = cntry.code;
            if (countrycode.lower() == 'gb'):
                countrycode = 'uk'
            if (countrycode.lower() == 'gr'):
                countrycode = 'el'
            print(countrycode)

            # Should move to datasources directory
            with open('/tmp/casedeath_source.csv', newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')

                country = Country.objects.get(code=cntry.code)

                for row in spamreader:
    #                try:
                        if (row[7].lower() == countrycode.lower()):
                            try:
                                   date_object = datetime.date(int(row[3]), int(row[2]), int(row[1]))
                            except:
                                    print("Error")
                            try:
                                cd_existing = CasesDeaths.objects.get(country=country, date=date_object)
                                cd_existing.deaths=row[5]
                                cd_existing.cases = row[4]
                                cd_existing.cases_per_mio = CalcCaesesPerMio(row[4],country.population)
                                cd_existing.save()
                            except CasesDeaths.DoesNotExist:
                                cd = CasesDeaths(country=country, deaths=row[5], cases=row[4], date=date_object, cases_per_mio=CalcCaesesPerMio(row[4],country.population))
                                cd.save()
#                    except:
 #                       print("Error reading line:")
  #                      print(row)







