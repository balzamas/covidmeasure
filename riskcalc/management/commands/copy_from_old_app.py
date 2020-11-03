from django.core.management.base import BaseCommand, CommandError
from riskcalc.models import BELProvince, BELAgeGroups
from measuremeterdata.models.models import  BELProvince as BELProvince_old
from measuremeterdata.models.models import  BELAgeGroups as BELAgeGroups_old

import os
import csv
import datetime
import requests
import pandas as pd
from datetime import date, timedelta
import urllib.request, json

class Command(BaseCommand):
    def handle(self, *args, **options):

        for x in BELProvince_old.objects.all().iterator():
            cd = BELProvince()
            cd.name = x.name
            cd.name_source = x.name_source
            cd.population = x.population
            cd.hasc = x.hasc

            cd.save()

        for x in BELAgeGroups_old.objects.all().iterator():
            cd = BELAgeGroups()
            cd.name = x.name
            cd.population = x.population
            cd.save()


