from django.core.management.base import BaseCommand, CommandError
from riskcalc.models import BELProvince, BELCases
import os
import csv
import datetime
import requests
import pandas as pd
from datetime import date, timedelta
import urllib.request, json

class Command(BaseCommand):
    def handle(self, *args, **options):
        cases = BELCases.objects.all().order_by("date")
        f = open("bel.csv", "w")
        for case in cases:
            case_total = (case.cases0_9 + case.cases10_19 + case.cases20_29 + case.cases30_39 + case.cases40_49 + case.cases50_59 + case.cases60_69 + case.cases70_79 + case.cases80_89 + case.cases90plus)

            print(f"{case.province.name},{case.province.hasc},{case.date},{case_total}\n")
            f.write(f"{case.province.name},{case.province.hasc},{case.province.population},{case.date},{case_total}\n")
        f.close()


