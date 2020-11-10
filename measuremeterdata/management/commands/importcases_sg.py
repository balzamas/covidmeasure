from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.models.models_ch import CHCanton, CHCases
import os
import csv
import datetime
import requests
import pandas as pd
from datetime import date, timedelta

#Source: https://data.europa.eu/euodp/en/data/dataset/covid-19-coronavirus-data/resource/55e8f966-d5c8-438e-85bc-c7a5a26f4863

def set_incidence(last_numbers, bezirk, date, cases_today):
    total = 0
    total7 = 0
    count = 0
    for cases in last_numbers:
        total += cases
        if (count > 6):
            total7 += cases
        count += 1

    ftdays = total / bezirk.population * 100000
    sdays = total7 / bezirk.population * 100000

    print(ftdays)
    development7to7 = 0
    if (total - total7) > 0:
        development7to7 = (total7 * 100 / (total - total7)) - 100

    try:
        cd_existing = CHCases.objects.get(canton=bezirk, date=date)
        cd_existing.incidence_past14days = ftdays
        cd_existing.incidence_past7days = sdays
        cd_existing.development7to7 = development7to7
        cd_existing.cases = cases_today
        cd_existing.save()
    except CHCases.DoesNotExist:
        cd = CHCases(canton=bezirk, incidence_past14days=ftdays, incidence_past7days=sdays, cases=cases_today, development7to7=development7to7, date=date)
        cd.save()
    return 0

class Command(BaseCommand):
    def handle(self, *args, **options):

      url="https://www.sg.ch/ueber-den-kanton-st-gallen/statistik/covid-19/_jcr_content/Par/sgch_downloadlist/DownloadListPar/sgch_download.ocFile/KantonSG_C19-Faelle_download.csv"

      with requests.Session() as s:

          download = s.get(url)

          decoded_content = download.content.decode('latin-1')

          cr = csv.reader(decoded_content.splitlines(), delimiter=';')
          my_list = list(cr)

          last_numbers_sg = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
          last_numbers_wil = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
          last_numbers_rorschach = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
          last_numbers_rheintal = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
          last_numbers_werdenberg = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
          last_numbers_sarganserland = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
          last_numbers_seegaster = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
          last_numbers_toggenburg = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]

          print("HANSA")

          count = 0
          for row in my_list:
              print(count)
              if (count > 6):
                date_tosave = date.fromisoformat(row[0])
                # St. Gallen
                bezirk = CHCanton.objects.get(swisstopo_id=1721)
                last_numbers_sg.append(int(row[4]))
                last_numbers_sg.pop(0)
                set_incidence(last_numbers_sg, bezirk, date_tosave, int(row[4]))

                # Rorschach
                bezirk = CHCanton.objects.get(swisstopo_id=1722)
                last_numbers_rorschach.append(int(row[6]))
                last_numbers_rorschach.pop(0)
                set_incidence(last_numbers_rorschach, bezirk, date_tosave, int(row[6]))

                # Rheintal
                bezirk = CHCanton.objects.get(swisstopo_id=1723)
                last_numbers_rheintal.append(int(row[8]))
                last_numbers_rheintal.pop(0)
                set_incidence(last_numbers_rheintal, bezirk, date_tosave, int(row[8]))

                # Werdenberg
                bezirk = CHCanton.objects.get(swisstopo_id=1724)
                last_numbers_werdenberg.append(int(row[10]))
                last_numbers_werdenberg.pop(0)
                set_incidence(last_numbers_werdenberg, bezirk, date_tosave, int(row[10]))

                # Sarganserland
                bezirk = CHCanton.objects.get(swisstopo_id=1725)
                last_numbers_sarganserland.append(int(row[12]))
                last_numbers_sarganserland.pop(0)
                set_incidence(last_numbers_sarganserland, bezirk, date_tosave, int(row[12]))

                # See-Gaster
                bezirk = CHCanton.objects.get(swisstopo_id=1726)
                last_numbers_seegaster.append(int(row[14]))
                last_numbers_seegaster.pop(0)
                set_incidence(last_numbers_seegaster, bezirk, date_tosave, int(row[14]))

                # Toggenburg
                bezirk = CHCanton.objects.get(swisstopo_id=1727)
                last_numbers_toggenburg.append(int(row[16]))
                last_numbers_toggenburg.pop(0)
                set_incidence(last_numbers_toggenburg, bezirk, date_tosave, int(row[16]))

                # Wil
                bezirk = CHCanton.objects.get(swisstopo_id=1728)
                last_numbers_wil.append(int(row[18]))
                last_numbers_wil.pop(0)
                set_incidence(last_numbers_wil, bezirk, date_tosave, int(row[18]))

              count += 1
