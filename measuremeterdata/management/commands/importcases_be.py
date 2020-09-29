from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.models import Country, MeasureCategory, MeasureType, Measure, Continent, CasesDeaths, CHCanton, CHCases
import os
import csv
import datetime
import requests
import pandas as pd
from datetime import date, timedelta

class Command(BaseCommand):
    def handle(self, *args, **options):

      url = 'https://www.be.ch/corona'

      with requests.Session() as s:
        download = s.get(url)

        with open(download.content, 'r') as f:
            decoded_content = download.content.decode('utf-8')

            for line in f:
                print(line)
                print(".......")



