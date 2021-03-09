from django.core.management.base import BaseCommand, CommandError
from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.models.models import Country, MeasureCategory, Continent, CasesDeaths
import os
import csv
import datetime
from datetime import timedelta
import requests
import pandas as pd

class Command(BaseCommand):
    def handle(self, *args, **options):

        country = Country.objects.get(pk=1)

        url = country.source_death

        myfile = requests.get(url)


        print("Read excel")
        read_file = pd.read_excel(myfile.content, sheet_name="CH", skiprows=5)

        print(read_file.keys())

        savedate20 = datetime.date(2019, 12, 30)
        savedate21 = datetime.date(2021, 1, 4)

        for index, row in read_file.iterrows():
            print(index)

            try:
                if row['Unnamed: 0'] != "Woche ":
                    week = int(row['Unnamed: 0'])

                    val15 = None
                    val20 = None
                    val21 = None



                    val20 = int(row["2020 2"])
                    val15 = int(row[2015])

                    if week < 53:
                        avg_1519 = (int(row[2015]) + int(row[2016]) + int(row[2017]) + int(row[2018]) + int(
                            row[2019])) / 5
                    else:
                        avg_1519 = int(row[2015])

                    avg_1519 = avg_1519 / 7

                    if  pd.notna(row["2021 2"]) and row["2021 2"]:
                        val21 = int(row["2021 2"])

                        avg21 = int(val21)/7
                        avg_peak21 = float(val15)/7

                        for number in range(1,8):
                            try:
                                cd_existing = CasesDeaths.objects.get(country=country, date=savedate21)
                                print(cd_existing)
                                cd_existing.deathstotal = avg21
                                cd_existing.deathstotal_peak = avg_peak21
                                cd_existing.deathstotal_average = avg_1519
                                cd_existing.save()
                            except CasesDeaths.DoesNotExist:
                                cd = CasesDeaths(country=country, deathstotal=avg21, deathstotal_peak=avg_peak21, deathstotal_average = avg_1519, date=savedate21)
                                cd.save()

                            savedate21 += timedelta(days=1)


                    avg20 = int(val20) / 7
                    avg_peak20 = float(val15) / 7

                    for number in range(1, 8):
                        try:
                            cd_existing = CasesDeaths.objects.get(country=country, date=savedate20)
                            print(cd_existing)
                            cd_existing.deathstotal = avg20
                            cd_existing.deathstotal_peak = avg_peak20
                            cd_existing.deathstotal_average = avg_1519
                            cd_existing.save()
                        except CasesDeaths.DoesNotExist:
                            cd = CasesDeaths(country=country, deathstotal=avg20, deathstotal_peak=avg_peak20, deathstotal_average = avg_1519,
                                             date=savedate20)
                            cd.save()

                        savedate20 += timedelta(days=1)

            except:
                print("error")


    def handleX(self, *args, **options):

        country = Country.objects.get(pk=1)

        url = country.source_death

        myfile = requests.get(url)

        print("Read excel")
        read_file = pd.read_excel(myfile.content, sheet_name = "CH")
        print("Convert and write:")
        read_file.to_csv('/tmp/death_ch.csv', index=None, header=True)

        workpath = os.path.dirname(os.path.abspath(__file__))  # Returns the Path your .py file is in


        print("Load data into django")
        # Should move to datasources directory
        with open('/tmp/death_ch.csv', newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')

                rowcount = 0
                savedate20 = datetime.date(2019,12,30)
                savedate21 = datetime.date(2021,1,4)
                for row in spamreader:
                    rowcount += 1
                    if (rowcount > 7 and rowcount < 61):

                        avg21 = int(row[1])/7
                        avg_peak21 = float(row[6])/7

                        for number in range(1,8):
                            try:
                                cd_existing = CasesDeaths.objects.get(country=country, date=savedate21)
                                print(cd_existing)
                                cd_existing.deathstotal = avg21
                                cd_existing.deathstotal_peak = avg_peak21
                                cd_existing.save()
                            except CasesDeaths.DoesNotExist:
                                cd = CasesDeaths(country=country, deathstotal=avg21, deathstotal_peak=avg_peak21, date=savedate21)
                                cd.save()

                        avg20 = int(row[0]) / 7
                        avg_peak20 = float(row[6]) / 7

                        for number in range(1, 8):
                            try:
                                cd_existing = CasesDeaths.objects.get(country=country, date=savedate20)
                                print(cd_existing)
                                cd_existing.deathstotal = avg20
                                cd_existing.deathstotal_peak = avg_peak20
                                cd_existing.save()
                            except CasesDeaths.DoesNotExist:
                                cd = CasesDeaths(country=country, deathstotal=avg20, deathstotal_peak=avg_peak20,
                                                 date=savedate20)
                                cd.save()

                            print(savedate21)
                            print(avg21)
                            print("....")

                            savedate21 += timedelta(days=1)

