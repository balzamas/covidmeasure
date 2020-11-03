from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.models.models_bel import BELProvince, BELCases
import os
import csv
import datetime
import requests
import pandas as pd
from datetime import date, timedelta
import urllib.request, json

class Command(BaseCommand):
    def handle(self, *args, **options):

      url_toload = 'https://epistat.sciensano.be/Data/COVID19BE_CASES_AGESEX.json'

      for x in BELCases.objects.all().iterator(): x.delete()

      with urllib.request.urlopen(url_toload) as url:
          data = json.loads(url.read().decode())
          count = 0
          for row in data:
              count+=1
              print(count)
              if 'PROVINCE' in row and 'AGEGROUP' in row and 'DATE' in row:
                    province = BELProvince.objects.filter(name_source=row['PROVINCE'])
                    date_tosave = date.fromisoformat(row["DATE"])
                    print(province)

                    if (province):
                        try:
                            cd = BELCases.objects.get(province=province[0], date=date_tosave)
                        except BELCases.DoesNotExist:
                            print("Does not Exist")
                            cd = BELCases(province=province[0], date=date_tosave)

                        if (row["AGEGROUP"] == "0-9"):
                            cd.cases0_9 += int(row["CASES"])
                        elif (row["AGEGROUP"] == "10-19"):
                            cd.cases10_19 += int(row["CASES"])
                        elif (row["AGEGROUP"] == "20-29"):
                            cd.cases20_29 += int(row["CASES"])
                        elif (row["AGEGROUP"] == "30-39"):
                            cd.cases30_39 += int(row["CASES"])
                        elif (row["AGEGROUP"] == "40-49"):
                            cd.cases40_49 += int(row["CASES"])
                        elif (row["AGEGROUP"] == "50-59"):
                            cd.cases50_59 += int(row["CASES"])
                        elif (row["AGEGROUP"] == "60-69"):
                            cd.cases60_69 += int(row["CASES"])
                        elif (row["AGEGROUP"] == "70-79"):
                            cd.cases70_79 += int(row["CASES"])
                        elif (row["AGEGROUP"] == "80-89"):
                            cd.cases80_89 += int(row["CASES"])
                        elif (row["AGEGROUP"] == "90+"):
                            cd.cases90plus += int(row["CASES"])

                        cd.save()
                        print(province)
                        print(date_tosave)
