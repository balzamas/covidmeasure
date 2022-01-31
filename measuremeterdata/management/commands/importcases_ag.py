from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.models.models import Country, MeasureCategory, Continent, CasesDeaths
from measuremeterdata.models.models_ch import CHCanton, CHCases
import os
import csv
import datetime
import requests
import pandas as pd
from datetime import date, timedelta
from django.db.models import Q
from measuremeterdata.tasks import import_helper
from measuremeterdata.tasks.socialmedia.tweet_district_ranking import tweet


def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

class Command(BaseCommand):
    def handle(self, *args, **options):

        url = 'https://www.ag.ch/media/kanton_aargau/themen_1/coronavirus_1/daten_excel/Covid-19-Daten_Kanton_Aargau.xlsx'

        myfile = requests.get(url)


        print("Read excel")
        read_file = pd.read_excel(myfile.content, sheet_name='2.1 Daten Gemeinden')
        print("Convert and write:")
        read_file.to_csv('/tmp/cases_ag.csv', index=None, header=True)

        has_new_data = False

        workpath = os.path.dirname(os.path.abspath(__file__))  # Returns the Path your .py file is in

        print("Load data into django")


        with open('/tmp/cases_ag.csv', newline='') as csvfile:

            spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in spamreader:
                if "Kalenderwoche" in row[0]:
                    week=int(row[0].replace("Kalenderwoche: ", ""))
        date_tosave = import_helper.get_start_end_dates(2022, week)[1]
        print(date_tosave)

        for gemeinde in CHCanton.objects.filter(code='ag', level=1):
            print("......")
            print(gemeinde.name.replace(" (AG)", ""))
            print("......")
            pop = 0
            cases_now = 0
            cases_last = 0
            with open('/tmp/cases_ag.csv', newline='') as csvfile:

                    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
                    for row in spamreader:
                        if row[0] == gemeinde.name.replace(" (AG)",""):
                            try:
                                    pop += float(row[2])
                                    cases_now += float(row[4])
                                    cases_last += float(row[5])
                            except:
                                pass

                    inz7d = 100000*cases_now/pop
                    inz14d= 100000*(cases_now+cases_last)/pop
                    weekoverweek = (cases_now * 100 / cases_last) - 100
                    print(pop)
                    print(cases_now)
                    print(cases_last)
                    print(inz7d)
                    print(inz14d)
                    print(weekoverweek)

                    try:
                        cd_existing = CHCases.objects.get(canton=gemeinde, date=date_tosave)
                        cd_existing.incidence_past7days = inz7d
                        cd_existing.incidence_past14days = inz14d
                        cd_existing.development7to7 = weekoverweek
                        cd_existing.save()
                    except CHCases.DoesNotExist:
                        has_new_data = True
                        cd = CHCases(canton=gemeinde, incidence_past7days=inz7d, incidence_past14days=inz14d, development7to7=weekoverweek, date=date_tosave)
                        cd.save()


        if has_new_data:
            canton_code = "ag"
            canton = CHCanton.objects.filter(level=0, code=canton_code)[0]
            tweet(canton)
