from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.models.models_ch import CHCanton, CHCases
import os
import csv
import datetime
import requests
import pandas as pd
from datetime import date, timedelta
from measuremeterdata.tasks.tweet_district_ranking import tweet

class Command(BaseCommand):
    def handle(self, *args, **options):

      url = 'https://raw.githubusercontent.com/openZH/covid_19/master/fallzahlen_bezirke/fallzahlen_kanton_GR_bezirk.csv'

      with requests.Session() as s:
        download = s.get(url)

        decoded_content = download.content.decode('utf-8')

        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)

        print("Load data into django")

        count = 0
        old_bezirk = -1
        last_numbers = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
        cases_yd = 0

        has_new_data = False

        for row in my_list:
            if (count > 1):

                try:
                    bezirk = CHCanton.objects.filter(swisstopo_id=int(row[0]))

                    if (bezirk):
                        if (old_bezirk != int(row[0])):
                            last_numbers = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
                            cases_yd = 0

                        cases_td = int(row[7]) - cases_yd


                        cases_yd = int(row[7])

                        last_numbers.append(cases_td)
                        last_numbers.pop(0)

                        tot = 0
                        seven_tot = 0

                        daycount = 0
                        for x in last_numbers:
                            tot += x

                            if (daycount > 6):
                                seven_tot += x

                            daycount += 1


                        fourteen_avg = tot * 100000 / bezirk[0].population
                        seven_avg = seven_tot * 100000 / bezirk[0].population

                        date_tosave = date.fromisoformat(row[3])

                        development7to7 = 0
                        if (tot - seven_tot) > 0:
                            development7to7 = (seven_tot * 100 / (tot - seven_tot)) - 100

                        print(bezirk[0])
                        print(cases_td)
                        print(date_tosave)
                        print(f"Average:{fourteen_avg}")

                        try:
                            cd_existing = CHCases.objects.get(canton=bezirk[0], date=date_tosave)
                            cd_existing.cases = cases_td
                            cd_existing.incidence_past7days = seven_avg
                            cd_existing.incidence_past14days = fourteen_avg
                            cd_existing.development7to7 = development7to7
                            cd_existing.date = date_tosave
                            cd_existing.save()
                        except CHCases.DoesNotExist:
                            cd = CHCases(canton=bezirk[0], incidence_past7days=seven_avg, incidence_past14days=fourteen_avg, cases=cases_td, development7to7=development7to7, date=date_tosave)
                            has_new_data = True
                            cd.save()

                    old_bezirk = int(row[0])

                except:
                    print("Nonedata")
                    old_bezirk = -1
                    last_numbers = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
                    cases_yd = 0

            count += 1

        if has_new_data:
            canton_code = "gr"
            canton = CHCanton.objects.filter(level=0, code=canton_code)[0]
            tweet(canton)
