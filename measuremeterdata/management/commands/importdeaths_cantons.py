from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.models.models import Country
from measuremeterdata.models.models_ch import CHCanton, CHDeaths
import os
import csv
import datetime
import requests
import pandas as pd
from datetime import date, timedelta
from django.db.models import Q

class Command(BaseCommand):
    def handle(self, *args, **options):

        country = Country.objects.get(pk=1)

        url = country.source_death

        myfile = requests.get(url)


        cantons = CHCanton.objects.filter(level=0)

        for canton in cantons:
            print("Read excel")
            print(canton)
            read_file = pd.read_excel(myfile.content, sheet_name=canton.code.upper(), skiprows=5)

            print(read_file.keys())

            for index, row in read_file.iterrows():
                print(index)

                try:
                    week = int(row['Unnamed: 0'])

                    val15 = None
                    val16 = None
                    val17 = None
                    val18 = None
                    val19 = None
                    val20 = None
                    val21 = None

                    val20 = int(row["2020 2"])
                    val15 = int(row[2015])

                    if week < 53:
                        print("......")
                        print(row["2021 2"])
                        if pd.notna(row["2021 2"]) and row["2021 2"] != '':
                            print("Has 21 value")
                            val21 = int(row["2021 2"])

                        val19 = int(row[2019])
                        val18 = int(row[2018])
                        val17 = int(row[2017])
                        val16 = int(row[2016])
                        val15 = int(row[2015])
                        avg = (val15 + val16 + val17 + val18 + val19)/5
                    else:
                        avg = val15

                    try:
                        cd_existing = CHDeaths.objects.get(canton=canton, week=week)
                        print(cd_existing)
                        cd_existing.deaths21 = val21
                        cd_existing.deaths20 = val20
                        cd_existing.deaths19 = val19
                        cd_existing.deaths15 = val15
                        cd_existing.average_deaths_15_19 = avg
                        cd_existing.save()
                        print("saved")
                    except CHDeaths.DoesNotExist:
                        cd = CHDeaths(canton=canton, deaths21=val21, deaths20=val20, deaths19=val19, deaths15=val15, average_deaths_15_19=avg, week=week)
                        cd.save()
                    except:
                        print("Other error")

                except:
                    print("error")
