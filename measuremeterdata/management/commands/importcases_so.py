from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.models.models_ch import CHCanton, CHCases
import os
import csv
import datetime
import requests
import pandas as pd
from datetime import date, timedelta



def get_start_end_dates(year, week):
    d = datetime.datetime(year, 1, 1)
    if (d.weekday() <= 3):
        d = d - timedelta(d.weekday())
    else:
        d = d + timedelta(7 - d.weekday())
    dlt = timedelta(days=(week - 1) * 7)
    return d + dlt + timedelta(days=6)

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def set_incidence(last_numbers, bezirk, date):
    print(last_numbers)

    if (last_numbers[0] != None):
        print(f"No Nones, write {date}")
        total = 0
        total7 = 0
        count = 0
        for cases in last_numbers:
            total += cases
            if (count > 4):
                total7 += cases
            count += 1

        ftdays = total / bezirk.population * 100000
        sdays = total7 / bezirk.population * 100000
        print(ftdays)

        development7to7 = 0
        if (total- total7) > 0:
            development7to7 = (total7 * 100 / (total- total7)) - 100

        try:
            cd_existing = CHCases.objects.get(canton=bezirk, date=date)
            cd_existing.incidence_past14days = ftdays
            cd_existing.incidence_past7days = sdays
            cd_existing.development7to7 = development7to7
            cd_existing.save()
        except CHCases.DoesNotExist:
            cd = CHCases(canton=bezirk, incidence_past14days=ftdays, incidence_past7days=sdays, development7to7=development7to7, date=date)
            cd.save()
        return 0

class Command(BaseCommand):
    def handle(self, *args, **options):

      url="https://raw.githubusercontent.com/openZH/covid_19/master/fallzahlen_bezirke/fallzahlen_kanton_SO_bezirk.csv"

      with requests.Session() as s:

          download = s.get(url)

          decoded_content = download.content.decode('latin-1')

          cr = csv.reader(decoded_content.splitlines(), delimiter=',')
          my_list = list(cr)

            #This is maybe the worst code I've every written but I am hungry

          last_numbers_gaeu = [None, None, None, None, None, None, None, None, None, None ]
          last_numbers_thal = [None, None, None, None, None, None, None, None, None, None ]
          last_numbers_bucheggberg = [None, None, None, None, None, None, None, None, None, None ]
          last_numbers_dorneck = [None, None, None, None, None, None, None, None, None, None ]
          last_numbers_goesgen = [None, None, None, None, None, None, None, None, None, None ]
          last_numbers_wasseramt = [None, None, None, None, None, None, None, None, None, None ]
          last_numbers_lebern = [None, None, None, None, None, None, None, None, None, None ]
          last_numbers_olten = [None, None, None, None, None, None, None, None, None, None ]
          last_numbers_solothurn = [None, None, None, None, None, None, None, None, None, None ]
          last_numbers_thierstein = [None, None, None, None, None, None, None, None, None, None ]

          count = 0
          for row in my_list:
              print(count)
              if (count > 1):
                date_tosave = date.fromisoformat(row[3])

                if row[0] == "1101":
                    bezirk = CHCanton.objects.get(swisstopo_id=1101)
                    last_numbers_gaeu.append(int(row[8]))
                    last_numbers_gaeu.pop(0)
                    set_incidence(last_numbers_gaeu, bezirk, date_tosave)
                elif row[0] == "1102":
                    bezirk = CHCanton.objects.get(swisstopo_id=1102)
                    last_numbers_thal.append(int(row[8]))
                    last_numbers_thal.pop(0)
                    set_incidence(last_numbers_thal, bezirk, date_tosave)
                elif row[0] == "1103":
                    bezirk = CHCanton.objects.get(swisstopo_id=1103)
                    last_numbers_bucheggberg.append(int(row[8]))
                    last_numbers_bucheggberg.pop(0)
                    set_incidence(last_numbers_bucheggberg, bezirk, date_tosave)
                elif row[0] == "1104":
                    bezirk = CHCanton.objects.get(swisstopo_id=1104)
                    last_numbers_dorneck.append(int(row[8]))
                    last_numbers_dorneck.pop(0)
                    set_incidence(last_numbers_dorneck, bezirk, date_tosave)
                elif row[0] == "1105":
                    bezirk = CHCanton.objects.get(swisstopo_id=1105)
                    last_numbers_goesgen.append(int(row[8]))
                    last_numbers_goesgen.pop(0)
                    set_incidence(last_numbers_goesgen, bezirk, date_tosave)
                elif row[0] == "1106":
                    bezirk = CHCanton.objects.get(swisstopo_id=1106)
                    last_numbers_wasseramt.append(int(row[8]))
                    last_numbers_wasseramt.pop(0)
                    set_incidence(last_numbers_wasseramt, bezirk, date_tosave)
                elif row[0] == "1107":
                    bezirk = CHCanton.objects.get(swisstopo_id=1107)
                    last_numbers_lebern.append(int(row[8]))
                    last_numbers_lebern.pop(0)
                    set_incidence(last_numbers_lebern, bezirk, date_tosave)
                elif row[0] == "1108":
                    bezirk = CHCanton.objects.get(swisstopo_id=1108)
                    last_numbers_olten.append(int(row[8]))
                    last_numbers_olten.pop(0)
                    set_incidence(last_numbers_olten, bezirk, date_tosave)
                elif row[0] == "1109":
                    bezirk = CHCanton.objects.get(swisstopo_id=1109)
                    last_numbers_solothurn.append(int(row[8]))
                    last_numbers_solothurn.pop(0)
                    set_incidence(last_numbers_solothurn, bezirk, date_tosave)
                elif row[0] == "1110":
                    bezirk = CHCanton.objects.get(swisstopo_id=1110)
                    last_numbers_thierstein.append(int(row[8]))
                    last_numbers_thierstein.pop(0)
                    set_incidence(last_numbers_thierstein, bezirk, date_tosave)

              count += 1
