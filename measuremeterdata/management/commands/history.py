from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.models.models import Country, CasesDeaths
import os
import csv
import datetime
from datetime import date, timedelta
import requests
import pandas as pd
from io import BytesIO
import gzip
import math
from urllib.request import urlopen
from measuremeterdata.tasks import import_helper
import pandas as pd
import zipfile
import urllib.request, json
from decimal import *
class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('country')


    def handle(self, *args, **kwargs):
        country_code = kwargs['country']

        country = Country.objects.get(code=country_code)

        cases = CasesDeaths.objects.filter(country=country).order_by("date")

        for case in cases:
            if (case.history != None):
                print(case)
                old_value = None
                for his_rec in case.history.all():
                    if old_value:
                        change_perc = (old_value * 100 / his_rec.deathstotal) -100
                        if change_perc != 0:
                            print(f"{his_rec}: New: {7*old_value} - Old: {7*his_rec.deathstotal} - {change_perc}%")
                    old_value = his_rec.deathstotal
                print("...........")

