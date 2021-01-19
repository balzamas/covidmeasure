from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.models.models import Country, CasesDeaths
from measuremeterdata.models.models_ch import CHCanton, CHCases, CHStringency
import os
import csv
import datetime
import io
import requests
import pandas as pd
from datetime import date, timedelta
from measuremeterdata.tasks import import_helper

def load_canton(dates, col, canton):
    print(canton)
    row_count = 0
    old_value = 0

    for row in col:
        if float(row) != old_value:
            try:
                cd_existing = CHStringency.objects.get(canton=canton, date=date.fromisoformat(dates[row_count]))
                cd_existing.KOF_value = float(row)
                cd_existing.KOF_value_before = old_value
                cd_existing.save()
            except CHStringency.DoesNotExist:
                cd = CHStringency(canton=canton, date=date.fromisoformat(dates[row_count]),
                             KOF_value=float(row), KOF_value_before=old_value)
                cd.save()
            old_value = float(row)
        row_count += 1


class Command(BaseCommand):
    def handle(self, *args, **options):
        url = "https://datenservice.kof.ethz.ch/api/v1/public/sets/stringency_plus_web?mime=csv&df=Y-m-d"
        s = requests.get(url).content
        df = pd.read_csv(io.StringIO(s.decode('utf-8')))

        for canton in CHCanton.objects.filter(level=0):
            if canton.code != 'fl':
                load_canton(df[f"date"], df[f"ch.kof.stringency.{canton.code}.stringency_plus"],canton)
