from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.models.models import Country
from measuremeterdata.models.models_ch import CHCanton, CHDeaths
import os
import csv
import datetime
import requests
import pandas as pd
from datetime import date, timedelta
from django.db.models import Q
from measuremeterdata.tasks.importer.ch.importdeaths_cantons import import_data

class Command(BaseCommand):
    def handle(self, *args, **options):
        import_data()
