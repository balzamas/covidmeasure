from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.models.models import Country, MeasureCategory, MeasureType, Measure, Continent, CasesDeaths
import os
import csv
import datetime
import requests
import pandas as pd
from datetime import date, timedelta



#Source: https://data.europa.eu/euodp/en/data/dataset/covid-19-coronavirus-data/resource/55e8f966-d5c8-438e-85bc-c7a5a26f4863

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

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

                start_date = date(2020, 1, 1)
                end_date = date.today()
                for single_date in daterange(start_date, end_date):
                    try:
                        cd_existing_zero = CasesDeaths.objects.get(country=country, date=single_date)
                    except CasesDeaths.DoesNotExist:
                        cd = CasesDeaths(country=country, deaths=0, cases=0, date=single_date)
                        cd.save()

                for row in spamreader:
                    try:
                        if (row[7].lower() == countrycode.lower()):
                            try:
                                   date_object = datetime.date(int(row[3]), int(row[2]), int(row[1]))
                            except:
                                    print("Error")



                            try:
                                cd_existing = CasesDeaths.objects.get(country=country, date=date_object)
                                cd_existing.deaths=row[5]
                                cd_existing.cases = row[4]
                                cd_existing.save()
                            except CasesDeaths.DoesNotExist:
                                cd = CasesDeaths(country=country, deaths=row[5], cases=row[4], date=date_object)
                                cd.save()
                    except:
                        print("Error reading line:")
                        print(row)


            #calc running avg
            last_numbers = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,]
            last_numbers_death = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,]

            rec_cases = CasesDeaths.objects.filter(country=country).order_by('date')

            print(country.name)
            for day in rec_cases:
                last_numbers.append(day.cases)
                last_numbers_death.append(day.deaths)
                last_numbers.pop(0)
                last_numbers_death.pop(0)
                tot = 0
                tot_death = 0
                seven_tot = 0

                daycount = 0
                for x in last_numbers:
                    tot += x

                    if (daycount > 6):
                        seven_tot += x

                    daycount += 1

                for x in last_numbers_death:
                    tot_death += x

                fourteen_avg = tot * 100000 / country.population
                fourteen_avg_death = tot_death * 100000 / country.population
                seven_avg = seven_tot * 100000 / country.population

                day.deaths_past14days = fourteen_avg_death
                day.cases_past14days = fourteen_avg
                day.cases_past7days = seven_avg
                day.save()










