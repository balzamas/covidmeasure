from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.models import Country, MeasureCategory, MeasureType, Measure, Continent, CasesDeaths, CHCanton, CHCases
import os
import csv
import datetime
import requests
import pandas as pd
from datetime import date, timedelta



#Source: https://data.europa.eu/euodp/en/data/dataset/covid-19-coronavirus-data/resource/55e8f966-d5c8-438e-85bc-c7a5a26f4863

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


def CalcCaesesPerMio(cases, population):
    casespm = int(cases) *1000000 / (int(population))
    return casespm

def set_incidence(last_numbers, bezirk, date):
    total = 0
    for cases in last_numbers:
        total += cases

    ftdays = total / bezirk.population * 100000
    print(ftdays)

    try:
        cd_existing = CHCases.objects.get(canton=bezirk, date=date)
        cd_existing.incidence_past14days = ftdays
        cd_existing.save()
    except CHCases.DoesNotExist:
        cd = CHCases(canton=bezirk, incidence_past14days=ftdays, date=date)
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
                set_incidence(last_numbers_sg, bezirk, date_tosave)

                # Rorschach
                bezirk = CHCanton.objects.get(swisstopo_id=1722)
                last_numbers_rorschach.append(int(row[6]))
                last_numbers_rorschach.pop(0)
                set_incidence(last_numbers_rorschach, bezirk, date_tosave)

                # Rheintal
                bezirk = CHCanton.objects.get(swisstopo_id=1723)
                last_numbers_rheintal.append(int(row[8]))
                last_numbers_rheintal.pop(0)
                set_incidence(last_numbers_rheintal, bezirk, date_tosave)

                # Werdenberg
                bezirk = CHCanton.objects.get(swisstopo_id=1724)
                last_numbers_werdenberg.append(int(row[10]))
                last_numbers_werdenberg.pop(0)
                set_incidence(last_numbers_werdenberg, bezirk, date_tosave)

                # Sarganserland
                bezirk = CHCanton.objects.get(swisstopo_id=1725)
                last_numbers_sarganserland.append(int(row[12]))
                last_numbers_sarganserland.pop(0)
                set_incidence(last_numbers_sarganserland, bezirk, date_tosave)

                # See-Gaster
                bezirk = CHCanton.objects.get(swisstopo_id=1726)
                last_numbers_seegaster.append(int(row[14]))
                last_numbers_seegaster.pop(0)
                set_incidence(last_numbers_seegaster, bezirk, date_tosave)

                # Toggenburg
                bezirk = CHCanton.objects.get(swisstopo_id=1727)
                last_numbers_toggenburg.append(int(row[16]))
                last_numbers_toggenburg.pop(0)
                set_incidence(last_numbers_toggenburg, bezirk, date_tosave)

                # Wil
                bezirk = CHCanton.objects.get(swisstopo_id=1728)
                last_numbers_wil.append(int(row[18]))
                last_numbers_wil.pop(0)
                set_incidence(last_numbers_wil, bezirk, date_tosave)

              count += 1
