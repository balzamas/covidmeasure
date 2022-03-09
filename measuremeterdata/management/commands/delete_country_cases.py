from django.core.management.base import BaseCommand, CommandError
from measuremeterdata.models.models import Country, MeasureCategory, Continent, CasesDeaths, CountryMeasure, CountryMeasureType
import os
import csv
import datetime
import requests
import pandas as pd
from datetime import date, datetime, timedelta
from decimal import *




class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('country')

    def handle(self, *args, **kwargs):
        country = kwargs['country']
        delete_country(
            country
        )


def delete_country(country):
    for x in CasesDeaths.objects.filter(country__code=country).iterator(): x.delete()
