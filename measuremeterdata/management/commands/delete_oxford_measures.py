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
    def handle(self, *args, **options):

        delete_oxford(
            10
        )

        delete_oxford(
            1
        )

        delete_oxford(
            2
        )

        delete_oxford(
            3
        )

        delete_oxford(
            4
        )

        delete_oxford(
            5
        )

        delete_oxford(
            6
        )

        delete_oxford(
            7
        )



        delete_oxford(
            8
        )

        delete_oxford(
            9
        )

def delete_oxford(type):
    for x in CountryMeasure.objects.filter(type=type).iterator(): x.delete()
