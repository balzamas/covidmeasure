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

class Command(BaseCommand):
    def handle(self, *args, **options):

      url = "https://www.sg.ch/tools/informationen-coronavirus/_jcr_content/Par/sgch_downloadlist/DownloadListPar/sgch_download.ocFile/COVID-19_LageberichtSG_FfS.xlsx"

      myfile = requests.get(url)

      print("Read excel")
      read_file = pd.read_excel(myfile.content, sheet_name="Übersicht")
      print("Convert and write:")
      read_file.to_csv('/tmp/cases_sg.csv', index=None, header=True)

      print("Load data into django")
      # Should move to datasources directory
      with open('/tmp/cases_sg.csv', newline='') as csvfile:
          spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')

          rowcount = 0
          savedate = datetime.date(2020, 3, 1)
          deaths_yesterday = 0
          for row in spamreader:
              if (rowcount > 3 and rowcount < 12):
                if (rowcount == 4):
                    #St. Gallen
                    bezirk = CHCanton.objects.filter(swisstopo_id=1721)
                if (rowcount == 5):
                    #Rorschach
                    bezirk = CHCanton.objects.filter(swisstopo_id=1722)
                if (rowcount == 6):
                    # Rheintal
                    bezirk = CHCanton.objects.filter(swisstopo_id=1723)
                if (rowcount == 7):
                    # Werdenberg
                    bezirk = CHCanton.objects.filter(swisstopo_id=1724)
                if (rowcount == 8):
                    # Sarganserland
                    bezirk = CHCanton.objects.filter(swisstopo_id=1725)
                if (rowcount == 9):
                    # See-Gaster
                    bezirk = CHCanton.objects.filter(swisstopo_id=1726)
                if (rowcount == 10):
                    # Toggenburg
                    bezirk = CHCanton.objects.filter(swisstopo_id=1727)
                if (rowcount == 11):
                    # Wil
                    bezirk = CHCanton.objects.filter(swisstopo_id=1728)

                if (bezirk):
                    print(row[1])

                    ftdays = (int(row[2])) / bezirk[0].population * 100000

                    try:
                      cd_existing = CHCases.objects.get(canton=bezirk[0], date=date.today())
                      cd_existing.cases_past14days = ftdays
                      cd_existing.save()
                    except CHCases.DoesNotExist:
                      cd = CHCases(canton=bezirk[0], cases_past14days=ftdays, date=date.today())
                      cd.save()

              rowcount += 1


