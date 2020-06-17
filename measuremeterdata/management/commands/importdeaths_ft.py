from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.models import Country, MeasureCategory, MeasureType, Measure, Continent, CasesDeaths
import os
import csv
import datetime
from datetime import timedelta, datetime
import requests
import pandas as pd


def loadcountry(country_str, country_pk):
    country = Country.objects.get(pk=country_pk)
    url = country.source_death

    with requests.Session() as s:
        download = s.get(url)

        decoded_content = download.content.decode('utf-8')

        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)

        print("Load data into django")
        for row in my_list:
            if (row[1] == country_str and row[3] == '2020'):
                print(".........,,,,,......")
                save_date = datetime.strptime(row[6], '%Y-%m-%d').date()
                avg = int(float(row[7])) / 7

                print(save_date)
                print(avg)

                for number in range(1, 8):
                    try:
                        cd_existing = CasesDeaths.objects.get(country=country, date=save_date)
                        print(cd_existing)
                        cd_existing.deathstotal = avg
                        cd_existing.save()
                    except CasesDeaths.DoesNotExist:
                        cd = CasesDeaths(country=country, deathstotal=avg, date=save_date)
                        cd.save()
                    save_date += timedelta(days=-1)

class Command(BaseCommand):

    def handle(self, *args, **options):
        print("Loading Italy")
        loadcountry("Italy", 33)

        print("Loading UK")
        loadcountry("UK", 7)

        print("Loading Iceland")
        loadcountry("Iceland", 44)

        print("Loading Belgium")
        loadcountry("Belgium", 14)

        print("Loading Portugal")
        loadcountry("Portugal", 31)

        print("Loading Norway")
        loadcountry("Norway", 22)

        print("Loading Israel")
        loadcountry("Israel", 48)










